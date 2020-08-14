import json
import re
from bot.settings import BASE_DIR
from discord.ext.commands import Bot, Cog, command, check


def is_admin():
    """
        returns whether or not the user invoking a command is an admin
    """

    def predicate(ctx):
        with open(f"{BASE_DIR}/save_data.JSON", "r") as data:
            save_data = json.load(data)
        return str(ctx.message.author.id) in save_data["admins"]
    
    return check(predicate)


def id_from_mention(messagecontent: str):
    pattern = r'\d{18}'
    id = re.search(pattern, messagecontent)
    if id is not None:
        return int(id.group())
    else:
        return None


class AdminCommands(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @command(brief="Kills your friend")
    @is_admin()
    async def shutdown(self, ctx):
        msg = f"Mr. Stark, I don't feel so good. . ."
        await ctx.send(msg)
        print("Closing Client...")
        await self.bot.logout()

    @command(name="createadmin")
    @is_admin()
    async def create_admin(self, ctx, user):
        msg = f"Could not create admin from {user}"

        with open(f"{BASE_DIR}/save_data.JSON", "r") as data:
            save_data = json.load(data)

        this_user = self.bot.get_user(id_from_mention(ctx.message.content))

        if this_user and str(this_user.id) not in save_data["admins"]:
            save_data["admins"].append(str(this_user.id))
            with open(f"{BASE_DIR}/save_data.JSON", "w") as file:
                json.dump(save_data, file)
                msg = f"{ctx.author.mention}, {user} added to admins"

        await ctx.send(msg)

        



def setup(bot: Bot) -> None:
    """Load the Admin cog."""
    bot.add_cog(AdminCommands(bot))