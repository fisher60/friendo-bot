"""
Commands that do not serve a useful function aside from being fun.
"""
import functools
import re
import string
from itertools import product
from random import choice, shuffle, randint
from typing import List

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

def get_factorial(num: int):
    """ Returns the factorial of `num` """

    answer = 1
    for i in range(num, 0, -1):
        answer *= i
    return answer

class Fun(Cog):
    """commands for fun that offer no benefit to users."""

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(
        brief="Send a number and get the factorial of it",
    )
    async def factorial(self, ctx, number: int):
        """
        Sends the factorial of `number`
        eg. 10 -> 3628800
        """
        if number > 69:
            await ctx.send("Hey woah don't break me. Give me a number upto 69")
            return

        result = await ctx.bot.loop.run_in_executor(None, get_factorial, number)
        await ctx.send(
            f"The factorial of **{number}** is **{result}** ({number}! = {result})"
        )

    @command(
        brief="Alternate case of inputted text",
        description="converts a phrase to alternating case",
    )
    async def spongify(self, ctx, *, phrase):
        """Converts input string to alternating case."""
        count = 0
        new = ""
        for i in phrase.lower():
            if i in string.punctuation:
                new += i
            else:
                if count % 2 == 0:
                    new += i
                else:
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
        brief="simulates a dice roll",
        description=".dice [quantity] [sides]\n"
        "`quantity` - how many to roll\n"
        "`sides` - how many sides each die will have",
    )
    async def dice(self, ctx, n: int, sides: int) -> None:
        """simple dice roll"""

        if n == 0:
            await ctx.send("you must roll at least one die")
        elif sides < 2:
            await ctx.send(f"you can't roll a {sides}-sided die")
        else:
            result = sum(randint(1, sides) for _ in range(n))

            await ctx.send(f"you rolled {result}")

    @command(
        brief="Ask any question to the 8ball",
        description="accepts a question and gives you an 8ball answer",
        name="8ball",
    )
    async def eight_ball(self, ctx, *, question=None):
        """Returns an 8ball response to a user's question."""

        responses = [
            "It is certain",
            "Yes, definitely",
            "Without a doubt",
            "That's for sure",
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

    @command(
        brief="Play a game of rock paper scissors. Usage: .rps rock",
        description="Enter an option between rock, paper, scissor after .play",
        aliases=["play", "Play", "RPS"],
    )
    async def rps(self, ctx, *, response=None):
        """Returns strings based on winning/losing/tie"""
        response = response.lower()
        options = ["rock", "paper", "scissors"]
        bot_choice = choice(options)
        win = "I win... I hope you arent angry?.😂"
        lose = "I lose.. 😶"
        choose = f"I choose {bot_choice}"

        if response not in options:
            await ctx.send("Please choose between rock, paper or scissors")
        elif response == bot_choice:
            await ctx.send(f"I choose {bot_choice}\nOh, we got a tie")

        elif response == "rock":
            await ctx.send(choose)
            await ctx.send(win if bot_choice == "paper" else lose)

        elif response == "paper":
            await ctx.send(choose)
            await ctx.send(win if bot_choice == "scissors" else lose)

        elif response == "scissors":
            await ctx.send(choose)
            await ctx.send(win if bot_choice == "rock" else lose)

        else:
            embed = Embed(
                title="Rock, Paper, Scissor",
                colour=Colour.red(),
                description="Usage: `.rps rock/paper/scissors`",
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

    @command(
        brief="Play blackjack with the Friendo Bot",
        description="Play one round of blackjack against the computer",
        aliases=("bj",),
    )
    async def blackjack(self, ctx):
        """simple blackjack game"""

        def display_hand(hand: List[str]) -> str:
            return f"{' '.join(hand)}, value: {hand_value(hand)}"

        def hand_value(hand: List[str]) -> int:
            """helper function to calculate the value of a hand"""

            convert = {str(i): i for i in range(2, 11)}
            convert.update({"A": 1, "J": 10, "Q": 10, "K": 10})

            value = 0
            has_ace = False

            # add up the normal cards and deal with aces at the end
            for card in hand:
                value += convert[card[:-1]]
                if card[:-1] == "A":
                    has_ace = True

            if value + 10 <= 21 and has_ace:
                value += 10

            return value

        VALUES = ["A", *map(str, range(2, 11)), "J", "Q", "K"]
        SUITS = ["D", "H", "S", "C"]

        # should be impossible to exhaust the entire list, so we can pop cards to emulate dealing
        cards = ["".join(c) for c in product(VALUES, SUITS)]
        shuffle(cards)

        player_hand = [cards.pop() for _ in range(2)]
        computer_hand = [cards.pop() for _ in range(2)]

        if hand_value(player_hand) == 21:
            await ctx.send("BLACKJACK! you WIN!")
        else:
            await ctx.send(
                f"your cards: {display_hand(player_hand)}\n"
                f"computer's cards: {display_hand(computer_hand[1:])}"
            )

            not_standing = True
            while not_standing:
                # player's turn
                await ctx.send("Type hit or stand")
                message = await self.bot.wait_for(
                    "message", check=lambda m: m.content.lower() in ("hit", "stand")
                )

                if message.content == "hit":
                    new_card = cards.pop()
                    player_hand.append(new_card)
                    await ctx.send(
                        f"your new card: {new_card}, hand score: {hand_value(player_hand)}"
                    )
                else:
                    await ctx.send(f"final hand: {display_hand(player_hand)}")
                    not_standing = False

                if hand_value(player_hand) > 21:
                    await ctx.send(f"BUST, you LOSE! hand: {display_hand(player_hand)}")
                    break
            else:
                # dealer's turn, only runs if player didn't bust
                while hand_value(computer_hand) < 17:
                    computer_hand.append(cards.pop())
                    if hand_value(computer_hand) > 21:
                        await ctx.send(
                            f"Dealer BUST, you WIN! computer's hand: {display_hand(computer_hand)}"
                        )
                        break
                else:
                    await ctx.send(
                        f"Dealer stood\n"
                        f"your hand: {display_hand(player_hand)}\n"
                        f"computer's hand: {display_hand(computer_hand)}"
                    )

                    player_hand_value = hand_value(player_hand)
                    computer_hand_value = hand_value(computer_hand)

                    if player_hand_value < computer_hand_value:
                        await ctx.send("you LOSE!")
                    elif player_hand_value > computer_hand_value:
                        await ctx.send("you WIN!")
                    else:
                        await ctx.send("PUSH!")


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
