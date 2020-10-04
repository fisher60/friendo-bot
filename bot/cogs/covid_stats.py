from discord.ext.commands import Bot, Cog, command
from bot.settings import BASE_DIR
from discord import Embed, Colour
from asyncio import sleep
from discord.ext import tasks
import aiohttp
import json
import re

url = 'https://api.covid19api.com/summary'  # Source data


# async def covid_stats():  # template I made
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as stats:
#             print(stats.status)
#             covid_summary = await stats.text()
#             print('\n'.join(f"{' '.join(re.findall('[A-Z][^A-Z]*', key))}: {value}" for key, value in
#                             json.loads(covid_summary)['Global'].items()))
#
#
# def main():
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(covid_stats())
#     loop.close()
#
#
# if __name__ == '__main__':
#     main()

class CovidStats(Cog):
    """Show COVID Stats around the world"""

    def __init__(self, bot: Bot):
        self.bot = bot

        self.summary_tasks = {}

    async def covid_stats_wrapper(self, ctx, task_type="covidstats"):