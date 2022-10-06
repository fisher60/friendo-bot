import random
import yaml
from pathlib import Path
from discord.ext.commands import Bot, Cog, Context, command

with open(Path.cwd() / 'bot' / 'resources' / 'wonder_twins.yaml', 'r', encoding='utf-8') as f:
    info = yaml.load(f, Loader=yaml.FullLoader)
    WATER_TYPES, OBJECTS, ADJECTIVES = info['water_types'], info['objects'], info["adjectives"]


class WonderTwins(Cog):
    """Cog for a Wonder Twins inspired command."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    def append_onto(phrase: str, insert_word: str) -> str:
        """Appends one word onto the end of another phrase, used to format the use of 'an' or 'a'."""
        if insert_word[-1] == "s":
            phrase = phrase.split()
            del phrase[0]
            phrase = " ".join(phrase)

        insert_word = insert_word.split()[-1]
        return " ".join([phrase, insert_word])

    def format_phrase(self) -> str:
        """Creates a transformation phrase from available words."""
        adjective = random.choice((None, random.choice(ADJECTIVES)))
        object_name = random.choice(OBJECTS)
        water_type = random.choice(WATER_TYPES)

        words = [object_name, water_type]
        if adjective:
            new_object = self.append_onto(adjective, object_name)
            words[0] = new_object
        return f"{words[0]} of {words[1]}"

    @command(name="formof", aliases=["wondertwins", "wondertwin", "fo"])
    async def form_of(self, ctx: Context) -> None:
        """Command to send a Wonder Twins inspired phrase to the user invoking the command."""
        await ctx.send(f"Form of {self.format_phrase()}")


def setup(bot: Bot) -> None:
    """Load the WonderTwins cog."""
    bot.add_cog(WonderTwins(bot))
