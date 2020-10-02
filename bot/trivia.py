import discord
from discord.ext import commands


class TriviaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MembersCog(bot))
