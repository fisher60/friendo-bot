"""
Launches the bot, starts the asyncio loop when called.
"""
from bot.meme_api import memegen
from . import settings
from .bot import Bot
import discord

if __name__ == "__main__":
    bot = Bot(command_prefix=settings.COMMAND_PREFIX)
    bot.remove_command("help")

    @bot.command(name="help", help="This will be shown")
    async def help(ctx):
        embed = discord.Embed(
            title="Friendo_Bot",
            url="https://github.com/Aravindha1234u/Friendo_Bot",
            color=0x1C1C1C,
        )
        embed.set_thumbnail(
            url="https://images.discordapp.net/avatars/723555941118771262/8f586ecb1f89cec031d00b3a616573ea.png?size=512"
        )
        embed.add_field(
            name="Events",
            value='events   Usage: `.events show "[*args]"`',
            inline=False,
        )
        embed.add_field(
            name="Fun",
            value="- 8ball     Ask any question to the 8ball \n- blackjack Play blackjack with the Friendo Bot\n- flip      simulates a coin toss\n- tosponge  Alternate case of inputted text\n- uwu       uwuify any text you like",
            inline=False,
        )
        embed.add_field(name="Greeting", value="hello Say hello", inline=True)
        embed.add_field(
            name="Memes",
            value="meme generator commands. Usage: `.meme [command] [*args]`",
            inline=False,
        )
        embed.add_field(
            name="Segmentation",
            value="segment Send an image and get a segmented one back",
            inline=False,
        )
        embed.add_field(
            name="Utilities",
            value="- drink     Starts a 10 minute drink session to stay hydrated\n- ping      Shows the latency between Friendo and the Discord API\n- reminder  [number] [unit (seconds/minutes/hours)] [reason for reminder]\n- version   Returns Friendo's Version",
            inline=False,
        )
        await ctx.send(embed=embed)

    # load in basic commands
    bot.load_extension("bot.cogs.greetings")
    bot.load_extension("bot.cogs.utilities")
    bot.load_extension("bot.cogs.source")

    # load in image segmentation commands
    bot.load_extension("bot.cogs.image_segmentation")

    # load in Meme commands
    bot.load_extension("bot.cogs.memes")

    # load in Admin commands
    bot.load_extension("bot.cogs.admin")

    # load in Trivia commands
    bot.load_extension("bot.cogs.trivia")

    # load in weather command
    bot.load_extension("bot.cogs.weather")

    # load in Fun commands
    bot.load_extension("bot.cogs.fun")

    # load in randomcase command
    bot.load_extension("bot.cogs.randomcase")

    # load in Event command
    bot.load_extension("bot.cogs.events")

    bot.run(settings.TOKEN)
