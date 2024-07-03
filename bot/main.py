import discord
from discord.ext import commands
import discordhealthcheck
import asyncpg

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
from core.logger import setup_logger

TOKEN = os.environ.get('DISCORD_TOKEN')

logger = setup_logger(__name__)

intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(name=f"{os.environ.get('DISCORD_COMMAND_PREFIX')}help - v{__version__}", type=discord.ActivityType.listening)
bot = commands.Bot(command_prefix=os.environ.get('DISCORD_COMMAND_PREFIX'), intents=intents, activity=activity)

setup_database()

class Database(commands.Cog): 
    def __init__(self, bot):
        self.bot = bot
        self.pool = None

    async def connect(self):
        self.pool = await asyncpg.create_pool(dsn=os.environ.get('POSTGRES_URL'))

    async def close(self):
        await self.pool.close()

    async def get_connection(self):
        if self.pool is None:
           await self.connect() 
        return await self.pool.acquire()
    
    async def release_connection(self, connection):
        await self.pool.release(connection)

database = Database(bot)

@bot.event
async def on_ready():
    await load_cogs()
    healthcheck_server = await discordhealthcheck.start(bot)
    #await bot.loop.run_until_complete(load_cogs())
    print(f'Logged in as {bot.user}')

@bot.event
async def on_connect():
    await database.connect()

@bot.event
async def on_disconnect():
    await database.close()

async def load_cogs():
    await bot.add_cog(Database(bot))
    await bot.add_cog(LeagueCommands(bot))
    await bot.add_cog(SeasonCommands(bot))
    await bot.add_cog(WeeksCommands(bot))
    await bot.add_cog(Notifications(bot))
    await bot.add_cog(CarsCommands(bot))
    await bot.add_cog(TracksCommands(bot))
    logger.info('Cogs loaded')



bot.run(TOKEN)

