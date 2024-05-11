from discord.ext import commands

class SeasonCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def createseason(self, ctx):

        await ctx.send('What league would you like to create a new season for?')

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