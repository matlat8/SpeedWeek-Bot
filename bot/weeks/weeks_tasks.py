from discord.ext import tasks
import aiohttp
from db import DB
import aiohttp
import os
import arrow

from .embeds import WeekEmbeds

class WeeksTasks:
    def __init__(self, bot):
        self.bot = bot
        self.db = DB(1, 5)
        self.check_weeks.start()
        self.embeds = WeekEmbeds()

    @tasks.loop(minutes=2)
    async def check_weeks(self):
        conn = self.db.get_conn()
        cur = conn.cursor()
        sql = """
SELECT w.id AS week_id,
       season_id,
       week_num,
       car_id,
       track_id,
       w.start_date,
       w.end_date,
       g61_team_id,
       l.id AS league_id
FROM weeks w
LEFT JOIN seasons s
    ON w.season_id = s.id
LEFT JOIN leagues l
    ON s.league_id = l.id
WHERE w.start_date <= CURRENT_DATE
  AND w.end_date >= CURRENT_DATE
  """
        cur.execute(sql)
        week_params = cur.fetchall()
        if week_params is None:
            return
        
        for week in week_params:
            laps = await self.get_week_laps(week[4], week[3], week[7], week[5])
            if laps is not None and 'items' in laps:
                for index, lap in enumerate(laps['items']):
                    lap['rank'] = index + 1
                    lap['week_id'] = week[0]
                    lap['season_id'] = week[1]
                    lap['league_id'] = week[8]
                    action = await self.insert_results(conn, lap)
                    print(action)
                    # If the time was the same, do nothing
                    if action == 'no action':
                        continue
                    
                    sql = "SELECT guild_id, channel_id from notifications WHERE league_id = %s AND notification_type =  'lap_time'"
                    cur.execute(sql, (lap['league_id'],))
                    notifications = cur.fetchone()
                    if notifications is None:
                        continue
                    guild_id, channel_id = notifications
                    channel = self.bot.get_channel(channel_id)
                    with open(os.path.join(os.path.dirname(__file__), 'sql', 'lap_times_for_driver.sql'), 'r') as file:
                        sql = file.read()
    
                    cur.execute(sql, (lap['league_id'], lap['season_id'], lap['week_id'], f'{lap["driver"]["firstName"]} {lap["driver"]["lastName"]}'))
                    position_plus_minus = cur.fetchall()
    
                    if action == 'inserted':
                        msg = self.embeds.initial_laptime_msg(lap, position_plus_minus)
                        await channel.send(msg)
                    if action == 'updated':
                        msg = self.embeds.updated_laptime_msg(lap, position_plus_minus)
                        await channel.send(msg)
        self.db.release_conn(conn)

    async def get_week_laps(self, track_id, car_id, team_id, start_date):
        async with aiohttp.ClientSession() as session:
            start_date = arrow.get(start_date).format('YYYY-MM-DDTHH:mm:ss[Z]')
            url = f"https://garage61.net/api/v1/laps?tracks={track_id}&cars={car_id}&teams={team_id}&after={start_date}&drivers=me"
            headers = {'Authorization': f'Bearer {os.environ.get("GARAGE61_API_KEY")}'}
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"Failed to get week laps. Status code: {response.status}\n{await response.text()}")

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

        
