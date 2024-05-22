CREATE TABLE IF NOT EXISTS notifications(
    id SERIAL PRIMARY KEY,
    league_id INTEGER NOT NULL,
    notification_type VARCHAR(255) NOT NULL,
    guild_id BIGINT NOT NULL,
    channel_id BIGINT NOT NULL,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)