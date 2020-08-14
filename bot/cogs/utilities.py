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


class Utilities(Cog):

    def __init__(self, bot: Bot):
        self.bot = bot
        self.index = 0
        self.drink_tasks = {}
        self.reminder_tasks = {}

    async def reminder_wrapper(self, time, period, ctx, msg="Reminder!", task_type="reminder", reason=None):

        seconds = convert_time(time, period)

        if task_type == "drink":
            self.drink_tasks[ctx.author.id] += 1
        elif task_type == "reminder":
            self.reminder_tasks[ctx.author.id] += 1

        @tasks.loop(count=1)
        async def create_reminder():
            await sleep(seconds)

        @create_reminder.after_loop
        async def after_create_reminder():
            completion_message = msg
            if task_type == "drink":
                self.drink_tasks[ctx.author.id] -= 1
            elif task_type == "reminder":
                completion_message = f"{ctx.author.mention}, Reminder for: {reason if reason else ''}"
                self.reminder_tasks[ctx.author.id] -= 1
            await ctx.send(completion_message)

        if seconds:
            create_reminder.start()
        else:
            msg = "Please enter a valid time and period (i.e .reminder 5 minutes)"
            await ctx.send(msg)

    @command(brief="Returns Friendo's Version")
    async def version(self, ctx):
        msg = f"Version is {settings.VERSION}"
        await ctx.send(msg)
        return msg

    @command(brief="[number] [unit (seconds/minutes/hours)] [reason for reminder]")
    async def reminder(self, ctx, time, period="minutes", *, reason=None):
        if ctx.author.id not in self.reminder_tasks:
            self.reminder_tasks[ctx.author.id] = 0
        if self.reminder_tasks[ctx.author.id] < 1:
            await self.reminder_wrapper(ctx=ctx, time=time, period=period, task_type="reminder", reason=reason)
            if period in ["second", "seconds", "minute", "minutes", "hour", "hours"]:
                await ctx.send(f"{ctx.author.mention} I will set a reminder for you in {time} {period}")
        return

    @command(brief="Starts a 10 minute drink session to stay hydrated")
    async def drink(self, ctx):
        print(self.drink_tasks)
        if ctx.author.id not in self.drink_tasks:
            self.drink_tasks[ctx.author.id] = 0
        if self.drink_tasks[ctx.author.id] < 1:
            await ctx.send(f"{ctx.author.mention} I got you, mate.")
            base_msg = f"OY! {ctx.author.mention}, drink some water, mate."
            await self.reminder_wrapper(
                ctx=ctx,
                time=5,
                period="minutes",
                msg=base_msg,
                task_type="drink",
                reason="drinking"
            )
            await self.reminder_wrapper(
                ctx=ctx,
                time=10,
                period="minutes",
                msg=base_msg + "\n\nYou can run this command and have another if you'd like.",
                task_type="drink",
                reason="drinking"
            )
        else:
            msg = f"{ctx.author.mention} You are already drinking!"
            await ctx.send(msg)


def setup(bot: Bot) -> None:
    """Load the Utilities cog."""
    bot.add_cog(Utilities(bot))
