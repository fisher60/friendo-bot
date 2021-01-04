from asyncio import sleep
from pathlib import Path
import random
import subprocess
from typing import Optional

from discord import Colour, Embed
from discord.ext import tasks
from discord.ext.commands import Cog, Context, command
import yaml

from bot import settings
from bot.bot import Friendo

with open(Path.cwd() / 'bot' / 'resources' / 'list_of_quotes.yaml', 'r', encoding='utf-8') as f:
    lines = yaml.load(f, Loader=yaml.FullLoader)['lines']

# Define the time period units user can pass
VALID_PERIODS = "s sec secs second seconds m min mins minute minutes h hour hours".split()


def convert_time(time: str, period: str) -> Optional[int]:
    """Converts the given time and period (i.e 10 minutes) to seconds."""
    try:
        # Strip at most one trailing s (if the string is not just "s")
        # Using rstrip() would let people enter "sss" which would return ""
        if len(period) > 1 and period[-1] == "s":
            period = period[:-1]

        time = int(time)

        if period in ("s", "sec", "second"):
            return time

        if period in ("m", "min", "minute"):
            return time * 60

        if period in ("h", "hour"):
            return time * (60 ** 2)

    except ValueError:
        pass


class Utilities(Cog):
    """Simple, useful commands that offer some sort of service or benefit to users."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

        self.drink_tasks = {}
        self.reminder_tasks = {}
        self.reminder_limit = 1

    @staticmethod
    async def send_reminder(context: Context,
                            reason: str,
                            time: str,
                            period: str,
                            is_final_reminder: bool = False) -> None:
        """Packs parameters into an embed and sends as a reminder."""
        if is_final_reminder:
            title = f"{context.author}'s reminder"
        else:
            title = f"I will remind {context.author}"
        reminder_embed = Embed(title=title,
                               description=f"For: `{reason}` in `{time}` `{period}`", colour=Colour.blue())
        await context.send(f"{context.author.mention}", embed=reminder_embed)

    async def reminder_wrapper(
            self,
            time: str,
            period: str,
            ctx: Context,
            msg: str = "Reminder!",
            task_type: str = "reminder",
            reason: str = None
    ) -> None:
        """Wrapper function for reminders to allow the task to be created on function call."""
        seconds = convert_time(time, period)

        if task_type == "drink":
            self.drink_tasks[ctx.author.id] += 1
        elif task_type == "reminder":
            self.reminder_tasks[ctx.author.id] += 1

        @tasks.loop(count=1)
        async def create_reminder() -> None:
            """Sets a delay for the reminder to complete."""
            await sleep(seconds)

        @create_reminder.after_loop
        async def after_create_reminder() -> None:
            """
            After the delay is complete, this function will execute.

            Used for both regular reminders and the special 'drink' reminder.
            """
            completion_message = msg
            custom_completion_message = None

            if task_type == "drink":
                if self.drink_tasks[ctx.author.id] > 0:
                    await ctx.send(completion_message)

                self.drink_tasks[ctx.author.id] -= 1

            elif task_type == "reminder":
                custom_completion_message = self.send_reminder(ctx,
                                                               reason,
                                                               time,
                                                               period,
                                                               is_final_reminder=True)

            if self.reminder_tasks[ctx.author.id] > 0:
                self.reminder_tasks[ctx.author.id] -= 1
                if custom_completion_message:
                    await custom_completion_message
                else:
                    await ctx.send(completion_message)

        if seconds:
            create_reminder.start()
        else:
            msg = "Please enter a valid time and period (i.e .reminder 5 minutes)"
            self.reminder_tasks[ctx.author.id] -= 1
            await ctx.send(msg)

    @command(brief="Returns Friendo's Version")
    async def version(self, ctx: Context) -> str:
        """Creates a version number from settings.VERSION and most recent commit hash."""
        commit_hash = (subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode("ascii"))
        msg = f"Version is {settings.VERSION}{commit_hash[-4:]}"

        await ctx.send(msg)

        return msg

    @command(brief="[number] [unit (seconds/minutes/hours)] [reason for reminder]", aliases=["remind"])
    async def reminder(self, ctx: Context, time: str, period: str = "minutes", *, reason: str = None) -> None:
        """Creates a reminder for the user."""
        reason = reason if reason else "nothing"

        if ctx.author.id not in self.reminder_tasks:
            self.reminder_tasks[ctx.author.id] = 0

        if self.reminder_tasks[ctx.author.id] < self.reminder_limit:
            await self.reminder_wrapper(
                ctx=ctx, time=time, period=period, task_type="reminder", reason=reason
            )

            if period in VALID_PERIODS:
                if self.reminder_tasks[ctx.author.id] > 0:
                    await self.send_reminder(ctx, reason, time, period, is_final_reminder=False)
        else:
            await ctx.send(
                f"{ctx.author.mention} you may only have {self.reminder_limit} at a time."
            )

    @command(brief="Starts a 10 minute drink session to stay hydrated")
    async def drink(self, ctx: Context) -> None:
        """Sets multiple reminders for a user to remind them to drink water and pace their drinking."""
        if ctx.author.id not in self.drink_tasks:
            self.drink_tasks[ctx.author.id] = 0

        if self.drink_tasks[ctx.author.id] < 1:
            await ctx.send(f"{ctx.author.mention} I got you, mate.")

            base_msg = f"OY! {ctx.author.mention} drink some water, mate."

            await self.reminder_wrapper(
                ctx=ctx,
                time='5',
                period="minutes",
                msg=base_msg,
                task_type="drink",
                reason="drinking",
            )

            await self.reminder_wrapper(
                ctx=ctx,
                time='10',
                period="minutes",
                msg=base_msg + "\n\nYou can run this command and have another if you'd like.",
                task_type="drink",
                reason="drinking",
            )

        else:
            msg = f"{ctx.author.mention} You are already drinking!"

            await ctx.send(msg)

    @command(brief="Shows the latency between Friendo and the Discord API")
    async def ping(self, ctx: Context) -> None:
        """Sends the ping between the bot and the discord API."""
        await ctx.send(f"Ping is {round(self.bot.latency * 1000)}ms")

    @command(brief="Shows quotes", name="quote")
    async def quotes(self, ctx: Context) -> None:
        """Chooses between a list of quotes."""
        embed_quote = Embed(title=random.choice(lines), color=Colour.green())

        await ctx.send(embed=embed_quote)


def setup(bot: Friendo) -> None:
    """Load the Utilities cog."""
    bot.add_cog(Utilities(bot))
