import datetime

from typing import Union
from dateutil.relativedelta import relativedelta
from discord import ActivityType, Embed, Member, Spotify, Status
from discord.ext.commands import Cog, Context, MemberConverter, MemberNotFound, command

from bot.bot import Friendo

# Dictionaries for the emojis in userinfo embed
BADGES = {'hypesquad_bravery': '<:bravery:785001148453093386>',
          'hypesquad_brilliance': '<:brilliance:785001159864614933>',
          'hypesquad_balance': '<:balance:785001135676194856>',
          'nitro': '<:nitro:785001224302362624>',
          'verified_bot_developer': '<:dev:785001175820271657>',
          'partner': '<:partner:785001265733566524>',
          'early_supporter': '<:early:785001210599047199>'}

STATUSES = {Status.online: '<:online:785001253133484042>',
            Status.offline: '<:offline:785001240621744149>',
            Status.idle: '<:idle:785001811081035777>',
            Status.dnd: '<:dnd:785001198159527958>'}

ACTIVITIES = {ActivityType.playing: ':video_game: Playing ',
              ActivityType.listening: ':headphones: Listening to ',
              ActivityType.streaming: ':desktop: Streaming on ',
              ActivityType.custom: ''}


class User(Cog):
    """Command to get user info."""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot

    @staticmethod
    async def get_member(ctx: Context, member: str) -> Member:
        """Manually convert string to Member, allows us to catch MemberNotFound if the member is invalid."""
        return await MemberConverter().convert(ctx, member)

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

    @command(brief="Get the info on the user specified, defaults to the command author",
             usage=".userinfo [user (optional)]",
             aliases=('ui', 'user', 'useri', 'uinfo'))
    async def userinfo(self, ctx: Context, member: Union[str, Member] = None) -> None:
        """Shows an embed containing basic info on the user."""
        if not member:
            user = ctx.author
        else:
            try:
                user = await self.get_member(ctx, member)
            except MemberNotFound:
                error_embed = Embed(
                    title="User not found",
                    description=f"No User `{member}` could be found in {ctx.guild}"
                )

                await ctx.send(embed=error_embed)
                return

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
    """Load the User cog."""
    bot.add_cog(User(bot))
