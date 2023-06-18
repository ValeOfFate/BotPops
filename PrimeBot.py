from discord.ext import commands
import discord
from discord import FFmpegPCMAudio
import json

# Config Values
SklarChannel = ''
BotToken = ''
DomainAddress = ''
BotID = ''

# Bot Creation
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='^', intents=intents)

# Config Loading
with open('Config.json') as uFile:
        Data = uFile.read()
        Obj = json.loads(Data)

BotToken = Obj['BotToken']
SklarChannel = Obj['SklarChannel']
DomainAddress = Obj['DomainAddress']
BotID = Obj['BotID']

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

    voice_state = member.guild.voice_client

    if member.id != BotID: 
        if after.channel != None and after.channel.id == DomainAddress and len(after.channel.members) == 1:
            channel = after.channel
            BotClient = await channel.connect()
            source = FFmpegPCMAudio('Files/PM.wav')
            player = BotClient.play(source)

        if before.channel != None and before.channel.id == DomainAddress and len(before.channel.members) == 1:
            channel = before.channel
            await voice_state.disconnect()

    if member.id == BotID and after.channel != None: 
        if after.channel != None and after.channel.id != DomainAddress:
            channel = before.channel
            discon = await voice_state.disconnect(force=True)

    

# Token
bot.run(BotToken)
