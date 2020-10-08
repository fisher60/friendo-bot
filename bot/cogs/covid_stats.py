from discord.ext.commands import Bot, Cog, command
from bot.settings import BASE_DIR
from discord import Embed, Colour
from asyncio import sleep
from discord.ext import tasks
import aiohttp
import asyncio
import json
import re

url_summary = "https://api.covid19api.com/summary"  # Source data


async def covid__global_stats():
    async with aiohttp.ClientSession() as session:
        async with session.get(url_summary) as stats:
            print(stats.status)
            covid_summary = await stats.text()
            return "\n".join(
                f"{' '.join(re.findall('[A-Z][^A-Z]*', key))}: {value:,.0f}"
                for key, value in json.loads(covid_summary)["Global"].items()
            )


async def covid_country_stats(country):
    async with aiohttp.ClientSession() as session:
        async with session.get(url_summary) as stats:
            print(stats.status)
            covid_summary = await stats.text()
            read = json.loads(covid_summary)["Countries"]
            data = []
            for _ in read:
                if (
                    country.lower() == _["Country"].lower()
                    or country.lower() == _["Slug"].lower()
                    or country.lower() == _["CountryCode"].lower()
                ):
                    for key, value in _.items():
                        if isinstance(value, int):
                            data.append(
                                f"{' '.join(re.findall('[A-Z][^A-Z]*', key))}: {value:,.0f}"
                            )
                        elif isinstance(value, str):
                            data.append(
                                f"{' '.join(re.findall('[A-Z][^A-Z]*', key))}: {value}"
                            )
                        else:
                            continue
                    break
            return "\n".join(data)


class CovidStats(Cog):
    """Show COVID Stats around the world"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(brief="Global Summary COVID19 Stats. `.globalcovid`", name="globalcovid")
    async def covid_global_summary(self, ctx):
        """Shows Summarized Global COVID19 Stats"""
        summary = await covid__global_stats()
        embed_msg = Embed(
            title="COVID19 GLOBAL SUMMARY :globe_with_meridians:",
            description=summary,
            color=Colour.blue(),
        )
        await ctx.send(embed=embed_msg)

    @command(
        brief="Choose a country's COVID19 stats. `.covid_stats [slug | country code | country name]`",
        name="covid_stats",
    )
    async def covid_stats(self, ctx, country=None):
        """Shows a summary COVID19 stats of a specific country"""
        if country:
            country_stats = await covid_country_stats(country=country)
            if country_stats:
                embed_msg = Embed(
                    title=f"COVID19 {country.title()} SUMMARY :globe_with_meridians:",
                    description=country_stats,
                    color=Colour.green(),
                )
            else:
                embed_msg = Embed(
                    title="Data is empty. Maybe you have a typo or the country name does not exist.",
                    description="Check if your spelling is correct. Use `.help CovidStats` to see how the commands work.",
                    color=Colour.red(),
                )

        else:
            embed_msg = Embed(
                title="Please try again.",
                description="Use `.help CovidStats` to see how the commands work.",
                color=Colour.red(),
            )

        await ctx.send(embed=embed_msg)


def setup(bot: Bot) -> None:
    """Load the CovidStats cog."""
    bot.add_cog(CovidStats(bot))
