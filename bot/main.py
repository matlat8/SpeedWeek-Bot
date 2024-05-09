import discord
from discord.ext import commands

import os
import asyncio

TOKEN = os.environ.get('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(name=f"{os.environ.get('DISCORD_COMMAND_PREFIX')}driver help - v{__version__}", type=discord.ActivityType.listening)
bot = commands.Bot(command_prefix=os.environ.get('DISCORD_COMMAND_PREFIX'), intents=intents, activity=activity)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


bot.run(TOKEN)

