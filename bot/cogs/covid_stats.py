import re
from typing import TYPE_CHECKING

from discord import Colour, Embed
from discord.ext.commands import Cog, Context, command

if TYPE_CHECKING:
    from bot.bot import Friendo

COVID_URL = "https://api.covid19api.com/summary"


class CovidStats(Cog):
    """Show COVID Stats around the world."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

    @command(name="globalcovid", brief="Global Summary COVID19 Stats.")
    async def covid_global_summary(self, ctx: Context) -> None:
        """Shows Summarized Global COVID19 Stats."""
        summary = await self.covid_global_stats()
        embed_msg = Embed(
            title="COVID19 GLOBAL SUMMARY :globe_with_meridians:",
            description=summary,
            color=Colour.blue(),
        )
        await ctx.send(embed=embed_msg)

    @command(
        brief="Choose a country's COVID19 stats. `.covid_stats [slug | country code | country name]`",
        aliases=("covidstats", "covid", "coronavirus", "covid19", "covid-19"),
    )
    async def covid_stats(self, ctx: Context, country: str) -> None:
        """Shows a summary COVID19 stats of a specific country."""
        country_stats = await self.covid_country_stats(country=country)

        if country_stats:
            embed_msg = Embed(
                title=f"COVID19 {country.title()} SUMMARY :globe_with_meridians:",
                description=country_stats,
                color=Colour.green(),
            )

        else:
            embed_msg = Embed(
                title="No data received from website. Please check to see if your arguments are correct.",
                description="Use `.help CovidStats` to see how the commands work.",
                color=Colour.red(),
            )

        await ctx.send(embed=embed_msg)

    async def covid_global_stats(self) -> str:
        """Acquires Covid statistics for the entire planet of Earth."""
        async with self.bot.session.get(COVID_URL) as stats:
            covid_summary = await stats.json()

            return "\n".join(
                f"{' '.join(re.findall('[A-Z][^A-Z]*', key))}: {value:,.0f}"
                for key, value in covid_summary["Global"].items()
            )

    async def covid_country_stats(self, country: str) -> str:
        """Acquires Covid statistics about a specific country."""
        async with self.bot.session.get(COVID_URL) as resp:
            resp.raise_for_status()
            read = (await resp.json())["Countries"]

            data = []
            for _ in read:
                if (
                    country.lower() == _["Country"].lower()
                    or country.lower() == _["Slug"].lower()
                    or country.lower() == _["CountryCode"].lower()
                ):
                    for key, value in _.items():
                        if isinstance(value, int):
                            data.append(f"{' '.join(re.findall('[A-Z][^A-Z]*', key))}: {value:,.0f}")
                        elif isinstance(value, str):
                            data.append(f"{' '.join(re.findall('[A-Z][^A-Z]*', key))}: {value}")
                        else:
                            continue
                    break

            return "\n".join(data)


async def setup(bot: Friendo) -> None:
    """Load the CovidStats cog."""
    await bot.add_cog(CovidStats(bot))
