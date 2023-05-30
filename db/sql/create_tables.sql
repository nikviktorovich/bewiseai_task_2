CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR UNIQUE,
    access_token UUID UNIQUE
);

CREATE TABLE IF NOT EXISTS audio (
    uuid UUID PRIMARY KEY,
    user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);