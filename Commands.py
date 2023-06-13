from discord.ext import commands
import discord


SklarChannel = ''
intents = discord.Intents.all()


bot = commands.Bot(command_prefix='^', intents=intents)


# Functions
@bot.command()
async def sklarSet(ctx):
    global SklarChannel
    SklarChannel = ctx.channel.id
    await ctx.message.delete()

# Client Components
@bot.event
async def on_ready():
    print('AWAWA')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.channel.id == SklarChannel:
        if message.content != "sklar":
            await message.channel.send('sklar') 
            await message.delete()

    # Message Replies
    if message.content == 'cal':
        await message.channel.send('cal')

    await bot.process_commands(message)


# Token
bot.run("")
