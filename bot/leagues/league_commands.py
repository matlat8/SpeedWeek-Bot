from discord.ext import commands

from db import DB

class LeagueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB(1, 10)

    @commands.command()
    async def createleague(self, ctx, *args):
        # convert the args array to a string
        league_name = ' '.join(args)

        await ctx.send('Enter your Garage61 team ID.\n\n*Hint: Open Garage61, open your Garage61 team and copy the URL. The team ID is the last part of the URL.*')

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await self.bot.wait_for('message', check=check)
        team_id = msg.content
        await ctx.send(f'Creating league {league_name}... {team_id}')

    @commands.command()
    async def viewleagues(self, ctx):
        await ctx.send('Viewing leagues...')

    @commands.command()
    async def editleague(self, ctx, league_id):
        await ctx.send(f'Editing league {league_id}...')

    @commands.command()
    async def deleteleague(self, ctx, league_id):
        await ctx.send(f'Deleting league {league_id}...')