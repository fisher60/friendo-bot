"""Commands for the trivia module"""
import discord
from discord.ext import commands
import json
import urllib.request
import random
import os
import html

answers = []
tokenID = ""

amounts = {}
userAnswers = {}


class TriviaCog(commands.Cog):
    """
    Commands for the Trivia Questions
    """

    def __init__(self, bot):
        self.bot = bot
        self.scores = {}
        if not os.path.exists("scores.txt"):
          with open('scores.txt',"w+") as file:
            file.write('{"auth_id": 0}')
        else:
            with open('scores.txt') as json_file:
                self.scores = json.load(json_file)


    # This batch of commands grab from the category based on their name
    @commands.command(
        name="history",
        brief="grabs a question from the history category and allows you to answer",
    )
    async def history(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = 23
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    @commands.command(
        name="book",
        brief="grabs a question from the books category and allows you to answer",
        aliases=["books", "literature"],
    )
    async def book(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = 10
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    @commands.command(
        name="entertainment",
        brief="grabs a question from the entertainment categories and allows you to answer",
    )
    async def entertainment(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = random.randrange(10, 16)
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    @commands.command(
        name="theatre",
        brief="grabs a question from the theatre category and allows you to answer",
    )
    async def theatre(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = 13
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    @commands.command(
        name="film",
        brief="grabs a question from the film category and allows you to answer",
        aliases=["films"],
    )
    async def film(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = 11
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    @commands.command(
        name="trivia",
        brief="grabs a question from a random category and allows you to answer",
    )
    async def trivia(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = random.randrange(9, 32)
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    @commands.command(
        name="computer",
        brief="grabs a question from the computer category and allows you to answer",
        aliases=["computers", "tech"],
    )
    async def computer(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = 18
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    @commands.command(
        name="cartoon",
        brief="grabs a question from the cartoon category and allows you to answer",
        aliases=["cartoons", "anime"],
    )
    async def cartoon(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = 32
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    @commands.command(
        name="animal",
        brief="grabs a question from the animal category and allows you to answer",
        aliases=["animals"],
    )
    async def animal(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = 27
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    @commands.command(
        name="boardgames",
        brief="grabs a question from the boardgame category and allows you to answer",
    )
    async def boardgame(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = 16
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    @commands.command(
        name="videgame",
        brief="grabs a question from the videogame category and allows you to answer",
        aliases=["videogames"],
    )
    async def videogame(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = 15
        embed = generate_embed(auth_id, quiz_var)

        await ctx.send(embed=embed)

    @commands.command(
        name="tv",
        brief="grabs a question from the tv category and allows you to answer",
        aliases=["television"],
    )
    async def tv(self, ctx):
        auth_id = str(ctx.message.author.id)
        quiz_var = 14
        embed = generate_embed(auth_id, quiz_var)
        await ctx.send(embed=embed)

    # listens for user input of an answer
    @commands.Cog.listener()
    async def on_message(self, message):
        auth_id = str(message.author.id)
        ctx = message.channel
        user_answer = message.content.lower()
        if userAnswers[auth_id] != 0:
                if auth_id not in self.scores:
                	self.scores[auth_id]=0;
                if user_answer in ["a", "b", "c", "d"]:
                    correct = userAnswers[auth_id]
                    if correct == 1:
                        correct = "a"
                    elif correct == 2:
                        correct = "b"
                    elif correct == 3:
                        correct = "c"
                    elif correct == 4:
                        correct = "d"
                    embed = discord.Embed(title="Answer")

                    if user_answer == correct:
                        self.scores[auth_id]+=10
                        save(self.scores)
                        values = "You, you got the right answer!"
                        embed.set_footer(text='Your score is: '+str(self.scores[auth_id]))
                    else:
                        values = "Correct answer was: " + str(correct)
                        embed.add_field(name="INCORRECT!", value=values, inline=False)
                    userAnswers[auth_id] = 0
                    await ctx.send(embed=embed)

    #This command prints your scores
    @commands.command(
        name="score",
        brief="returns your score",
    )
    async def score(self,ctx):
      auth_id = str(ctx.message.author.id)
      if auth_id not in self.scores:
        self.scores[auth_id]=0;
      embed = discord.Embed(title='Your Score',description=str(self.scores[auth_id])+' points')
      await ctx.send(embed=embed)

    @commands.command(
        name="leaderboard",
        brief="returns bot trivia leaderboard",
    )
    async def leaderboard(self,ctx):
      leaderboard = {}
      for f in self.scores:
          user = await self.bot.fetch_user(int(f))
          if user != 'none':
            leaderboard[user.display_name] = self.scores[f]


      sorted_leaderboard = sorted(leaderboard.items(),key = lambda t:t[1],reverse=True)
      embed = discord.Embed(title='Leader Board')
      count = 1
      for f in sorted_leaderboard:
        embed.add_field(name=f[0],value=f[1],inline=False)
        count = count+1
      await ctx.send(embed=embed)

    # This command prints an embed listing the categories avaliable
    @commands.command(
        name="categories", brief="returns an embed listing the trivia categories"
    )
    async def categories(self, ctx):
        embed = discord.Embed(title="Trivia Bot Categories")
        embed.add_field(
            name="-trivia",
            value="Gives a question from a random category",
            inline=False,
        )
        embed.add_field(name="-history", value="Gives a history question", inline=False)
        embed.add_field(name="-books", value="Gives a book question", inline=False)
        embed.add_field(name="-film", value="Gives a film question", inline=False)
        embed.add_field(
            name="-entertainment",
            value="Gives a question from the film category",
            inline=False,
        )
        embed.add_field(
            name="-theatre",
            value="Gives a question from the theatre category",
            inline=False,
        )
        embed.add_field(
            name="-animals",
            value="Gives a question from the animal category",
            inline=False,
        )
        embed.add_field(
            name="-videogames",
            value="Gives a question from the video games category",
            inline=False,
        )
        embed.add_field(
            name="-computers",
            value="Gives a question from the computer category",
            inline=False,
        )
        embed.add_field(
            name="-cartoons",
            value="Gives a question from the cartoons category",
            inline=False,
        )
        embed.add_field(
            name="-boardgames",
            value="Gives a question from the boardgames category",
            inline=False,
        )
        embed.add_field(
            name="-tv",
            value="Gives a question from the television category",
            inline=False,
        )
        await ctx.send(embed=embed)


def generate_embed(auth_id, quiz_var):
    """
    Generates an embed to send from the data gotten in url_request,
    takes in a User ID to set the correct answer to and a quizVar for the category number
    """

    data = [6]
    data = url_request(quiz_var)
    userAnswers[auth_id] = int(data[7])

    embed = discord.Embed(title="TRIVIA")

    embed.add_field(name="Category:", value=html.unescape(data[0]), inline=True)
    embed.add_field(name="Difficulty", value=html.unescape(data[1]), inline=True)
    embed.add_field(name="Question", value=html.unescape(data[2]), inline=False)
    embed.add_field(name="A: " + html.unescape(data[3]), value="______", inline=False)
    embed.add_field(name="B: " + html.unescape(data[4]), value="______ ", inline=False)
    embed.add_field(name="C: " + html.unescape(data[5]), value="______ ", inline=False)
    embed.add_field(name="D: " + html.unescape(data[6]), value="______ ", inline=False)
    embed.set_footer(text="Reply with A,B,C,D to answer")
    return embed


def url_request(value: int):
    """takes in a value for the category of the question and returns an array with the info for the question"""
    global tokenID
    url = (
        "https://opentdb.com/api.php?amount=1&category="
        + str(value)
        + "&type=multiple&token="
        + tokenID
    )

    response = urllib.request.urlopen(url)
    data = json.load(response)
    responsecode = data["response_code"]
    if str(responsecode) == "4":
        url2 = "https://opentdb.com/api_token.php?command=reset&token=" + tokenID

    elif str(responsecode) == "3":
        url2 = "https://opentdb.com/api_token.php?command=request"
        response2 = urllib.request.urlopen(url2)
        data2 = json.load(response2)
        tokenID = data2["token"]
        data = url_request(value)
        return data
    else:
        question = data["results"]
        for f in question:
            data[0] = f["category"]
            data[1] = f["difficulty"]
            correct_answer = f["correct_answer"]
            answers = f["incorrect_answers"]
            data[2] = f["question"]

        answers.append(correct_answer)

        random.shuffle(answers)

        correct = correct_answer
        if answers[0] == correct:
            correct = 1
        if answers[1] == correct:
            correct = 2
        if answers[2] == correct:
            correct = 3
        if answers[3] == correct:
            correct = 4

        answers[0] = answers[0].replace("&amp;", "&")
        answers[1] = answers[1].replace("&amp;", "&")
        answers[2] = answers[2].replace("&amp;", "&")
        answers[3] = answers[3].replace("&amp;", "&")

        data[3] = answers[0]
        data[4] = answers[1]
        data[5] = answers[2]
        data[6] = answers[3]
        data[7] = correct


        return data


def save(scores):
  """Saves the user scores to the json file"""
  with open('scores.txt', 'w') as outfile:
    json.dump(scores, outfile)

def setup(bot):
    """Load the bot Cog"""
    bot.add_cog(TriviaCog(bot))
