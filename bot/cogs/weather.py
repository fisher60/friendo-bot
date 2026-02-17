"""Commands for the weather module."""

import aiohttp
import discord
from discord.ext import commands

from bot.settings import WEATHER_TOKEN


class Weather(commands.Cog):
    """commands for the weather finder."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(brief="Takes in a city name and returns the weather for that location")
    async def weather(self, ctx: commands.context.Context, *, args: str = "") -> None:
        """Weather command takes in a city name and sends embed."""
        if not args:
            description = "This should be done like `.weather city name`"
            await ctx.send(embed=discord.Embed(title="Please give a city name", description=description))
        else:
            try:
                embed = discord.Embed(title=f"Weather in {args}")

                url = "http://api.openweathermap.org/data/2.5/weather?q="

                imperial_url = f"{url}{args}&appid={WEATHER_TOKEN}&units=imperial"
                metric_url = f"{url}{args}&appid={WEATHER_TOKEN}&units=metric"

                async with aiohttp.ClientSession() as session:
                    async with session.get(metric_url) as resp:
                        metric = await resp.json()
                    async with session.get(imperial_url) as resp:
                        data = await resp.json()

                icon = data["weather"]
                weather = data["main"]
                weather_m = metric["main"]

                temp_f = weather["temp"]
                temp_ft = weather["feels_like"]
                low_f = weather["temp_min"]
                high_f = weather["temp_max"]
                wind_m = data["wind"]["speed"]

                temp_c = weather_m["temp"]
                temp_fc = weather_m["feels_like"]
                low_c = weather_m["temp_min"]
                high_c = weather_m["temp_max"]
                wind_k = metric["wind"]["speed"]

                for f in icon:
                    icon = f["icon"]
                    main = f["main"]
                    description = f["description"]

                img_url = f"http://openweathermap.org/img/wn/{icon}@4x.png"
                args = args.replace("%20", " ")
                embed.set_thumbnail(url=img_url)
                fields = [
                    ("Status", f"{main}\n{description}", False),
                    ("Current Temp", f"{temp_f!s}F ({temp_c!s}C)", False),
                    ("Feels Like", f"{temp_ft!s}F ({temp_fc!s}'C)", True),
                    (
                        "High Temp",
                        f"{high_f!s}F ({high_c!s}C)",
                        True,
                    ),
                    ("Low Temp", f"{low_f!s}F ({low_c!s}C)", True),
                    ("Wind Speed", f"{wind_m!s}MPH ({wind_k!s}KPH)", False),
                ]

                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)

                await ctx.send(embed=embed)
            except KeyError:
                await ctx.send(embed=discord.Embed(title=f"{args} is an invalid city name"))


async def setup(bot: commands.Bot) -> None:
    """Sets up the cog."""
    await bot.add_cog(Weather(bot))
