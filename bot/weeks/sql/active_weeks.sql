select
    w.id as week_id,
    season_id,
    car_id,
    track_id,
    w.start_date as week_start_date,
    league_id,
    season_num,
    name,
    g61_team_id
from weeks w
    left join seasons s
        on w.season_id = s.id
    left join leagues l
        on s.league_id = l.id
where
    w.start_date <= current_date
and w.end_date >= current_date
and league_id = %s