drop table if exists user_songs;
CREATE TABLE user_songs(
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    title,
    score INTEGER,
    created_at DEFAULT CURRENT_TIMESTAMP,
    image_id INTEGER,
    record_id INTEGER
);