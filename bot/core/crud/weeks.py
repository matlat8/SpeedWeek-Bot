from core.crud.utils import fetchall_as_dict

def get_active_weeks(conn):
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
    cursor = conn.cursor()
    cursor.execute(sql)
    weeks = fetchall_as_dict(cursor)
    return weeks