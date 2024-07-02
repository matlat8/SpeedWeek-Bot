import discord
from discord.ext import commands
import discordhealthcheck

import os
import asyncio

from version import __version__
from setup.setup import setup_database 
from leagues import LeagueCommands
from seasons import SeasonCommands
from weeks import WeeksCommands
from cogs.notifications import Notifications
from cogs.cars_cog import CarsCommands
from cogs.tracks_cog import TracksCommands

TOKEN = os.environ.get('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(name=f"{os.environ.get('DISCORD_COMMAND_PREFIX')}help - v{__version__}", type=discord.ActivityType.listening)
bot = commands.Bot(command_prefix=os.environ.get('DISCORD_COMMAND_PREFIX'), intents=intents, activity=activity)

setup_database()

@bot.event
async def on_ready():
    healthcheck_server = await discordhealthcheck.start(bot)
    await bot.add_cog(LeagueCommands(bot))
    await bot.add_cog(SeasonCommands(bot))
    await bot.add_cog(WeeksCommands(bot))
    await bot.add_cog(Notifications(bot))
    await bot.add_cog(CarsCommands(bot))
    await bot.add_cog(TracksCommands(bot))
    print(f'{bot.user} has connected to Discord!')


bot.run(TOKEN)

