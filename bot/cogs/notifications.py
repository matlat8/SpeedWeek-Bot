import discord
from discord.ext import commands 
import asyncio

from db import DB

from core.crud.leagues import get_leagues
from core.crud.notifications import insert_notification
from core.embeds.leagues import view_leagues_basic_embed
from core.misc.discord import check

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DB(1, 5)

    @commands.command()
    async def setlaptimenotification(self, ctx):
        conn = self.db.get_conn()
        leagues = get_leagues(conn)
        embed= view_leagues_basic_embed(leagues)
        await ctx.send(embed=embed)

        check_message = lambda m: check(m, ctx)
        
        # Get the league ID from the user
        try:
            message = await self.bot.wait_for('message', check=check_message, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond.')
            return
        league_id = message.content

        await ctx.send('Please mention the channel you would like to set as the notification channel.')
        try:
            message = await self.bot.wait_for('message', check=check_message, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond.')
            return
        channel = message.channel_mentions[0]
        insert_notification(conn, league_id, 'lap_time', channel.guild.id, channel.id)
        pass

    