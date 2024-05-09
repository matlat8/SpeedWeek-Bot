CREATE TABLE IF NOT EXISTS weeks (
    id SERIAL PRIMARY KEY,
    season_id integer not null,
    week_num INTEGER not null,
    car_id INTEGER not null,
    track_id INTEGER not null,
    start_date DATE not null,
    end_date DATE not null,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
