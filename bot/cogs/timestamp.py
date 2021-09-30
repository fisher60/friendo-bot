from discord.ext.commands import Bot, Cog, Context, command, group


class TimestampGeneration(Cog):
    """Commands for generating timestamps for a user."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @group(
        name="timestamp",
        aliases=("t", "ts", "time"),
        brief="Commands for generating discord timestamps."

    )
    async def timestamp_group(self, ctx: Context) -> None:
        """Base group for generating timestamps"""
        pass

    @timestamp_group.command(
        name="generate",
        aliases=("create", "g", "c"),
        brief=(
                "Create a Discord timestamp from a valid time input.\n",
                "Use ISO date format YYYY-MM-DD or YYYYMMDD"
        )
    )
    async def generate_timestamp(self, ctx: Context) -> None:
        """Given a valid timestamp format, create and send a discord timestamp."""
        pass

    @timestamp_group.command(
        name="raw",
        aliases=("raw", "r"),
        brief="Create the raw text for a Discord timestamp and send it in a codeblock"
    )
    async def generate_raw_timestamp(self, ctx: Context) -> None:
        """Given a valid timestamp format, create and send a discord timestamp in a codeblock."""
        pass

    @timestamp_group.command(
        name="samples",
        aliases=("sample", "example", "list", "l", "formats"),
        brief="A list of example input and output timestamps"
    )
    async def sample_timestamps(self, ctx: Context) -> None:
        """Sends multiple input examples along with their outputs for generating a timestamp."""
        pass

    @timestamp_group.command(
        name="user",
        aliases=("u", "me", "creation", "account"),
        brief="Get the invoking user's creation date as a timestamp."
    )
    async def user_creation_time(self, ctx: Context) -> None:
        """Sends the timestamp for the creation time on the invoking user's account."""
        pass


def setup(bot: Bot) -> None:
    """Load the Timestamp cog."""
    bot.add_cog(TimestampGeneration(bot))
