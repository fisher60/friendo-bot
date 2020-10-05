"""Commands for the weather module"""
import discord
from discord.ext import commands
import json
import urllib.request




class WeatherCog(commands.Cog):
    """commands for the weather finder"""
    def __init__(self, bot):
        self.bot = bot

    #Weather command, takes in an arg of city name
    @commands.command(brief="Takes in a city name and returns the weather for that location")
    async def weather(self,ctx, *,args):
      embed=discord.Embed(title='Weather in '+args)

      args=args.replace(' ','%20')
      imperialURL = "http://api.openweathermap.org/data/2.5/weather?q="+args+ "&appid=00389432347e0b586478c8709f381c00&units=imperial"
      metricURL = "http://api.openweathermap.org/data/2.5/weather?q="+args+ "&appid=00389432347e0b586478c8709f381c00&units=metric"
      imperial = urllib.request.urlopen(imperialURL)
      metric = urllib.request.urlopen(metricURL) 
      
      data = json.load(imperial)
      metric=json.load(metric)
      icon = data['weather']
      weather = data['main']
      weatherM=metric['main']

      tempF = weather['temp']
      tempFT = weather['feels_like']
      lowF = weather['temp_min']
      highF = weather['temp_max']
      windM = data['wind']['speed']
      
      tempC = weatherM['temp']
      tempCT = weatherM['feels_like']
      lowC = weatherM['temp_min']
      highC = weatherM['temp_max']
      windK = metric['wind']['speed']

      for f in icon:
          icon = f['icon']
          main = f['main']
          description = f['description']

      imgUrl= 'http://openweathermap.org/img/wn/'+icon+'@4x.png'
      args=args.replace('%20',' ')
      embed.set_thumbnail(url=imgUrl)
      embed.add_field(name='Status',value=main+
      '\n'+description,inline=False)
      embed.add_field(name='Current Temp',value=str(tempF)+'F ('+str(tempC)+'C)',inline=False)
      embed.add_field(name='Feels Like',value=str(tempFT)+'F ('+str(tempCT)+'C)')
      embed.add_field(name='High Temp',value=str(highF)+'F ('+str(highC)+'C)')
      embed.add_field(name='Low Temp',value=str(lowF)+'F ('+str(lowC)+'C)')
      embed.add_field(name='Wind Speed',value=str(windM)+'MPH ('+str(windK)+'KPH)',inline=False)
      

      await ctx.send(embed=embed)
    


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    """sets up the cog"""
    bot.add_cog(WeatherCog(bot))
