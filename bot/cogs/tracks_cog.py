from discord.ext import commands

from tasks.load_tracks_task import load_tracks

class TracksCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_tracks.start(self.bot)