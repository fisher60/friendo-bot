from discord import Embed, Colour
from discord.ext import commands
from typing import Union
from bot import settings


SourceType = Union[
    commands.HelpCommand,
    commands.Command,
    commands.Cog,
    str,
    commands.ExtensionNotLoaded,
]


class SourceConverter(commands.Converter):
    """Convert an argument into a help command, tag, command, or cog."""

    async def convert(self, ctx: commands.Context, argument: str) -> SourceType:
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
        elif argument.lower() in tags_cog._cache:
            return argument.lower()

        raise commands.BadArgument(
            f"Unable to convert `{argument}` to valid command{', tag,' if show_tag else ''} or Cog."
        )


class Source(commands.Cog):
    """Command to send the source (github repo) of a command."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="source", brief="Send a link to Friendo's GitHub repo")
    async def send_source(self, ctx, arg1=None):
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
                    value=f"[Go To GitHub]({settings.BASE_GITHUB_REPO})",
                )
                await ctx.send(embed=embed)
            except commands.BadArgument:
                await ctx.send("That command could not be found.")
        else:
            embed = Embed(title="Friendo's GitHub Repo", colour=Colour.blue())
            embed.add_field(
                name="Repository", value=f"[Go To GitHub]({settings.BASE_GITHUB_REPO})"
            )
            await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Load the Source cog."""
    bot.add_cog(Source(bot))
