from discord.ext import tasks
import aiohttp
from db import DB
import aiohttp
import os

class WeeksTasks:
    def __init__(self, bot):
        self.bot = bot
        self.db = DB(1, 5)
        self.check_weeks.start()

    @tasks.loop(hours=1)
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
    ON s.league_id = w.id
WHERE w.start_date <= CURRENT_DATE
  AND w.end_date >= CURRENT_DATE
  """
        cur.execute(sql)
        week_params = cur.fetchall()
        if week_params is None:
            return
        
        print(week_params)
        for week in week_params:
            laps = await self.get_week_laps(week[4], week[3], week[7])
            for lap in laps['items']:
                lap['week_id'] = week[0]
                lap['season_id'] = week[1]
                lap['league_id'] = week[8]
                await self.insert_results(conn, lap)

    async def get_week_laps(self, track_id, car_id, team_id):
        async with aiohttp.ClientSession() as session:

            url = f"https://garage61.net/api/v1/laps?tracks={track_id}&cars={car_id}&teams={team_id}"
            headers = {'Authorization': f'Bearer {os.environ.get("GARAGE61_API_KEY")}'}
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"Failed to get week laps. Status code: {response.status}\n{await response.text()}")

    async def upsert_results(self, lap):
        conn = self.db.get_conn()
        cur = conn.cursor()
        sql = """
            INSERT INTO lapdata (lap_id, lap_time, driver_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (lap_id) DO UPDATE
            SET lap_time = EXCLUDED.lap_time, driver_id = EXCLUDED.driver_id
        """
        params = (lap['lap_id'], lap['lap_time'], lap['driver_id'])
        cur.execute(sql, params)
        conn.commit()

    async def insert_results(self, conn, lap):
        conn = self.db.get_conn()
        cur = conn.cursor()

        cur.execute('SELECT id, lap_time FROM results WHERE league_id = %s AND season_id = %s AND week_id = %s AND driver_name = %s', (lap['league_id'], lap['season_id'], lap['week_id'], f'{lap["driver"]["firstName"]} {lap["driver"]["lastName"]}'))
        current_lap = cur.fetchone()
        if not current_lap:
            sql = """
                INSERT INTO results (league_id, season_id, week_id, driver_name, lap_time, last_updated)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """
            cur.execute(sql, (lap['league_id'], lap['season_id'], lap['week_id'], f'{lap["driver"]["firstName"]} {lap["driver"]["lastName"]}', lap['lapTime']))
            conn.commit()
            self.db.release_conn(conn)
            return
        if current_lap[1] == lap['lapTime']:
            return
        else:
            sql = """
                UPDATE results
                SET lap_time = %s, last_updated = NOW()
                WHERE league_id = %s AND season_id = %s AND week_id = %s AND driver_name = %s
            """
            cur.execute(sql, (lap['lapTime'], lap['league_id'], lap['season_id'], lap['week_id'], f'{lap["driver"]["firstName"]} {lap["driver"]["lastName"]}'))
            conn.commit()
            self.db.release_conn(conn)
        
        #params = (lap['lap_id'], lap['lap_time'], lap['driver_id'])
        #cur.execute(sql, params)
        #conn.commit()
