import asyncio
from discord.ext import commands
import discord
from discord import FFmpegPCMAudio
import json

# Config Values
SklarChannel = ''
BotToken = ''
DomainAddress = ''
BotID = ''
SklarValues = ''

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
SklarValues = Obj['SklarValues']

uFile.close()

# Client Components

# Startup
@bot.event
async def on_ready():
    print('Bot Ready')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Sklar Protection
    if message.channel.id == SklarChannel and message.author != 690261128596816027:
        if message.content not in SklarValues:
            await message.channel.send('sklar') 
            await message.delete()
            return

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
            # Create voice Loop
            bot.loop.create_task(play_source(BotClient, channel))

        # Natural Leaving
        if before.channel != None and before.channel.id == DomainAddress and len(before.channel.members) == 1:
            channel = before.channel
            voice_state.stop() # Stops the audio
            await voice_state.disconnect() # Disconnects the bot

    # Forced Leaving
    if member.id == BotID and after.channel != None: 
        if after.channel.id != DomainAddress:
            channel = before.channel
            voice_state.stop()
            discon = await voice_state.disconnect(force=True)

# Voice loop
async def play_source(voice_client, channel):
    # Ensures no errors when disconnecting the bot
    if channel.id == DomainAddress and len(channel.members) != 1:
        await asyncio.sleep(0.5)
        source = FFmpegPCMAudio("Files/PM.wav")
        voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else bot.loop.create_task(play_source(voice_client, channel)))

# Token
bot.run(BotToken)
