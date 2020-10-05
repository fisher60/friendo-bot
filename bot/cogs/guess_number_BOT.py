import discord
import math, random
from discord.ext import commands

client = commands.Bot(command_prefix = '.')

class myClass: # Create class to avoid global on variables
    # Default bounds unless it's rewritten with .bound command
    lower_bound = 1
    upper_bound = 100
    # Just count from # rounds to 0 and game end. Increase by 1 each time .n command is called.
    count = 0

    check_number = round(random.randint(lower_bound, upper_bound)) # Random number between lower and upper bounds.
    rounds_number = round(math.log(upper_bound - lower_bound + 1, 2)) # Random number of rounds like 3 rounds till game end.

### Results in terminal
@client.event
async def on_ready():
    print('Bot is ready.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

async def on_member_remove(member):
    print(f'{member} has left a server.')

### Commands
@client.command()
async def ping(ctx): # write '.ping' to invoke the command.  .ping => ping(ctx)
    # invoke the command
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms\nType `.start` to start a game.\nType `.use` to view commands.')

@client.command()
async def use(ctx):
    await ctx.send(f'```\n'
                   '(Help):\n'
                   f'.start:' '   Start the game\n'
                   '.n:       Type number to guess\n'
                   '.ping:    Ring the bot!\n'
                   '.bound default <=> .bound 1 10\nDefault between 1 and 100 <=> Guess between 1 and 10.\n'
                   '\n```')

@client.command()
async def bound(ctx, lower, upper): # Will set bound when called.
    obj = myClass()

    if lower == 'default': # In case someone want to change it back to default
        obj.lower_bound = 1
        obj.upper_bound = 100
        await ctx.send(f'You entered 1 and 100 as default bounds.')
    obj.lower_bound = lower
    obj.upper_bound = upper
    await ctx.send(f'You entered bounds: {lower} and {upper}')


# Give details.
@client.command()
async def start(ctx):
    # Create an object of myClass
    obj = myClass()

    await ctx.send(f'Try to guess a random number between {obj.lower_bound}-{obj.upper_bound}.\nType a number after `.n` command.\nGood Luck!', delete_after=30)

    #upper = obj.upper_bound
    #lower = obj.lower_bound

    #check_number = obj.random_number # Random number

    #roundn = obj.rounds_number # Number of rounds

    #count = 0 => Already defined in myClass

@client.command()
async def n(ctx, guess_number: int):
    obj = myClass()

    obj.count += 1 # Will add to count = 0 each time this command is called.

    await ctx.send(obj.count)

    if obj.check_number == guess_number:
        await ctx.send(f'Congratulations you did it! You entered {guess_number}.\nType `.start` to play again or Type `.use` to view commands.')
    elif obj.check_number > guess_number:
        await ctx.send(f'You guessed too small!  Try again {obj.rounds_number - obj.count} round(s) pending.', delete_after=30)
    elif obj.check_number < guess_number:
        await ctx.send(f'You guessed too high!  Try again. {obj.rounds_number - obj.count} round(s) pending.', delete_after=30)
    if obj.count >= obj.rounds_number:
        await ctx.send(f'Sorry! The number is {obj.check_number}. Type `.start` to play again.')


client.run('token')