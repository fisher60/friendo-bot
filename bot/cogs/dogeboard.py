import logging
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

from discord import Color, Embed, Member, Message, RawReactionActionEvent, Reaction, TextChannel
from discord.ext.commands import Cog, Context, group

from bot import settings

if TYPE_CHECKING:
    from bot.bot import Friendo

log = logging.getLogger(__name__)


@dataclass
class DogeBoardData:
    """
    Dataclass to hold the data retrieved from the API.

    Names are made to match the API field names.
    """

    guild_id: int
    dogeboard_id: int
    dogeboard_emoji: str = "🐶"
    dogeboard_reactions_required: int = 5


class DogeBoard(Cog):
    """Starboard Copy."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot
        self._cache: dict[int, DogeBoardData] = {}
        self._token: str | None = None
        self._url = settings.FRIENDO_API_URL
        self.doged_messages = []

    async def _get_guild_data(self, guild_id: int) -> DogeBoardData | None:
        """
        Attempt to get the dogeboard_data from cache using guild_id.

        if the data is not in the cache, it will request it from the GraphQL DB.
        if the data doesn't exist in the database it will be created and send to GraphQL DB
        """
        if (dogeboard_data := self._cache.get(guild_id)) or (
            dogeboard_data := await self._fetch_guild_data(guild_id)
        ):
            return dogeboard_data
        return None

    async def _fetch_guild_data(self, guild_id: int) -> DogeBoardData | None:
        """Attempt to fetch guild data from the GraphQL database."""
        query = (
            "mutation fetch_guild($guild_id: BigInt!) {"
            "   get_guild(data: { guild_id: $guild_id }) {"
            "    guild_id"
            "    dogeboard_id"
            "    dogeboard_emoji"
            "    dogeboard_reactions_required"
            "  }"
            "}"
        )
        variables = {"guild_id": guild_id}

        resp = await self.bot.graphql.request(json={"query": query, "variables": variables})
        log.info(resp)
        if resp.get("errors"):
            return None
        dogeboard_data = DogeBoardData(**resp["data"]["get_guild"])
        self._cache[guild_id] = dogeboard_data

        return dogeboard_data

    async def _update_guild_data(self, dogeboard: DogeBoardData) -> None:
        """Update the cache and api with the new dogeboard data."""
        query = (
            "mutation modify("
            "   $guild_id: BigInt!,"
            "   $dogeboard_id: BigInt!,"
            "   $dogeboard_emoji: String!,"
            "   $dogeboard_reactions_required: Int!"
            "){"
            "   modify_guild("
            "       data: {"
            "           guild_id: $guild_id,"
            "           dogeboard_id: $dogeboard_id,"
            "           dogeboard_emoji: $dogeboard_emoji,"
            "           dogeboard_reactions_required: $dogeboard_reactions_required"
            "       }"
            "   ){"
            "       guild_id"
            "   }"
            "}"
        )

        await self.bot.graphql.request(json={"query": query, "variables": asdict(dogeboard)})
        self._cache[dogeboard.guild_id] = dogeboard

    @staticmethod
    async def _send_dogeboard_message(message: Message, channel: TextChannel) -> None:
        embed = Embed(
            title=message.author.display_name,
            description=message.content + f"\n\n[Jump to message]({message.jump_url})",
            colour=message.author.colour,
        )
        embed.set_thumbnail(url=message.author.avatar.url)

        # Set the image to the first one if there is one
        for attachment in message.attachments:
            *_, ext = attachment.filename.split(".")
            if ext in ["jpg", "png", "jpeg", "gif", "gifv"]:
                embed.set_image(url=attachment.url)
                break

        await channel.send(embed=embed)
        await message.add_reaction("✅")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        """Handle event when users add reactions."""
        # Ensure the caches are ready
        await self.bot.wait_until_ready()

        dogeboard_data = await self._get_guild_data(payload.guild_id)
        if not dogeboard_data:
            return

        if str(payload.emoji) == dogeboard_data.dogeboard_emoji:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)

            # Prevent bot messages from being starred
            if message.author == self.bot.user:
                return

            dogeboard_reaction: Reaction | None = None
            for reaction in message.reactions:
                if reaction.emoji == "✅":
                    if self.bot.user in await reaction.users().flatten():
                        # If the bot has set a checkmark reaction to this message,
                        # it's already been DogeBoarded
                        return

                elif str(reaction.emoji) == str(payload.emoji):
                    dogeboard_reaction = reaction

            if dogeboard_reaction and message.id not in self.doged_messages:
                if dogeboard_reaction.count >= dogeboard_data.dogeboard_reactions_required:
                    self.doged_messages.append(message.id)
                    dogeboard_channel = self.bot.get_channel(dogeboard_data.dogeboard_id)
                    await self._send_dogeboard_message(message, dogeboard_channel)

    @group(brief="Collate the best message of the server using reactions")
    async def dogeboard(self, ctx: Context) -> None:
        """Command group for DogeBoard."""
        if not ctx.subcommand_passed:
            dogeboard_data = await self._get_guild_data(ctx.guild.id)
            embed = Embed(title="DogeBoard", color=Color.blurple())

            if not dogeboard_data:
                embed.description = (
                    "DogeBoard is not configured, use `.dogeboard channel <channel>` to start."
                )
            else:
                embed.add_field(name="Emoji", value=dogeboard_data.dogeboard_emoji)
                embed.add_field(
                    name="Channel", value=ctx.guild.get_channel(dogeboard_data.dogeboard_id).mention
                )
                embed.add_field(name="Required", value=str(dogeboard_data.dogeboard_reactions_required))

            await ctx.send(embed=embed)

    @dogeboard.command(brief="Set the dogeboard_emoji used for the DogeBoard, Custom Emojis Only")
    async def emoji(self, ctx: Context) -> None:
        """Set the dogeboard_emoji used for the DogeBoard."""
        dogeboard_data = await self._get_guild_data(ctx.guild.id)

        if not dogeboard_data:
            await ctx.send(
                ">>> DogeBoard has not been configured for this guild.\n"
                "Use `.dogeboard channel <channel>` to enable this feature.\n"
                "You can configure the emoji and required reactions by using.\n"
                "Use `.dogeboard emoji` to configure the emoji.\n"
                "User `.dogeboard required <amount>` to configure the required reactions."
            )
            return None

        reaction_msg = await ctx.send(content="> React with the new dogeboard_emoji")

        def check(reaction: Reaction, member: Member) -> bool:
            return member == ctx.author and reaction_msg == reaction.message

        try:
            reaction, _member = await self.bot.wait_for("reaction_add", check=check, timeout=60)
        except TimeoutError:
            return await reaction_msg.edit(content="> You didn't react, Canceling dogeboard_emoji change.")
        finally:
            await reaction_msg.delete(delay=10)

        # Default Emoji or Guild dogeboard_emoji
        if not reaction.custom_emoji or reaction.emoji in ctx.guild.emojis:
            dogeboard_data.dogeboard_emoji = str(reaction.emoji)
        else:
            await ctx.send("> Please react with a default or guild dogeboard_emoji.")
            return None

        await ctx.send(f"> Updated your emoji to {dogeboard_data.dogeboard_emoji}")
        await self._update_guild_data(dogeboard_data)
        return None

    @dogeboard.command(brief="Set the channel for DogeBoard messages to be sent to.")
    async def channel(self, ctx: Context, channel: TextChannel) -> None:
        """Set the channel used for the DogeBoard."""
        dogeboard_data = await self._get_guild_data(ctx.guild.id)

        if not dogeboard_data:
            dogeboard_data = DogeBoardData(guild_id=ctx.guild.id, dogeboard_id=channel.id)
        else:
            dogeboard_data.dogeboard_id = channel.id

        await self._update_guild_data(dogeboard_data)
        await ctx.send(f"> Updated the channel for DogeBoard to: {channel.mention}", delete_after=5)

    @dogeboard.command(brief="Set the reactions required for the DogeBoard")
    async def required(self, ctx: Context, amount: int) -> None:
        """Set the amount of required emojis to trigger the DogeBoard."""
        dogeboard_data = await self._get_guild_data(ctx.guild.id)

        if not dogeboard_data:
            await ctx.send(
                ">>> DogeBoard has not been configured for this guild.\n"
                "Use `.dogeboard channel <channel>` to enable this feature.\n"
                "You can configure the emoji and required reactions by using.\n"
                "Use `.dogeboard emoji` to configure the emoji.\n"
                "User `.dogeboard required <amount>` to configure the required reactions."
            )
            return

        dogeboard_data.dogeboard_reactions_required = amount
        await self._update_guild_data(dogeboard_data)
        await ctx.send(f"> Updated DogeBoard required reactions to: {amount}", delete_after=5)


async def setup(bot: Friendo) -> None:
    """Adding the help cog."""
    if not settings.FRIENDO_API_USER:
        msg = "Missing environment variable: FRIENDO_API_USER"
        raise OSError(msg)
    if not settings.FRIENDO_API_PASS:
        msg = "Missing environment variable: FRIENDO_API_PASS"
        raise OSError(msg)

    await bot.add_cog(DogeBoard(bot))
