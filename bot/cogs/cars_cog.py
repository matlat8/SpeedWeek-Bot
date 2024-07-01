from discord.ext import commands

from db import DB
from tasks.load_cars_task import load_cars

class CarsCommands(commands.Cog):
    def __init__(self, bot):
        load_cars.start(bot)

