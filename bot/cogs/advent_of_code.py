from bot.bot import Friendo
from discord import errors
from discord.ext.commands import Cog, Context, group
from bot.settings import AOC_LEADERBOARD_LINK, AOC_JOIN_CODE, AOC_SESSION_COOKIE


class AdventOfCode(Cog):
    """Cog for AOC 2020 for small features."""

    def __init__(self, bot: Friendo):
        self.bot = bot

    @staticmethod
    def sort_stats(stat_d: dict) -> dict:
        """Staticmethod for making a sorted dictionary of the leaderboard."""
        stats = dict()
        for ms in stat_d['members']:
            if stat_d['members'][ms]['name'] is None:
                stat_d['members'][ms]['name'] = 'Anonymous'
            stats.update({(stat_d['members'][ms]['name'],
                         stat_d['members'][ms]['stars']): stat_d['members'][ms]['local_score']})

        stats = {k: stats[k] for k in sorted(stats, key=lambda y: stats[y])[::-1]}
        return stats

    @group(name="AdventofCode",
           aliases=('aoc', 'aoc2020'),
           brief="Small commands for AoC 2020",
           usage=".aoc [command]")
    async def aoc_group(self, ctx: Context) -> None:
        """Group for advent of code commands."""
        if not ctx.invoked_subcommand:
            await ctx.send("Please enter a valid command")

    @aoc_group.command(brief="Get the leaderboard join code in your DM's",
                       usage=".aoc join",
                       aliases=("join", "join_lb", "j"))
    async def join_leaderboard(self, ctx: Context) -> None:
        """Dms the author the join code and link for the leaderboard."""
        info = [
            "To join our leaderboard, follow these steps:",
            "• Log in on https://adventofcode.com",
            "• Head over to https://adventofcode.com/leaderboard/private",
            f"• Use this code `{AOC_JOIN_CODE}` to join the Code Collective leaderboard!"]
        error_msg = f":x: {ctx.author.mention}, please (temporarily) enable DMs to receive the join code"

        await ctx.message.add_reaction("📨")
        try:
            await ctx.author.send('\n'.join(info))
        except errors.Forbidden:
            await ctx.send(error_msg)

    @aoc_group.command(brief="Get the leaderboard of AoC 2020 for the Code Collective server",
                       usage=".aoc leaderboard",
                       aliases=('lb', 'board'))
    async def leaderboard(self, ctx: Context) -> None:
        """Shows the leaderboard of code collective server for AoC 2020."""
        async with ctx.channel.typing():
            async with self.bot.session.get(AOC_LEADERBOARD_LINK, cookies={'session': AOC_SESSION_COOKIE}) as stats:
                stats = await stats.json()
                sorted_stats = self.sort_stats(stats)
                msg = []
                count = 1

                for name_star, score in sorted_stats.items():
                    msg.append(
                        f"{count} | {name_star[0] + ' '*(16-len(name_star[0]))} "
                        f"|  {name_star[1]} ★  |   {score}")
                    count += 1

                msg = '\n'.join(msg)
                await ctx.send("🎄 Advent of Code 2020 leaderboard for Code Collective 🎄")
                await ctx.send(f"```  | Name {' '*(16-4)}| Stars | Score\n{msg}```")


def setup(bot: Friendo) -> None:
    """Sets up the AdventOfCode cog."""
    bot.add_cog(AdventOfCode(bot))
