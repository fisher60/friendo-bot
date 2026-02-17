from discord import Colour, Embed
from discord.ext import commands as comms

from bot import settings

SourceType = comms.HelpCommand | comms.Command | comms.Cog | str | comms.ExtensionNotLoaded


class SourceConverter(comms.Converter):
    """Convert an argument into a help command, tag, command, or cog."""

    async def convert(self, ctx: comms.Context, argument: str) -> SourceType:
        """Convert argument into source object."""
        if argument.lower().startswith("help"):
            return ctx.bot.help_command

        cog = ctx.bot.get_cog(argument)
        if cog:
            return cog

        cmd = ctx.bot.get_command(argument)
        if cmd:
            return cmd

        tags_cog = ctx.bot.get_cog("Tags")
        show_tag = True

        if not tags_cog:
            show_tag = False
        elif argument.lower() in tags_cog._cache:  # noqa: SLF001
            return argument.lower()

        msg = f"Unable to convert `{argument}` to valid command{', tag,' if show_tag else ''} or Cog."
        raise comms.BadArgument(msg)


class Source(comms.Cog):
    """Command to send the source (github repo) of a command."""

    def __init__(self, bot: comms.Bot) -> None:
        self.bot = bot

    @comms.command(name="source", brief="Send a link to Friendo's GitHub repo")
    async def send_source(self, ctx: comms.Context, arg1: str | None = None) -> None:
        """Send the source url in an embed."""
        src_conv = SourceConverter()
        if arg1:
            try:
                src_obj = await src_conv.convert(ctx, arg1)
                embed = Embed(
                    title="Friendo's GitHub Repo",
                    colour=Colour.blue(),
                    description=f"Description: {src_obj.brief}",
                )
                embed.add_field(
                    name="Repository",
                    value=f"[Go To GitHub]({settings.GITHUB_REPO})",
                )
                await ctx.send(embed=embed)
            except comms.BadArgument:
                await ctx.send("That command could not be found.")
        else:
            embed = Embed(title="Friendo's GitHub Repo", colour=Colour.blue())
            embed.add_field(name="Repository", value=f"[Go To GitHub]({settings.GITHUB_REPO})")
            await ctx.send(embed=embed)


async def setup(bot: comms.Bot) -> None:
    """Load the Source cog."""
    await bot.add_cog(Source(bot))
