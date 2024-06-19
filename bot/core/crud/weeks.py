from core.crud.utils import fetchall_as_dict

def get_active_weeks(conn):
    sql = """
SELECT w.id AS week_id, -- 0
       season_id, -- 1
       week_num, --2
       car_id, --3
       track_id, -- 4
       w.start_date, --5
       w.end_date, -- 6
       g61_team_id,-- 7
       l.id AS league_id --8
FROM weeks w
LEFT JOIN seasons s
    ON w.season_id = s.id
LEFT JOIN leagues l
    ON s.league_id = l.id
WHERE w.start_date <= CURRENT_DATE
  AND w.end_date >= CURRENT_DATE
  """
    cursor = conn.cursor()
    cursor.execute(sql)
    weeks = fetchall_as_dict(cursor)
    return weeks

async def upsert_laptime(conn, lap):
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