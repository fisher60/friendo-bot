import aiohttp
import discord
import os
from io import BytesIO
from urllib import parse
from discord.ext import commands
from bot.settings import APPID


class Wolfram(commands.Cog):
    """command for wolfram search"""
    def __init__(self, bot):
        self.bot = bot
        self.query = "http://api.wolframalpha.com/v2/{request}?{data}"
        

    # wolfram command, takes in a search and gives the result
    # PS, I didn't totally steal it from seasonal bot
    @commands.command(brief="Takes in a wolfram search and displays the result", usage=".wolfram [query]")
    async def wolfram(self, ctx, *, query):

        url_str = parse.urlencode({
            "i": query,
            "appid": APPID,
        })

        query_final = self.query.format(request="simple", data=url_str)

        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(query_final) as response:
                    status = response.status
                    image_bytes = await response.read()

                    image_file = discord.File(BytesIO(image_bytes), filename="image.png")
                    image_url = "attachment://image.png"

                    if status == 501:
                        message = "Failed to get response"
                        footer = ""
                        color = discord.Color.red()
                        
                    elif status == 400:
                        message = "No input found"
                        footer = ""
                                                
                    elif status == 403:
                        message = "Wolfram API key is invalid or missing."
                        footer = ""
                        
                    else:
                        message = ""
                        footer = "View original for a bigger picture."
                        color = discord.Colour.orange()
                                   
                    final_emb = discord.Embed(title=message, color=color)
                    final_emb.set_image(url=image_url)
                    final_emb.set_footer(text=footer)
                    
                    await ctx.send(embed=final_emb, file=image_file)

def setup(bot):
    """sets up the cog"""
    bot.add_cog(Wolfram(bot))
    
