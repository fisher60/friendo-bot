from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING

import yaml
from dateutil.relativedelta import relativedelta
from discord import ActivityType, Embed, Member, Spotify, Status
from discord.ext.commands import Cog, Context, MemberConverter, MemberNotFound, command

if TYPE_CHECKING:
    from bot.bot import Friendo

# Dictionaries for the emojis in userinfo embed

yaml_path = Path.cwd() / "bot" / "resources" / "user_badges.yaml"
with yaml_path.open("r", encoding="utf-8") as f:
    info = yaml.load(f, Loader=yaml.FullLoader)
    BADGES = info[0]


STATUSES = {
    Status.online: "<:online:785001253133484042>",
    Status.offline: "<:offline:785001240621744149>",
    Status.idle: "<:idle:785001811081035777>",
    Status.dnd: "<:dnd:785001198159527958>",
    "spotify": "<:spotify:785113868543852584>",
}

ACTIVITIES = {
    ActivityType.playing: ":video_game: Playing ",
    ActivityType.listening: ":headphones: Listening to ",
    ActivityType.streaming: ":desktop: Streaming on ",
    ActivityType.custom: "",
}


class User(Cog):
    """Command to get user info."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

    @staticmethod
    async def get_member(ctx: Context, member: str) -> Member:
        """Manually convert string to Member, allows us to catch MemberNotFound if the member is invalid."""
        return await MemberConverter().convert(ctx, member)

    @staticmethod
    def get_timedelta(a: datetime, b: datetime) -> list:
        """Static method for getting parsed time delta between 2 datetimes."""
        final = []
        delta = relativedelta(a, b)

        dates = {
            "years": abs(delta.years),
            "months": abs(delta.months),
            "days": abs(delta.days),
            "hours": abs(delta.hours),
            "minutes": abs(delta.minutes),
            "seconds": abs(delta.seconds),
        }

        for k, v in dates.items():
            if v:
                final.append(f"{v} {k}")

        return final[:3]

    @command(
        brief="Get the info on the user specified, defaults to the command author",
        usage=".userinfo [user (optional)]",
        aliases=("ui", "user", "useri", "uinfo"),
    )
    async def userinfo(self, ctx: Context, member: str | Member = None) -> None:
        """Shows an embed containing basic info on the user."""
        if not member:
            user = ctx.author
        else:
            try:
                user = await self.get_member(ctx, member)
            except MemberNotFound:
                error_embed = Embed(
                    title="User not found", description=f"No User `{member}` could be found in {ctx.guild}"
                )

                await ctx.send(embed=error_embed)
                return

        user_badges = []
        roles = []
        statuses = []
        is_bot = "Bot: :x:"

        create_time = ", ".join(self.get_timedelta(datetime.now(UTC), user.created_at))
        joined_time = ", ".join(self.get_timedelta(datetime.now(UTC), user.joined_at))

        flags = user.public_flags

        info_emb = Embed(color=user.color, title=str(user))
        info_emb.set_thumbnail(url=user.avatar)

        user_badges = [BADGES[str(flag_.name)] for flag_ in flags.all() if str(flag_.name) in BADGES]

        if (user.avatar and user.avatar.is_animated()) or user.premium_since:
            user_badges.append(BADGES["nitro"])

        roles = [f"<@&{role.id}>" for role in user.roles[1:]]

        if user.bot or user.id == 196664644113268736:
            is_bot = "Bot: :white_check_mark:"

        statuses.append(f"{STATUSES[user.mobile_status]} Mobile Client")
        statuses.append(f"{STATUSES[user.web_status]} Web Client")
        statuses.append(f"{STATUSES[user.desktop_status]} Desktop Client")

        roles = ", ".join(roles)
        user_badges = " ".join(user_badges)
        statuses = "\n".join(statuses)
        info_emb.description = user_badges
        men, id_, nick = user.mention, user.id, user.nick

        base_activity = user.activities
        if base_activity:
            activities = [ACTIVITIES[i.type] + i.name for i in base_activity if not isinstance(i, Spotify)]
        else:
            activities = ["No activity is being done"]

        for activity in base_activity:
            if isinstance(activity, Spotify):
                activities.append(f"{STATUSES['spotify']} Listening to {activity.title}, {activity.artist}")
                break

        activities = "\n".join(activities)

        user_info = {
            "User Information": f"Created: {create_time} ago\nProfile: {men}\nID: {id_}\n{is_bot}",
            "Guild Profile": f"Joined: {joined_time} ago\nNick: {nick}\nRoles: {roles}",
            "Status": statuses,
            "Activities": activities,
        }

        for k, v in user_info.items():
            info_emb.add_field(name=k, value=v, inline=False)
        await ctx.send(embed=info_emb)


async def setup(bot: Friendo) -> None:
    """Load the User cog."""
    await bot.add_cog(User(bot))
