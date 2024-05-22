CREATE TABLE IF NOT EXISTS results (
    id SERIAL PRIMARY KEY,
    league_id INTEGER NOT NULL,
    season_id INTEGER NOT NULL,
    week_id INTEGER NOT NULL,
    driver_name VARCHAR(255) NOT NULL,
    garage_lapid VARCHAR(255) NOT NULL,
    lap_time FLOAT(7) NOT NULL,
    points INTEGER,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)