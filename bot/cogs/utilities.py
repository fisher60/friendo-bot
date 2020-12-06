from asyncio import sleep
from pathlib import Path
import random
import subprocess
import datetime
from typing import Optional

from discord import ActivityType, Colour, Embed, Member, Spotify, Status
from discord.ext import tasks
from discord.ext.commands import Cog, Context, command
import yaml

from bot import settings
from bot.bot import Friendo
from dateutil.relativedelta import relativedelta

with open(Path.cwd() / 'bot' / 'resources' / 'list_of_quotes.yaml', 'r', encoding='utf-8') as f:
    lines = yaml.load(f, Loader=yaml.FullLoader)['lines']

# Define the time period units user can pass
VALID_PERIODS = "s sec secs second seconds m min mins minute minutes h hour hours".split()

# Dictionaries for the emojis in userinfo embed
BADGES = {'hypesquad_bravery': '<:bravery:784430728683323392>',
          'hypesquad_brilliance': '<:brilliance:784430705118806036>',
          'hypesquad_balance': '<:balance:784430681857720332>',
          'nitro': '<:nitro:784751384780079134>',
          'verified_bot_developer': '<:dev:784755774781390849>',
          'partner': '<:partner:784756644634034176>',
          'early_supporter': '<:early:784756624509108224>'}

STATUSES = {Status.online: '<:online:782636673653407744>',
            Status.offline: '<:offline:782636856075616286>',
            Status.idle: '<:3929_idle:782638272483950623>',
            Status.dnd: '<:dnd:782637101464027136>'}

ACTIVITIES = {ActivityType.playing: ':video_game: Playing ',
              ActivityType.listening: ':headphones: Listening to ',
              ActivityType.streaming: ':desktop: Streaming on '}


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
    def get_timedelta(a: datetime.datetime, b: datetime.datetime) -> list:
        """Static method for getting parsed time delta between 2 datetimes."""
        final = []
        delta = relativedelta(a, b)
        years = abs(delta.years)
        months = abs(delta.months)
        days = abs(delta.days)
        hours = abs(delta.hours)
        minutes = abs(delta.minutes)

        if minutes and not months and not years:
            final.append(f'{minutes} minutes')

        if hours:
            final.append(f'{hours} hours')

        if days:
            final.append(f'{days} days')

        if months:
            final.append(f'{months} months')

        if years:
            final.append(f'{years} years')
        final = final[::-1]

        return final[:3]

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

            if task_type == "drink":
                if self.drink_tasks[ctx.author.id] > 0:
                    await ctx.send(completion_message)

                self.drink_tasks[ctx.author.id] -= 1

            elif task_type == "reminder":
                completion_message = (
                    f"{ctx.author.mention}, Reminder for: {reason if reason else ''}"
                )

            if self.reminder_tasks[ctx.author.id] > 0:
                self.reminder_tasks[ctx.author.id] -= 1
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

    @command(brief="[number] [unit (seconds/minutes/hours)] [reason for reminder]")
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
                    await ctx.send(
                        f"{ctx.author.mention} I will remind you about {reason} in {time} {period}"
                    )
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

    @command(brief="Get the info on the user specified, defaults to the command author",
             usage=".userinfo [user (optional)]",
             aliases=('ui', 'user', 'useri', 'uinfo'))
    async def userinfo(self, ctx: Context, user: Member = None) -> None:
        """Shows an embed containing basic info on the user."""
        user = ctx.author if not user else user
        spotify_emoji = '<:spotify:785113868543852584>'
        user_badges = []
        roles = []
        statuses = []
        is_bot = "Bot: :x:"

        create_time = ', '.join(self.get_timedelta(datetime.datetime.utcnow(), user.created_at))
        joined_time = ', '.join(self.get_timedelta(datetime.datetime.utcnow(), user.joined_at))

        flags = user.public_flags

        info_emb = Embed(color=user.color,
                         title=str(user))
        info_emb.set_thumbnail(url=user.avatar_url)

        for flag_ in flags.all():
            if str(flag_.name) in BADGES:
                user_badges.append(BADGES[str(flag_.name)])

        if user.is_avatar_animated():
            user_badges.append(BADGES['nitro'])

        for role in user.roles[1:]:
            roles.append(f"<@&{role.id}>")

        if user.bot:
            is_bot = "Bot: :white_check_mark:"

        statuses.append(f"{STATUSES[user.mobile_status]} Mobile Client")
        statuses.append(f"{STATUSES[user.web_status]} Web Client")
        statuses.append(f"{STATUSES[user.desktop_status]} Desktop Client")

        roles = ', '.join(roles)
        user_badges = " ".join(user_badges)
        statuses = '\n'.join(statuses)
        info_emb.description = user_badges
        men, id_, nick = user.mention, user.id, user.nick

        base_activity = user.activity
        if base_activity:
            activity = ACTIVITIES[base_activity.type] + base_activity.name
        else:
            activity = "No activity is being done"

        if isinstance(base_activity, Spotify):
            activity = "\n".join([f'{spotify_emoji} {activity[12:]}',
                                  f"**Song**: {base_activity.title}",
                                  f"**Artist**: {base_activity.artist}",
                                  f"**Album**: {base_activity.album}"])

        info_emb.add_field(name='User Information',
                           value=f"Created: {create_time} ago\nProfile: {men}\nID: {id_}\n{is_bot}",
                           inline=False)
        info_emb.add_field(name="Guild Profile",
                           value=f"Joined: {joined_time} ago\nNick: {nick}\nRoles: {roles}",
                           inline=False)
        info_emb.add_field(name="Status",
                           value=statuses,
                           inline=False)
        info_emb.add_field(name="Activity",
                           value=activity,
                           inline=False)

        await ctx.send(embed=info_emb)


def setup(bot: Friendo) -> None:
    """Load the Utilities cog."""
    bot.add_cog(Utilities(bot))
