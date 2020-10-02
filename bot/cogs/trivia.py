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
    async def history(self,ctx):
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
        data = [6]
        quizVar = 23
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
    async def books(self,ctx):
        id = str(ctx.message.author.id)
        user = self.self.bot.get_user(int(id))
        data = [6]
        quizVar = 10
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
    async def entertainment(self,ctx):
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
        data = [6]
        quizVar = random.randrange(10, 16)
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
    async def theatre(self,ctx):
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
        data = [6]
        quizVar = 13
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
    async def film(self,ctx):
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
        data = [6]
        quizVar = 11
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
    async def trivia(self,ctx):
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
        data = [6]
        quizVar = random.randrange(9, 32)
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
    async def computers(self,ctx):
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
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
    async def cartoons(self,ctx):
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
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
    async def animals(self,ctx):
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
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
    async def boardgames(self,ctx):
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
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
    async def videogames(self,ctx):
        global userAnswers
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
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
    async def tv(self,ctx):
        id = str(ctx.message.author.id)
        user = self.bot.get_user(int(id))
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
        user = self.bot.get_user(int(id))
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
    async def categories(self,ctx):
        id = str(ctx.message.author.id)
        global embed
        await ctx.send(embed=embed)

def url_request(value : int):
    global tokenID
    url = 'https://opentdb.com/api.php?amount=1&category='+str(value) +'&type=multiple&token='+tokenID

    data = [6]
    response = urllib.request.urlopen(url)
    data = json.load(response)
    print('Data is:')
    print(data)
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
        print(tokenID)
        data = url_request(value)
        return data
    else:   
        print(data['response_code'])
        question = data['results']
        for f in question:
            data[0] = f['category']
            data[1] = f['difficulty']
            correctAnswer = f['correct_answer']
            answers = f['incorrect_answers']
            data[2] = f['question']

        answers.append(correctAnswer)

        random.shuffle(answers)


        global correct 
        correct = correctAnswer

        global difficulty
        difficulty = difficult

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


# The setup fucntion below is neccesarry. Remember we give bot.add_cog() the name of the class in this case MembersCog.
# When we load the cog, we use the name of the file.
def setup(bot):
    bot.add_cog(TriviaCog(bot))
