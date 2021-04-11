import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from aiohttp import ClientResponse
from discord import Color, Embed, Member, Message, RawReactionActionEvent, Reaction, TextChannel
from discord.ext.commands import Cog, Context, group

from bot import settings
from bot.bot import Friendo

log = logging.getLogger(__name__)


class QueryError(Exception):
    """Error containing all query errors."""

    errors: Tuple[Any]

    def __init__(self, *errors, **kwargs):
        self.errors = errors


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
    """Starboard Copy."""""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot
        self._cache: Dict[int, DogeBoardData] = {}
        self._token: Optional[str] = None
        self._url = settings.FRIENDO_API_URL

    @property
    def headers(self) -> Dict[str, str]:
        """Get headers used in API calls."""
        if self._token:
            return {"Authorization": f"Bearer {self._token}"}

    @staticmethod
    async def _handle_request(resp: ClientResponse) -> Dict[str, Any]:
        """Handle the request errors and status codes."""
        if resp.status != 200:
            raise ConnectionError(f"Error: {resp.status} | Cannot connect to GraphQL Database")

        data = await resp.json()
        if errors := data.get("errors"):
            raise QueryError([error["message"] for error in errors])
        return data

    async def _login(self) -> None:
        """Login to the GraphQL database and store the token."""
        query = """mutation {
          login(data: { username: "%s", password: "%s" }) {
            token
          }
        }
        """ % (settings.FRIENDO_API_USER, settings.FRIENDO_API_PASS)

        async with self.bot.session.post(self._url, json={"query": query}) as resp:
            data = await self._handle_request(resp)
            try:
                self._token = data["data"]["login"]["token"]
            except QueryError as e:
                log.error(f"Couldn't login: {e}")

    async def _get_guild_data(self, guild_id: int) -> Optional[DogeBoardData]:
        """
        Attempt to get the dogeboard_data from cache using guild_id.

        if the data is not in the cache, it will request it from the GraphQL DB.
        if the data doesn't exist in the database it will be created and send to GraphQL DB
        """
        if self._token is None:
            await self._login()

        if dogeboard_data := self._cache.get(guild_id):
            return dogeboard_data
        elif dogeboard_data := await self._fetch_guild_data(guild_id):
            return dogeboard_data

    async def _fetch_guild_data(self, guild_id: int) -> Optional[DogeBoardData]:
        """Attempt to fetch guild data from the GraphQL database."""
        query = """mutation {
            get_guild(data: { guild_id: "%s", }) {
                guild_id
                dogeboard_id
                dogeboard_emoji
                dogeboard_reactions_required
              }
        }""" % guild_id

        async with self.bot.session.post(self._url, json={"query": query}, headers=self.headers) as resp:
            try:
                data = await self._handle_request(resp)

                dogeboard_data = DogeBoardData(**data["data"]["get_guild"])
                self._cache[guild_id] = dogeboard_data
                return dogeboard_data
            except QueryError as e:
                log.error(f"Query Errors: {e}")

    async def _update_guild_data(self, dogeboard: DogeBoardData) -> None:
        """Update the cache and api with the new dogeboard data."""
        if self._token is None:
            await self._login()

        self._cache[dogeboard.guild_id] = dogeboard
        query = """mutation {
            modify_guild(data: {
                guild_id: %d,
                dogeboard_id: %d,
                dogeboard_emoji: "%s",
                dogeboard_reactions_required: %d
            }) {
              guild_id
          }
        }""" % (
            dogeboard.guild_id,
            dogeboard.dogeboard_id,
            dogeboard.dogeboard_emoji,
            dogeboard.dogeboard_reactions_required
        )

        async with self.bot.session.post(self._url, json={"query": query}, headers=self.headers) as resp:
            try:
                await self._handle_request(resp)
                self._cache[dogeboard.guild_id] = dogeboard
            except QueryError as e:
                log.error(f"Query Errors: {e}")

    @staticmethod
    async def _send_dogeboard_message(message: Message, channel: TextChannel) -> None:
        embed = Embed(
            title=message.author.display_name,
            description=message.content + f"\n\n[Jump to message]({message.jump_url})",
            colour=message.author.colour,
        )
        embed.set_thumbnail(url=message.author.avatar_url)

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

            dogeboard_reaction: Optional[Reaction] = None
            for reaction in message.reactions:

                if reaction.emoji == "✅":
                    if self.bot.user in await reaction.users().flatten():
                        # If the bot has set a checkmark reaction to this message,
                        # it's already been DogeBoarded
                        return

                elif str(reaction.emoji) == str(payload.emoji):
                    dogeboard_reaction = reaction

            if dogeboard_reaction:
                if dogeboard_reaction.count >= dogeboard_data.dogeboard_reactions_required:
                    dogeboard_channel = self.bot.get_channel(dogeboard_data.dogeboard_id)
                    await self._send_dogeboard_message(message, dogeboard_channel)

    @group(brief="Collate the best message of the server using reactions")
    async def dogeboard(self, ctx: Context) -> None:
        """Command group for DogeBoard."""
        if not ctx.subcommand_passed:
            dogeboard_data = await self._get_guild_data(ctx.guild.id)
            embed = Embed(title="DogeBoard", color=Color.blurple())

            if not dogeboard_data:
                embed.description = "DogeBoard is not configured, " \
                                    "use `.dogeboard channel <channel>` to start."
            else:
                embed.add_field(name="Emoji", value=dogeboard_data.dogeboard_emoji)
                embed.add_field(
                    name="Channel",
                    value=ctx.guild.get_channel(dogeboard_data.dogeboard_id).mention
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
            return

        reaction_msg = await ctx.send(content="> React with the new dogeboard_emoji")

        def check(reaction: Reaction, member: Member) -> bool:
            return member == ctx.author and reaction_msg == reaction.message

        try:
            reaction, member = await self.bot.wait_for("reaction_add", check=check, timeout=60)
        except asyncio.TimeoutError:
            return await reaction_msg.edit(content="> You didn't react, Canceling dogeboard_emoji change.")
        finally:
            await reaction_msg.delete(delay=10)

        # Default Emoji or Guild dogeboard_emoji
        if not reaction.custom_emoji or reaction.emoji in ctx.guild.emojis:
            dogeboard_data.dogeboard_emoji = reaction.emoji
        else:
            await ctx.send("> Please react with a default or guild dogeboard_emoji.")
            return None

        await ctx.send(f"> Updated your emoji to {dogeboard_data.dogeboard_emoji}")
        await self._update_guild_data(dogeboard_data)

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


def setup(bot: Friendo) -> None:
    """Adding the help cog."""
    if not settings.FRIENDO_API_USER:
        raise EnvironmentError("Missing environment variable: FRIENDO_API_USER")
    if not settings.FRIENDO_API_PASS:
        raise EnvironmentError("Missing environment variable: FRIENDO_API_PASS")

    bot.add_cog(DogeBoard(bot))
