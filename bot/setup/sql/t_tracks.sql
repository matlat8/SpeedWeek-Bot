CREATE TABLE IF NOT EXISTS tracks (
    id SERIAL PRIMARY KEY,
    g61_id INTEGER UNIQUE,
    ir_id INTEGER UNIQUE,
    category VARCHAR(255),
    track_name VARCHAR(4096),
    config_name VARCHAR(4096),
    is_dirt BOOLEAN,
    is_oval BOOLEAN,
    is_ps_purchasable BOOLEAN,
    location VARCHAR(4096),
    price FLOAT,
    price_display VARCHAR(4096),
    purchasable BOOLEAN,
    track_config_length FLOAT,
    free_with_subscription BOOLEAN
)