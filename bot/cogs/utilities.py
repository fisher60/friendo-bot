import datetime
from asyncio import sleep
from discord.ext import tasks
from discord.ext.commands import Bot, Cog, command
from discord.utils import sleep_until
from bot import settings


def convert_time(time, period):
    result = None
    try:
        time = int(time)
        if "sec" in period:
            result = time
        elif "min" in period:
            result = time * 60
        elif "hour" in period:
            result = time * (60**2)
    except ValueError:
        pass
    return result

# def convert_time(time, period):
#     result = None
#     try:
#         time = int(time)
#         if "sec" in period:
#             result = datetime.timedelta(seconds=time)
#         elif "min" in period:
#             result = datetime.timedelta(seconds=time * 60)
#         elif "hour" in period:
#             result = datetime.timedelta(seconds=time * (60**2))
#     except ValueError:
#         pass
#     return datetime.datetime.now() + result



class Utilities(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.index = 0

    async def reminder_wrapper(self, time, period, ctx, msg="Reminder!"):

        @tasks.loop(count=1)
        async def create_reminder():
            seconds = convert_time(time, period)
            if not seconds:
                msg = "Please enter a valid time and period (i.e .reminder 5 minutes)"
                await ctx.send(msg)
                return msg
            else:
                await sleep(seconds)
            return

        @create_reminder.after_loop
        async def after_create_reminder():
            await ctx.send(msg)

        create_reminder.start()

    # async def create_reminder(self, ctx, time, period, msg="Reminder!"):
    #     await sleep_until(convert_time(time, period), await ctx.send(msg))


    @command()
    async def version(self, ctx):
        msg = f"Version is {settings.VERSION}"
        await ctx.send(msg)
        return msg

    @command()
    async def reminder(self, ctx, time, period="minutes"):
        await self.reminder_wrapper(ctx=ctx, time=time, period=period)
        return


def setup(bot: Bot) -> None:
    """Load the Help cog."""
    bot.add_cog(Utilities(bot))