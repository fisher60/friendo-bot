from . import settings
from bot.bot import Friendo

if __name__ == "__main__":
    bot = Friendo(command_prefix=settings.COMMAND_PREFIX, help_command=None)

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

    # load in Todo List command
    bot.load_extension("bot.cogs.todo_list")

    # load covid stats
    bot.load_extension("bot.cogs.covid_stats")

    bot.run(settings.TOKEN)
