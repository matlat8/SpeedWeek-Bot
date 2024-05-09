CREATE TABLE IF NOT EXISTS leagues (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) not null,
    g61_team_id VARCHAR(255),
    first_day_of_week integer,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
)