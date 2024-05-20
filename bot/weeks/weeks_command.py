from discord.ext import commands, tasks
import arrow
from db import DB

from .weeks_tasks import WeeksTasks

class WeeksCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB(1, 5)
        self.weeks_tasks = WeeksTasks(bot)

    @commands.command()
    async def newweek(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        conn = self.db.get_conn()
        cursor = conn.cursor()

        ## Get the League ID
        cursor.execute('SELECT id, name FROM leagues')
        leagues = cursor.fetchall()
        await ctx.send('Enter the league ID for the week you would like to create.')
        for league in leagues:
            await ctx.send(f'ID: {league[0]} --> Name: {league[1]}')
        league_id = await self.bot.wait_for('message', check=check)

        ## Get the active season
        cursor.execute('SELECT id FROM seasons WHERE league_id = %s AND end_date >= now()', (league_id.content,))
        season_id = cursor.fetchone()
        if season_id is None:
            await ctx.send('No active season found for the selected league.')
            return
        print(season_id)
        
        ## Get the week number
        cursor.execute('SELECT MAX(week_num) FROM weeks WHERE season_id = %s', (season_id))
        week_num = cursor.fetchone()
        week_num = week_num[0] + 1 if week_num[0] is not None else 1

        ## Get the start and end date of the week
        start_date = arrow.now().floor('week')
        end_date = arrow.now().ceil('week')

        await ctx.send('What car are you using this week? Enter the Garage61 Car ID, found in the URL of the search G61 app page.') ## lazily doing this for now. will eventually copy the G61 /tracks and /cars endpoints to abstract ID's for this
        car_id = await self.bot.wait_for('message', check=check)
        try:
            car_id = int(car_id.content)
        except ValueError:
            await ctx.send('Invalid car ID.')
            return
        await ctx.send('What track are you racing on this week? Enter the Garage61 Track ID, found in the URL of the search G61 app page.')
        track_id = await self.bot.wait_for('message', check=check)
        
        try:
            track_id = int(track_id.content)
        except ValueError:
            await ctx.send('Invalid track ID.')
            return
        
        cursor.execute('INSERT INTO weeks (season_id, week_num, start_date, end_date, car_id, track_id) VALUES (%s, %s, %s, %s, %s, %s)', (season_id[0], week_num, start_date.format('YYYY-MM-DD'), end_date.format('YYYY-MM-DD'), car_id, track_id))
        conn.commit()
    
        await ctx.send('Created new week')
        self.db.release_conn(conn)