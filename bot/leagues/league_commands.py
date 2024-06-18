from discord.ext import commands

from .api import LeagueAPI
from core.crud.leagues import new_league, get_leagues
from core.embeds.leagues import view_leagues_basic_embed
from db import DB

class LeagueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB(1, 10)
        self.league_api = LeagueAPI()

    @commands.command()
    async def createleague(self, ctx):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        await ctx.send('Enter the name of the league.')
        league_name = await self.bot.wait_for('message', check=check)

        await ctx.send('Enter your Garage61 team ID.\n\n*Hint: Open Garage61, open your Garage61 team and copy the URL. The team ID is the last part of the URL.*')
        msg = await self.bot.wait_for('message', check=check)

        team_id = msg.content
        lap_check_data = await self.league_api.search_for_team(team_id)
        
        if not any(team['slug'] == team_id for team in lap_check_data['teams']): #check to see if team exists within teams array
            await ctx.send('Invalid team ID.')
            return
        
        conn = self.db.get_conn()
        new_league(conn, league_name.content, team_id)
        conn.commit()
        self.db.release_conn(conn)

        await ctx.send(f'Creating league {league_name.content}... {team_id}')

    @commands.command()
    async def viewleagues(self, ctx):
        conn = self.db.get_conn()
        leagues = get_leagues(conn)
        self.db.release_conn(conn)
        if not leagues:
            await ctx.send('No leagues found.')
            return
        embed = view_leagues_basic_embed(leagues)
        await ctx.send(embed=embed)

        return

    @commands.command()
    async def editleague(self, ctx, league_id):
        await ctx.send(f'Editing league {league_id}...')

    @commands.command()
    async def deleteleague(self, ctx, league_id):
        await ctx.send(f'Deleting league {league_id}...')