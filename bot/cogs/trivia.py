import discord
from discord.ext import commands
import json
import urllib.request
import random

correct = 'wrong'
category = 'null'
answers = []
tokenID= ''

amounts = {}
userAnswers = {}


class TriviaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def history(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = 23
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)


    @commands.command()
    async def books(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = 10
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)

    @commands.command()
    async def entertainment(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = random.randrange(10, 16)
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)


    @commands.command()
    async def theatre(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = 13
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def film(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = 11
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)



    @commands.command()
    async def trivia(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = random.randrange(9, 32)
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)


    @commands.command()
    async def computers(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = 18
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)


    @commands.command()
    async def cartoons(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = 32
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)


    @commands.command()
    async def animals(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = 27
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)


    @commands.command()
    async def boardgames(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = 16
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)


    @commands.command()
    async def videogames(self,ctx):
        global userAnswers
        id = str(ctx.message.author.id)
        quizVar = 15
        embed = generate_embed(id,quizVar)
        
        await ctx.send(embed=embed)


    @commands.command()
    async def tv(self,ctx):
        id = str(ctx.message.author.id)
        quizVar = 14
        embed= generate_embed(id,quizVar)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
      id = str(message.author.id)
      ctx = message.channel
      user_answer = message.content.lower()
      try:
        if userAnswers[id] != 0:
          if user_answer in ['a','b','c','d']:
              correct = userAnswers[id]
              if correct == 1:
                correct = 'a'
              elif correct == 2:
                correct = 'b'
              elif correct == 3:
                correct = 'c'
              elif correct == 4:
                correct = 'd'
              embed=discord.Embed(title="Answer")

              if user_answer == correct:
                values = "You, you got the right answer!"
                embed.add_field(name="CORRECT!", value=values, inline=False)
              else:
                values = "Correct answer was: "+str(correct)
                embed.add_field(name="INCORRECT!", value=values,inline=False)
              userAnswers[id]=0
              await ctx.send(embed=embed)
              
      except:
        'user not in array'
        

    @commands.command()
    async def categories(self,ctx):
        embed=discord.Embed(title="Trivia Bot Categories")
        embed.add_field(name="-trivia", value="Gives a question from a random category", inline=False)
        embed.add_field(name="-history", value="Gives a history question", inline=False)
        embed.add_field(name="-books", value="Gives a book question", inline=False)
        embed.add_field(name="-film", value="Gives a film question", inline=False)
        embed.add_field(name="-entertainment", value="Gives a question from the film category", inline=False)
        embed.add_field(name="-theatre", value="Gives a question from the theatre category", inline=False)
        embed.add_field(name="-animals", value="Gives a question from the animal category", inline=False)
        embed.add_field(name="-videogames", value="Gives a question from the video games category", inline=False)
        embed.add_field(name="-computers", value="Gives a question from the computer category", inline=False)
        embed.add_field(name="-cartoons", value="Gives a question from the cartoons category", inline=False)
        embed.add_field(name="-boardgames", value="Gives a question from the boardgames category", inline=False)
        embed.add_field(name="-tv", value="Gives a question from the television category", inline=False)
        await ctx.send(embed=embed)


def generate_embed(id,quizVar):
        data = [6]
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply with A,B,C,D to answer')
        return embed

def url_request(value : int):
    global tokenID
    url = 'https://opentdb.com/api.php?amount=1&category='+str(value) +'&type=multiple&token='+tokenID

    data = [6]
    response = urllib.request.urlopen(url)
    data = json.load(response)
    responsecode = data['response_code']
    if str(responsecode) == '4':
      url2 = 'https://opentdb.com/api_token.php?command=reset&token='+tokenID
      response2 = urllib.request.urlopen(url2)
      data2 = json.load(response2)
    elif str(responsecode)== '3':
        url2 = 'https://opentdb.com/api_token.php?command=request'
        response2=urllib.request.urlopen(url2)
        data2 = json.load(response2)
        tokenID=data2['token']
        data = url_request(value)
        return data
    else:   
        question = data['results']
        for f in question:
            data[0] = f['category']
            data[1] = f['difficulty']
            correctAnswer = f['correct_answer']
            answers = f['incorrect_answers']
            data[2] = f['question']

        answers.append(correctAnswer)

        random.shuffle(answers)

        correct = correctAnswer

        answers[0] = answers[0].replace("&#039;","'")
        answers[1] = answers[1].replace("&#039;","'")
        answers[2] = answers[2].replace("&#039;","'")
        answers[3] = answers[3].replace("&#039;","'")

        if answers[0] == correct:
          correct = 1
        if answers[1] == correct:
          correct = 2
        if answers[2] == correct:
          correct = 3
        if answers[3] == correct:
          correct = 4

        answers[0]=answers[0].replace('&amp;','&')
        answers[1]=answers[1].replace('&amp;','&')
        answers[2]=answers[2].replace('&amp;','&')
        answers[3]=answers[3].replace('&amp;','&')


        data[3]=answers[0]
        data[4]=answers[1]
        data[5]=answers[2]
        data[6]=answers[3]
        data[7]=correct


        data[2]=data[2].replace('&quot;','"')
        data[2]=data[2].replace('&#039;',"'")

        return data


def setup(bot):
    bot.add_cog(TriviaCog(bot))
