"""Commands for the trivia module."""
import json
import os

from bot.settings import EMBED_COLOR

from discord import Embed, Reaction
from discord.abc import User
from discord.ext import commands
from discord.ext.commands.bot import Bot
from discord.ext.commands.context import Context
from random import shuffle
from html import unescape
from asyncio import TimeoutError


class Trivia(commands.Cog):
    """commands for the trivia game."""

    def __init__(self, bot: Bot):
        self.bot = bot
        self.TOKEN = "null"
        if os.path.exists("bot/scores.json"):
            with open("bot/scores.json") as file:
                self.scores = json.load(file)
                print('Loaded saved scores')
        else:
            self.scores = {}
            with open("bot/scores.json", "w+") as file:
                json.dump(self.scores, file, indent=4)
            print('Creating Blank Scores')

    @commands.command(
        brief="Takes in an optional argument for category and returns a question.",
        description="Do .trivia categories to see avaliable choices."
    )
    async def trivia(self, ctx: Context, *, category: str = None) -> None:
        """Trvia command takes in an optional category and sends embed."""
        if category:
            category = category.lower()
        if category == 'categories':
            embed = Embed(
                title="Trivia Categories:",
                description="""
                        General
                        Books or Book
                        Film
                        Music
                        Theatre
                        Televsion or TV
                        Video Games or VG
                        Board Games or BG
                        Science
                        Computers or Computer
                        Math
                        Mythology or Myths
                        Geography or Geo
                        History
                        Art
                        Animals or Animal
                        Comics or Comic
                        Anime
                        Cartoons or Cartoon
                            """,
                color = EMBED_COLOR
            )
            embed.set_footer(
                text="Do .trivia (category name) to choose a category, categories are NOT case sensitive."
            )
            await ctx.send(embed=embed)
            return
        elif category == 'general':
            category = 9
        elif category == 'book' or category == 'books':
            category = 10
        elif category == 'film':
            category = 11
        elif category == 'music':
            category = 12
        elif category == 'theatre':
            category = 13
        elif category == 'television' or category == 'tv':
            category = 14
        elif category == 'vg' or category == 'video games':
            category = 15
        elif category == 'bg' or category == 'board games':
            category = 16
        elif category == 'science':
            category = 17
        elif category == 'computer' or category == 'computers':
            category = 18
        elif category == 'math':
            category = 19
        elif category == 'mythology' or category == 'myth':
            category = 20
        elif category == 'sports':
            category = 21
        elif category == 'geography' or category == 'geo':
            category = 22
        elif category == 'history':
            category = 23
        elif category == 'art':
            category = 25
        elif category == 'animals' or category == 'animal':
            category = 27
        elif category == 'comics' or category == 'comic':
            category = 29
        elif category == 'anime':
            category = 31
        elif category == 'cartoons' or category == 'cartoon':
            category = 32

        message = await ctx.send(embed=Embed(title='Loading.....', color=EMBED_COLOR))

        while True:
            t_data = await self.get_trivia(category)
            embed = Embed(
                title=t_data['question'],
                description=f"1️⃣: {t_data['answers'][0]}\n\n"
                            f"2️⃣: {t_data['answers'][1]}\n\n"
                            f"3️⃣: {t_data['answers'][2]}\n\n"
                            f"4️⃣: {t_data['answers'][3]}\n\n"
                            f"You have 15 seconds or until {ctx.author.mention} answers!",
                color=EMBED_COLOR
            )
            embed.set_author(name=f"{t_data['difficulty']} question for {t_data['points']} points")
            embed.set_footer(text=t_data['category'])

            await message.edit(
                embed=embed
            )
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')
            await message.add_reaction('3️⃣')
            await message.add_reaction('4️⃣')

            answers = {}

            def r_check(reaction: Reaction, user: User) -> bool:
                return reaction.message.id == message.id and not user.bot

            while True:
                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=r_check)
                except TimeoutError:
                    break
                if reaction.emoji == '1️⃣':
                    answers[str(user.id)] = (1, user.name)
                elif reaction.emoji == '2️⃣':
                    answers[str(user.id)] = (2, user.name)
                elif reaction.emoji == '3️⃣':
                    answers[str(user.id)] = (3, user.name)
                elif reaction.emoji == '4️⃣':
                    answers[str(user.id)] = (4, user.name)

                await reaction.remove(user)

                if user.id == ctx.author.id:
                    break

            winners = []

            for user in answers:
                if answers[user][0] == t_data['correct']:
                    if user in self.scores:
                        self.scores[user][1] += t_data['points']
                    else:
                        self.scores[user] = [answers[user][1], t_data['points']]
                    winners.append(answers[user][1])

            with open("bot/scores.json", "w+") as file:
                json.dump(self.scores, file, indent=4)

            if winners:
                title = "Congrats"
                description = f"{','.join(winners)} got it right, it was:\n"\
                    f"   {t_data['answers'][t_data['correct']-1]}\n\n"\
                    "*React with ✅ to play again!*"
            else:
                title = "No One Got the correct answer, it was:\n"
                description = f"   {t_data['answers'][t_data['correct']-1]}\n\n"\
                    "*React with ✅ to play again!*"

            await message.edit(embed=Embed(
                title=title,
                description=description,
                color=EMBED_COLOR
            ))

            await message.add_reaction("✅")
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=r_check)
            except TimeoutError:
                break
            await reaction.remove(user)

        message = await ctx.fetch_message(message.id)
        await message.edit(embed=Embed(
            title="Nobody wanted to play trivia again 😞",
            color=EMBED_COLOR
        ))
        for reaction in message.reactions:
            await reaction.clear()

    @commands.command(
        brief="Gets a users score of the trivia game.",
        aliases=['points']
    )
    async def score(self, ctx: Context) -> None:
        """Generates an embed with the users score (if applicable)."""
        if str(ctx.author.id) in self.scores:
            await ctx.send(embed=Embed(
                title=f"Trivia Score for {ctx.author.name}",
                description=f"You currently have {self.scores[str(ctx.author.id)][1]} points!",
                color=EMBED_COLOR
            ))
        else:
            await ctx.send(embed=Embed(
                title="You need to play first!",
                description="Do .trivia to play!",
                color=EMBED_COLOR
            ))

    @commands.command(
        brief="Gets the trivia leaderboard.",
    )
    async def leaderboard(self, ctx: Context) -> None:
        """Generates an embed with the trivia leaderboard."""
        leaders = []
        for user in self.scores:
            leaders.append([self.scores[user][0], self.scores[user][1]])
        leaders.sort(key=lambda x: x[1])
        leaders.reverse()
        description = ""
        for count, leader in enumerate(leaders):
            if count == 0:
                description += f"🥇: {leader[0]} with {leader[1]} points\n\n"
            elif count == 1:
                description += f"🥈: {leader[0]} with {leader[1]} points\n\n"
            elif count == 2:
                description += f"🥉: {leader[0]} with {leader[1]} points\n\n"
            elif count == 25:
                break
            else:
                description += f"{count+1}: {leader[0]} with {leader[1]} points\n"
        if not description:
            description = "No one has played yet!"
        embed = Embed(
            title="Trivia top 25 leaderboard",
            description=description,
            color=EMBED_COLOR
        )
        if str(ctx.author.id) in self.scores:
            embed.set_footer(text=f"{ctx.author.name} you have {self.scores[str(ctx.author.id)][1]} points")
        await ctx.send(embed=embed)

    async def get_trivia(self, category: str) -> dict:
        """Function Used to generate the dictionary with question data."""
        if not category:
            url = "https://opentdb.com/api.php?amount=1&type=multiple&token="
        else:
            url = f"https://opentdb.com/api.php?amount=1&category={category}&type=multiple&token="
        reset_url = "https://opentdb.com/api_token.php?command=reset&token="
        while True:
            async with self.bot.session.get(url+self.TOKEN) as resp:
                data = await resp.json()
            if data['response_code'] == 0:
                break
            elif data['response_code'] == 3:
                async with self.bot.session.get('https://opentdb.com/api_token.php?command=request') as resp:
                    self.TOKEN = (await resp.json())['token']
                    print('Generating Token')
            elif data['response_code'] == 4:
                await self.bot.session.get(reset_url+self.TOKEN)
        data = data['results'][0]

        answers = [
            unescape(data['incorrect_answers'][0]),
            unescape(data['incorrect_answers'][1]),
            unescape(data['incorrect_answers'][2]),
            unescape(data['correct_answer']),
        ]
        shuffle(answers)
        for _count, item in enumerate(answers):
            if item == data['correct_answer']:
                break

        if data['difficulty'] == 'easy':
            points = 5
        elif data['difficulty'] == 'medium':
            points = 10
        elif data['difficulty'] == 'hard':
            points = 20

        return {
            'correct': _count+1,
            'answers': answers,
            'difficulty': data['difficulty'],
            'question': unescape(data['question']),
            'points': points,
            'category': f"Category: {data['category']}"
        }


def setup(bot: Bot) -> None:
    """Imports the cog."""
    bot.add_cog(Trivia(bot))
