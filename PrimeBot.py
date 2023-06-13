from discord.ext import commands
import discord
from discord import FFmpegPCMAudio


SklarChannel = ''
intents = discord.Intents.all()


bot = commands.Bot(command_prefix='^', intents=intents)


# Functions
@bot.command()
async def sklarSet(ctx):
    global SklarChannel
    SklarChannel = ctx.channel.id
    await ctx.message.delete()

@bot.command()
async def pTime(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('Files/PM.wav')
        player = voice.play(source)


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

@bot.event
async def on_voice_state_update(member, before, after):

      if before.channel is None and after.channel is not None:
        if after.channel.id == 774879876670029864:
            channel = after.channel
            voice = await channel.connect()
            source = FFmpegPCMAudio('Files/PM.wav')
            player = voice.play(source)
         #do whatever you want here


# Token
bot.run("")
