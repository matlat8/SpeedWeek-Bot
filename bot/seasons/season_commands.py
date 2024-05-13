from discord.ext import commands

from db import DB

class SeasonCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB(1,5)

    @commands.command()
    async def createseason(self, ctx):
        conn = self.db.get_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM leagues')
        leagues = cur.fetchall()
        await ctx.send('What league would you like to create a new season for?')
        for league in leagues:
            await ctx.send(f'')



        msg = await self.bot.wait_for('message', check=self.check(ctx))

        await ctx.send(f'Creating season... {msg.content}')

    @commands.command()
    async def viewseasons(self, ctx):
        await ctx.send('Viewing seasons...')

    @commands.command()
    async def joinseason(self, ctx):
        pass

    @commands.command()
    async def editseason(self, ctx, season_id):
        await ctx.send(f'Editing season {season_id}...')

    def check(self, m, ctx):
        return m.author == ctx.author and m.channel == ctx.channel