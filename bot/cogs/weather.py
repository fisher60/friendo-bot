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
        embed = discord.Embed(title="Weather!")

        args = args.replace(" ", "%20")
        wUrl = (
            "http://api.openweathermap.org/data/2.5/weather?q="
            + args
            + "&appid=00389432347e0b586478c8709f381c00&units=imperial"
        )
        response = urllib.request.urlopen(wUrl)
        data = json.load(response)
        print(data["main"])
        icon = data["weather"]
        weather = data["main"]

        temp = weather["temp"]
        tempT = weather["feels_like"]
        low = weather["temp_min"]
        high = weather["temp_max"]

        for f in icon:
            icon = f["icon"]
            main = f["main"]
            description = f["description"]

        imgUrl = "http://openweathermap.org/img/wn/" + icon + "@4x.png"
        print(imgUrl)
        args = args.replace("%20", " ")
        embed.set_thumbnail(url=imgUrl)
        embed.add_field(name="Status", value=main + "\n" + description, inline=False)
        embed.add_field(name="Current Temp", value=temp, inline=False)
        embed.add_field(name="Feels Like", value=tempT)
        embed.add_field(name="High Temp", value=high)
        embed.add_field(name="Low Temp", value=low)

        await ctx.send(embed=embed)


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    """sets up the cog"""
    bot.add_cog(WeatherCog(bot))
