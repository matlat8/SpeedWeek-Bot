from discord.ext import tasks
import aiohttp
from db import DB
import aiohttp
import os
import arrow

from .embeds import WeekEmbeds
from core.crud.weeks import get_active_weeks, upsert_laptime
from core.crud.notifications import get_notifications_for_league_for_laptime
from core.garage.laps import get_week_laps
from core.logger import setup_logger

logger = setup_logger(__name__)

class WeeksTasks:
    def __init__(self, bot):
        self.bot = bot
        self.db = DB(1, 5)
        self.check_weeks.start()
        self.embeds = WeekEmbeds()

    @tasks.loop(minutes=2)
    async def check_weeks(self):
        logger.debug('Checking for new lap times')
        conn = self.db.get_conn()
        cur = conn.cursor()
        week_params = get_active_weeks(conn)
        if week_params is None:
            return
        logger.debug(f'Found {len(week_params)} active weeks')

        # Loop through the active weeks
        for week in week_params:
            # Call the G61 API to get the laps for the week
            laps = await get_week_laps(week['track_id'], week['car_id'], week['g61_team_id'], week['start_date'])
            if laps is not None and 'items' in laps:
                logger.debug(f'Found {len(laps["items"])} laps for week id {week["week_id"]}')
                for index, lap in enumerate(laps['items']):
                    lap['rank'] = index + 1
                    lap['week_id'] = week['week_id']
                    lap['season_id'] = week['season_id']
                    lap['league_id'] = week['league_id']
                    action = await self.insert_results(conn, lap)
                    # If the time was the same, do nothing
                    if action == 'no action':
                        continue
                    
                    notifications = get_notifications_for_league_for_laptime(conn, week['league_id'])
                    # if there are no notifications for the league, do nothing
                    if notifications is None:
                        continue
                    channel = self.bot.get_channel(notifications['channel_id'])
                    if channel is None:
                        continue
                    with open(os.path.join(os.path.dirname(__file__), 'sql', 'lap_times_for_driver.sql'), 'r') as file:
                        sql = file.read()

                    cur.execute(sql, (lap['league_id'], lap['season_id'], lap['week_id'], f'{lap["driver"]["firstName"]} {lap["driver"]["lastName"]}'))
                    position_plus_minus = cur.fetchall()

                    if action == 'inserted':
                        logger.debug(f'New lap time for {lap["driver"]["firstName"]} {lap["driver"]["lastName"]}')
                        msg = self.embeds.initial_laptime_msg(lap, position_plus_minus)
                        await channel.send(msg)
                    if action == 'updated':
                        logger.debug(f'Updated lap time for {lap["driver"]["firstName"]} {lap["driver"]["lastName"]}')
                        msg = self.embeds.updated_laptime_msg(lap, position_plus_minus)
                        await channel.send(msg)
        self.db.release_conn(conn)

    async def insert_results(self, conn, lap):
        cur = conn.cursor()

        cur.execute('SELECT id, lap_time, garage_lapid FROM results WHERE league_id = %s AND season_id = %s AND week_id = %s AND driver_name = %s', (lap['league_id'], lap['season_id'], lap['week_id'], f'{lap["driver"]["firstName"]} {lap["driver"]["lastName"]}'))
        current_lap = cur.fetchone()
        if not current_lap:
            sql = """
                INSERT INTO results (league_id, season_id, week_id, driver_name, lap_time, garage_lapid, last_updated)
                VALUES (%s, %s, %s, %s, %s, %s,NOW())
            """
            cur.execute(sql, (lap['league_id'], lap['season_id'], lap['week_id'], f'{lap["driver"]["firstName"]} {lap["driver"]["lastName"]}', lap['lapTime'], lap['id']))
            conn.commit()
            return 'inserted'
        
        if current_lap[2] == lap['id']:
            return 'no action'
        else:
            sql = """
                UPDATE results
                SET lap_time = %s, garage_lapid = %s, last_updated = NOW()
                WHERE league_id = %s AND season_id = %s AND week_id = %s AND driver_name = %s
            """
            lap_time = f'{lap["lapTime"]}'
            cur.execute(sql, (lap_time, lap['id'], lap['league_id'], lap['season_id'], lap['week_id'], f'{lap["driver"]["firstName"]} {lap["driver"]["lastName"]}'))
            conn.commit()
            return 'updated'

        
