from discord.ext import commands
import os
from db import DB
from core.crud.cars import get_randomcar
from core.crud.tracks import get_randomtrack
from tasks.load_cars_task import load_cars
from cogs.constants import car_categories, car_track_categories

class CarsCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_cars.start(self.bot)

    @commands.command()
    async def randomweek(self, ctx, *args):

        result = await lookup_args(ctx, args)
        if not result:
            return
        category, track_category = result
        # Initialize the database connection
        db = self.bot.get_cog('Database')
        connection = await db.get_connection()

        # Get a random car from the given category
        car = await get_randomcar(connection, category, free_tracks_only=False)
        track = await get_randomtrack(connection, track_category, free_tracks_only=False)
        msg = '**Car Track Combo:**\n'
        msg += f'**Car:** {car["car_name"]}\n'
        msg += f'**Track:** {track["track_name"]} ({track["config_name"]})\n'

        await ctx.send(msg)

    @commands.command()
    async def freerandomweek(self, ctx, *args):
        result = await lookup_args(ctx, args)
        if not result:
            return
        category, track_category = result

        # Initialize the database connection
        db = self.bot.get_cog('Database')
        connection = await db.get_connection()

        # Get a random car from the given category
        car = await get_randomcar(connection, category, free_tracks_only=True)
        track = await get_randomtrack(connection, track_category, free_tracks_only=True)

        msg = '**Car Track Combo:** *(Free)*\n'
        msg += f'**Car:** {car["car_name"]}\n'
        msg += f'**Track:** {track["track_name"]} ({track["config_name"]})\n'
        await ctx.send(msg)

        

async def lookup_args(ctx, args):
    # If no args given, return available categories
    if not args:
        msg = 'Please provide a category. Available categories are:\n'
        for category in car_categories:
            msg += f'- {category}\n'
        msg += f'**Usage:** {os.environ.get("DISCORD_COMMAND_PREFIX")}randomweek <category>'
        await ctx.send(msg)
        return
    category = args[0]
    # Check to see if category passed is valid
    if category not in car_categories:
        msg = 'Invalid category. Available categories are:\n'
        for category in car_categories:
            msg += f'- {category}\n'
        msg += f'\n\n**Usage:** {os.environ.get("DISCORD_COMMAND_PREFIX")}randomweek <category>'
        await ctx.send(msg)
        return
    
    # Lookup the track category for the given car category
    track_category = car_track_categories.get(category)
    if not track_category:
        await ctx.send(f'No track category found for the car category: {category}')
        return
    
    return category, track_category