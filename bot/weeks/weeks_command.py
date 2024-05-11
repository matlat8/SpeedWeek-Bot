from discord.ext import commands, tasks

from db import DB

class WeeksCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB()

