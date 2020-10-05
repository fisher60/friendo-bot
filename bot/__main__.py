"""
Launches the bot, starts the asyncio loop when called.
"""
import discord
from . import settings
from .bot import Bot

if __name__ == "__main__":
    bot = Bot(command_prefix=settings.COMMAND_PREFIX)
    bot.remove_command("help")

    @bot.command(name="help", help="This will be shown")
    async def help(ctx, *, name=None):
        char_repeat = 20
        embed = discord.Embed(
            title=f"{'-' * (char_repeat//2)}Friendo_Bot{'-' * (char_repeat//2)}",
            url="https://github.com/Aravindha1234u/Friendo_Bot",
            color=0x1C1C1C,
        )
        embed.set_thumbnail(
            url="https://images.discordapp.net/avatars/723555941118771262/8f586ecb1f89cec031d00b3a616573ea.png?size=512"
        )

        if name is None:
            cogs = list(bot.cogs.keys())
            field_body = "\n".join(cogs)
            field_body = field_body.strip()

            field_body += (
                "\n\nUsage: `%shelp [Cog | Command]`. Example: `%shelp greetings`"
                % (bot.command_prefix, bot.command_prefix)
            )

            embed.add_field(name="Cogs", value=field_body, inline=False)
        else:
            cog = bot.cogs.get(name.title(), None)

            if cog is None:
                # Check if this is not a command
                command = bot.get_command(name.lower())

                if command is not None:
                    embed.title += "\n" + command.name

                    field_body = (
                        command.description
                        if command.description != ""
                        else (
                            command.brief
                            if command.brief != ""
                            else "This command has no description."
                        )
                    )
                    field_body += "\n" + (
                        "Usage: `" + command.usage + "`"
                        if command.usage is not None
                        else ""
                    )

                    embed.add_field(
                        name=command.name, value=field_body.strip(), inline=False
                    )
                else:
                    field_body = (
                        "Error: Cog or command `%s` not found! Use `%shelp` to see a list of cogs"
                        % (name, bot.command_prefix)
                    )
                    embed.add_field(name="Cogs", value=field_body, inline=False)
            else:
                embed.title += "\n" + name.title()

                for command in cog.get_commands():
                    field_body = (
                        (command.brief if command.brief is not None else "")
                        + "\n"
                        + (
                            "Usage: `" + command.usage + "`"
                            if command.usage is not None
                            else ""
                        )
                    )
                    field_body = field_body.strip()

                    embed.add_field(
                        name=command.name,
                        value=(
                            field_body + "\n"
                            if field_body != ""
                            else "This command has no help message"
                        ),
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
    
    #load in music search commands
    bot.load_extension("bot.cogs.LastFM")

    # load in Fun commands
    bot.load_extension("bot.cogs.fun")

    # load in Event command
    bot.load_extension("bot.cogs.events")

    # load in Todo List command
    bot.load_extension("bot.cogs.todo_list")

    bot.run(settings.TOKEN)
