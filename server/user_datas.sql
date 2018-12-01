drop table if exists user_datas;
CREATE TABLE user_datas(
    id INTEGER PRIMARY KEY,
    user_name,
    user_password,
    created_at DEFAULT CURRENT_TIMESTAMP
);