Create TABLE Users (
    id INT PRIMARY KEY,
    name TEXT UNIQUE,
    password_hash TEXT,
)