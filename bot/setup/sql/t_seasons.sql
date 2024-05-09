CREATE TABLE IF NOT EXISTS seasons (
    id SERIAL PRIMARY KEY,
    league_id integer not null,
    season_num INTEGER not null,
    start_date DATE not null,
    end_date DATE not null,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);