from discord.ext import commands
import arrow
from db import DB

class SeasonCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB(1,5)

    @commands.command()
    async def createseason(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        conn = self.db.get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM leagues')
        leagues = cur.fetchall()
        await ctx.send('What league would you like to create a new season for? Enter the ID of the league.')
        for league in leagues:
            await ctx.send(f'ID: {league[0]} --> Name: {league[1]}')

        selected_league_id = await self.bot.wait_for('message', check=check)

        await ctx.send('Enter the start date of the season in the format YYYY-MM-DD')
        start_date = await self.bot.wait_for('message', check=check)
        await ctx.send('Enter the end date of the season in the format YYYY-MM-DD')
        end_date = await self.bot.wait_for('message', check=check)

        # calculate how many mondays are between the start and end date
        start_date = arrow.get(start_date.content).floor('week')
        end_date = arrow.get(end_date.content).floor('week')
        weeks = (end_date - start_date).days / 7
        print(weeks)

        await ctx.send(f'Your season will be {weeks} weeks long. Confirm? (yes/no)')
        confirm = await self.bot.wait_for('message', check=check)
        if confirm.content.lower() != 'yes':
            await ctx.send('Season creation cancelled.')
            return
        
        cur.execute('SELECT coalesce(max(season_num), 0) + 1 FROM seasons WHERE league_id = %s', (selected_league_id.content,)) # this feels so sloppy to do but it gets the job done. if the league ID is not found, it still returns 1
        season_num = cur.fetchone()
        cur.execute('INSERT INTO seasons (league_id, season_num, start_date, end_date) values (%s, %s, %s, %s)', (selected_league_id.content, season_num, start_date.format('YYYY-MM-DD'), end_date.format('YYYY-MM-DD')))
        conn.commit()

        ## TODO add a way to check if there is an ongoing season for the league

        self.db.release_conn(conn)
        await ctx.send('Season created.')
        

        

    @commands.command()
    async def viewseasons(self, ctx, *args):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        conn = self.db.get_conn()
        cur = conn.cursor()

        if not args:
            cur.execute('SELECT id, name FROM leagues')
            leagues = cur.fetchall()
            await ctx.send('What league would you like to view seasons for? Enter the ID of the league.')
            for league in leagues:
                await ctx.send(f'ID: {league[0]} --> Name: {league[1]}')
            selected_league_id = await self.bot.wait_for('message', check=check)
        else:
            try:
                selected_league_id = int(args[0])
            except ValueError:
                await ctx.send('Invalid league ID.')
                return

        cur.execute('SELECT * FROM seasons WHERE league_id = %s', (selected_league_id.content,))
        seasons = cur.fetchall()
        if not seasons:
            await ctx.send('No seasons found for this league.')
            return
        else:
            for season in seasons:
                await ctx.send(f'Season ID: {season[0]}\nSeason Number: {season[2]}\nStart Date: {season[3]}\nEnd Date: {season[4]}')
        

    @commands.command()
    async def joinseason(self, ctx):
        pass

    @commands.command()
    async def editseason(self, ctx, season_id):
        await ctx.send(f'Editing season {season_id}...')

    