from discord import Embed, Colour
from discord.ext.commands import Bot, Cog, command
from random import choice, shuffle
from itertools import product
from typing import List


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
        count = 0
        new = ""
        for i in phrase:
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
        description="gives an output of heads or tails like a coin",
        name="flip",
    )
    async def coin_toss(self, ctx, toss):
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
                description=f"Usage: `.8ball will this command work?`",
            )
            await ctx.send(embed=embed)

    @command(
        brief="Play blackjack with the Friendo Bot",
        description="Play one round of blackjack against the computer",
        aliases=("bj",)
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
            await ctx.send(f"your cards: {display_hand(player_hand)}\n"
                           f"computer's cards: {display_hand(computer_hand[1:])}"
                           )

            not_standing = True
            while not_standing:
                # player's turn
                await ctx.send("Type hit or stand")
                message = await self.bot.wait_for("message", check=lambda m: m.content.lower() in ("hit", "stand"))

                if message.content == 'hit':
                    new_card = cards.pop()
                    player_hand.append(new_card)
                    await ctx.send(f"your new card: {new_card}, hand score: {hand_value(player_hand)}")
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
                        await ctx.send(f"Dealer BUST, you WIN! computer's hand: {display_hand(computer_hand)}")
                        break
                else:
                    await ctx.send(f"Dealer stood\n"
                                   f"your hand: {display_hand(player_hand)}\n"
                                   f"computer's hand: {display_hand(computer_hand)}")

                    player_hand_value = hand_value(player_hand)
                    computer_hand_value = hand_value(computer_hand)

                    if player_hand_value < computer_hand_value:
                        await ctx.send("you LOSE!")
                    elif player_hand_value > computer_hand_value:
                        await ctx.send("you WIN!")
                    else:
                        await ctx.send("PUSH!")


def setup(bot: Bot) -> None:
    """Load the Fun cog."""
    bot.add_cog(Fun(bot))
