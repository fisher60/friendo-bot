"""Commands for the weather module."""
import aiohttp
import discord

from discord.ext import commands

from bot.settings import WEATHER_TOKEN
from discord.ext import commands
import aiohttp
from bot.settings import WEATHER_TOKEN


class Weather(commands.Cog, name='weather'):
    """commands for the weather finder."""

    def __init__(self, bot: discord.ext.commands.bot.Bot):
        self.bot = bot

    @commands.command(
        brief="Takes in a city name and returns the weather for that location")
    async def weather(self, ctx: discord.ext.commands.context.Context, *, args: str) -> None:
        """Weather command takes in a city name and sends embed."""
        embed = discord.Embed(title=f"Weather in {args}")
        url = "http://api.openweathermap.org/data/2.5/weather?q="
        args = args.replace(' ', '%20')
        imperial_url = f"{url}{args}&appid={WEATHER_TOKEN}&units=imperial"
        metric_url = f"{url}{args}&appid={WEATHER_TOKEN}&units=metric"
        async with aiohttp.ClientSession() as session:
            async with session.get(metric_url) as resp:
                metric = await resp.json()
        async with aiohttp.ClientSession() as session:
            async with session.get(imperial_url) as resp:
                data = await resp.json()

        icon = data['weather']
        weather = data['main']
        weather_m = metric['main']

        temp_f = weather['temp']
        temp_ft = weather['feels_like']
        low_f = weather['temp_min']
        high_f = weather['temp_max']
        wind_m = data['wind']['speed']

        temp_c = weather_m['temp']
        temp_fc = weather_m['feels_like']
        low_c = weather_m['temp_min']
        high_c = weather_m['temp_max']
        wind_k = metric['wind']['speed']

        for f in icon:
            icon = f['icon']
            main = f['main']
            description = f['description']

        img_url = f"http://openweathermap.org/img/wn/{icon}@4x.png"
        args = args.replace('%20', ' ')
        embed.set_thumbnail(url=img_url)
        fields = [
            (
                "Status",
                f"{main}\n{description}",
                False
            ),
            (
                'Current Temp',
                f"{str(temp_f)}F ({str(temp_c)}C)",
                False
            ),
            (
                'Current Temp',
                f"{str(temp_f)}F ({str(temp_c)}C)",
                False
            ),
            (
                'Current Temp',
                f"{str(temp_f)}F ({str(temp_c)}C)",
                False
            ),
            (
                'Feels Like',
                f"{str(temp_ft)}F ({str(temp_fc)}'C)",
                True
            ),
            (
                'High Temp',
                f"{str(high_f)}F ({str(high_c)}C)",
                True,
            ),
            (
                'Low Temp',
                f"{str(low_f)}F ({str(low_c)}C)",
                True
            ),
            (
                'Wind Speed',
                f"{str(wind_m)}MPH ({str(wind_k)}KPH)",
                False
            )
        ]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)


def setup(bot: discord.ext.commands.bot.Bot) -> None:
    """Sets up the cog."""
    bot.add_cog(Weather(bot))
