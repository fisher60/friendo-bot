"""
Commands that do not serve a useful function aside from being fun.
"""
import functools
import re
import string
from random import choice

from discord import Embed, Colour
from discord.ext.commands import Bot, Cog, command

UWU_WORDS = {
    "fi": "fwi",
    "l": "w",
    "r": "w",
    "some": "sum",
    "th": "d",
    "thing": "fing",
    "tho": "fo",
    "you're": "yuw'we",
    "your": "yur",
    "you": "yuw",
}


class Fun(Cog):
    """commands for fun that offer no benefit to users."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        brief="Alternate case of inputted text",
        description="converts a phrase to alternating case",
        name="tosponge",
    )
    async def to_sponge(self, ctx, *, phrase):
        """Converts input string to alternating case."""
        count = 0
        new = ""
        for i in phrase.lower():
            if i == " ":
                new += i
            else:
                if count % 2 == 0:
                    new += i
                if count % 2 == 1:
                    new += i.upper()
                count += 1

        await ctx.send(new)
        return new

    @command(
        brief="simulates a coin toss",
        description="accepts a string value of heads or tails and tells you if you win or lose the call, ie .flip heads",
        name="flip",
    )
    async def coin_toss(self, ctx, toss):
        """Determines whether or not a user won a coin toss."""

        outcomes = ["heads", "tails"]

        if toss == choice(outcomes):
            msg = f"{ctx.author.mention} wins!"
        else:
            msg = f"{ctx.author.mention} loses!"

        await ctx.send(msg)

    @command(
        brief="Ask any question to the 8ball",
        description="accepts a question and gives you an 8ball answer",
        name="8ball",
    )
    async def eight_ball(self, ctx, *, question=None):
        """Returns an 8ball response to a user's question."""

        responses = [
            "It is certain",
            "Yes, definately",
            "Without a doubt",
            "Thats for sure",
            "Most likely",
            "Umm, try again",
            "Didnt quite get that",
            "Concentrate and try again",
            "Not likely at all",
            "My reply is no",
            "Obviously not",
            "No...",
            "My sources say no",
        ]

        if question:
            await ctx.send(f"Question: {question}\nAnswer: {choice(responses)}")

        # Send help if question == None
        else:
            embed = Embed(
                title="8ball",
                colour=Colour.blue(),
                description="Usage: `.8ball will this command work?`",
            )
            await ctx.send(embed=embed)

    @command(brief="uwuify any text you like", name="uwu")
    async def uwu(self, ctx, *text):
        """
        Converts a given `text` into it's uwu equivalent.

        This is shamelessly stolen from Python Discord's seasonalbot.
        https://github.com/python-discord/seasonalbot/blob/master/bot/exts/evergreen/fun.py
        """
        text = " ".join(text)
        conversion_func = functools.partial(
            _replace_many, replacements=UWU_WORDS, ignore_case=True, match_case=True
        )
        converted_text = conversion_func(text)
        # Don't put >>> if only embed present
        if converted_text:
            converted_text = f">>> {converted_text.lstrip('> ')}"
        await ctx.send(content=converted_text)


def _replace_many(
    sentence: str,
    replacements: dict,
    *,
    ignore_case: bool = False,
    match_case: bool = False,
) -> str:
    """
    Replaces multiple substrings in a string given a mapping of strings.
    By default replaces long strings before short strings, and lowercase before uppercase.
    Example:
        var = replace_many("This is a sentence", {"is": "was", "This": "That"})
        assert var == "That was a sentence"
    If `ignore_case` is given, does a case insensitive match.
    Example:
        var = replace_many("THIS is a sentence", {"IS": "was", "tHiS": "That"}, ignore_case=True)
        assert var == "That was a sentence"
    If `match_case` is given, matches the case of the replacement with the replaced word.
    Example:
        var = replace_many(
            "This IS a sentence", {"is": "was", "this": "that"}, ignore_case=True, match_case=True
        )
        assert var == "That WAS a sentence"

    This is shamelessly stolen from Python Discord's seasonalbot
    https://github.com/CharlieADavies/seasonalbot/blob/master/bot/utils/__init__.py
    """
    if ignore_case:
        replacements = dict(
            (word.lower(), replacement) for word, replacement in replacements.items()
        )

    words_to_replace = sorted(replacements, key=lambda s: (-len(s), s))

    # Join and compile words to replace into a regex
    pattern = "|".join(re.escape(word) for word in words_to_replace)
    regex = re.compile(pattern, re.I if ignore_case else 0)

    def _repl(match: re.Match) -> str:
        """Returns replacement depending on `ignore_case` and `match_case`."""
        word = match.group(0)
        replacement = replacements[word.lower() if ignore_case else word]

        if not match_case:
            return replacement

        # Clean punctuation from word so string methods work
        cleaned_word = word.translate(str.maketrans("", "", string.punctuation))
        if cleaned_word.isupper():
            return replacement.upper()
        elif cleaned_word[0].isupper():
            return replacement.capitalize()
        else:
            return replacement.lower()

    return regex.sub(_repl, sentence)


def setup(bot: Bot) -> None:
    """Load the Fun cog."""
    bot.add_cog(Fun(bot))
