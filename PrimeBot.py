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

# Client Components

# Startup
@bot.event
async def on_ready():
    print('AWAWA')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Sklar Protection
    if message.channel.id == SklarChannel:
        if message.content != "sklar":
            await message.channel.send('sklar') 
            await message.delete()

    # Message Replies
    if message.content == 'cal':
        await message.channel.send('cal')

    await bot.process_commands(message)

# Voice State events
@bot.event
async def on_voice_state_update(member, before, after):

    voice_state = member.guild.voice_client

    if member.id != BotID: 
        # Join channel functionality
        if after.channel != None and after.channel.id == DomainAddress and len(after.channel.members) == 1:
            channel = after.channel
            BotClient = await channel.connect()
            source = FFmpegPCMAudio('Files/PM.wav')
            player = BotClient.play(source)

        # Natural Leaving
        if before.channel != None and before.channel.id == DomainAddress and len(before.channel.members) == 1:
            channel = before.channel
            await voice_state.disconnect()

    # Forced Leaving
    if member.id == BotID and after.channel != None: 
        if after.channel != None and after.channel.id != DomainAddress:
            channel = before.channel
            discon = await voice_state.disconnect(force=True)

# Token
bot.run(BotToken)
