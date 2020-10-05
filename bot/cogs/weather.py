"""Commands for the weather module"""
import discord
from discord.ext import commands
import json
import urllib.request


class WeatherCog(commands.Cog):
    """commands for the weather finder"""

    def __init__(self, bot):
        self.bot = bot

    # Weather command, takes in an arg of city name
    @commands.command(
        brief="Takes in a city name and returns the weather for that location"
    )
    async def weather(self, ctx, *, args):
        embed = discord.Embed(title="Weather in " + args)

        args = args.replace(" ", "%20")
        imperial_url = (
            "http://api.openweathermap.org/data/2.5/weather?q="
            + args
            + "&appid=00389432347e0b586478c8709f381c00&units=imperial"
        )
        metric_url = (
            "http://api.openweathermap.org/data/2.5/weather?q="
            + args
            + "&appid=00389432347e0b586478c8709f381c00&units=metric"
        )
        imperial = urllib.request.urlopen(imperial_url)
        metric = urllib.request.urlopen(metric_url)

        data = json.load(imperial)
        metric = json.load(metric)
        weather_f = data["main"]
        weather_c = metric["main"]

        icon = None
        main = None
        description = None

        for f in data["weather"]:
            icon = f["icon"]
            main = f["main"]
            description = f["description"]

        embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{icon}@4x.png")

        if main and description and icon:
            embed.add_field(
                name="Status", value=main + "\n" + description, inline=False
            )
        else:
            raise ValueError(
                "Api call failed, unable to retrieve 'icon,' 'main,' or 'description'"
            )
        embed.add_field(
            name="Current Temp",
            value=str(weather_f["temp"]) + "F (" + str(weather_c["temp"]) + "C)",
            inline=False,
        )
        embed.add_field(
            name="Feels Like",
            value=str(weather_f["feels_like"])
            + "F ("
            + str(weather_c["feels_like"])
            + "C)",
        )
        embed.add_field(
            name="High Temp",
            value=str(weather_f["temp_max"])
            + "F ("
            + str(weather_c["temp_max"])
            + "C)",
        )
        embed.add_field(
            name="Low Temp",
            value=str(weather_f["temp_min"])
            + "F ("
            + str(weather_c["temp_min"])
            + "C)",
        )
        embed.add_field(
            name="Wind Speed",
            value=str(data["wind"]["speed"])
            + "MPH ("
            + str(metric["wind"]["speed"])
            + "KPH)",
            inline=False,
        )

        await ctx.send(embed=embed)


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    """sets up the cog"""
    bot.add_cog(WeatherCog(bot))
