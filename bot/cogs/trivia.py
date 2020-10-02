import discord
from discord.ext import commands
import os
import json
import urllib.request
import random

correct = 'wrong'
difficulty = 'easy'
category = 'null'
answers = []
difficult = 'null'
tokenID= '1234'

amounts = {}
userAnswers = {}


class TriviaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def history(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = 23
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        _saveA()
        #print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)


    @commands.command()
    async def books(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = 10
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        _saveA()
        #print(userAnswers[id])
         embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)

    @commands.command()
    async def entertainment(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = random.randrange(10, 16)
        #print(quizVar)
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        _saveA()
        #print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)


    @commands.command()
    async def theatre(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = 13
        #print(quizVar)
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        _saveA()
        #print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)
        
        @bot.command()
    async def film(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = 11
        #print(quizVar)
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        _saveA()
        #print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)



    @commands.command()
    async def trivia(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = random.randrange(9, 32)
        #print(quizVar)
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        _saveA()
        #print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)


    @commands.command()
    async def computers(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = 18
        #print(quizVar)
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        
        #print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)


    @commands.command()
    async def cartoons(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = 32
        #print(quizVar)
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        
        #print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)


    @commands.command()
    async def animals(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = 27
        print(quizVar)
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        
        print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)


    @commands.command()
    async def boardgames(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = 16
        print(quizVar)
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        
        print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)


    @commands.command()
    async def videogames(ctx):
        global userAnswers
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = 15
        #print(quizVar)
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        
        #print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)


    @commands.command()
    async def tv(ctx):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        data = [6]
        quizVar = 14
        #print(quizVar)
        data = url_request(quizVar)
        userAnswers[id] = int(data[7])
        
        #print(userAnswers[id])
        embed=discord.Embed(title='TRIVIA')

        embed.add_field(name='Category:',value=data[0],inline=True)
        embed.add_field(name='Difficulty',value=data[1],inline=True)
        embed.add_field(name='Question',value=data[2],inline=False)
        embed.add_field(name='A: '+data[3],value='______',inline=False)
        embed.add_field(name='B: '+data[4],value='______ ',inline=False)
        embed.add_field(name='C: '+data[5],value='______ ',inline=False)
        embed.add_field(name='D: '+data[6],value='______ ',inline=False)
        embed.set_footer(text =  'Reply -answer (a,b,c or d) to answer')
        await ctx.send(embed=embed)




    @commands.command()
    async def answer(ctx,*,args):
        id = str(ctx.message.author.id)
        user = bot.get_user(int(id))
        correct = userAnswers[id]
        if correct == 1:
          correct = 'A'
        elif correct == 2:
          correct = 'B'
        elif correct == 3:
          correct = 'C'
        elif correct == 4:
          correct = 'D'
        elif correct ==0:
          correct = 'https://media1.tenor.com/images/255df1d886da07cd869f7425a6b73014/tenor.gif?itemid=11397484'

        if args == 'a':
          args = 'A'
        elif args == 'b':
          args = 'B'
        elif args == 'c':
          args = 'C'
        elif args == 'd':
          args = 'D'

        embed=discord.Embed(title="Answer")
        print(correct)

        if args == correct:
          values = "You, you got the right answer!"
          embed.add_field(name="CORRECT!", value=values, inline=False)
          _save()
        else:
          values = "Correct answer was: "+str(correct)
          embed.add_field(name="INCORRECT!", value=values,inline=False)

        await ctx.send(embed=embed)
        userAnswers[id] = 0

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

    @commands.command()
    async def categories(ctx):
        id = str(ctx.message.author.id)
        global embed
        await ctx.send(embed=embed)


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(MembersCog(bot))
