CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE Projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL,
    project_depreciation_method INT
);

CREATE TABLE ProjectTypes (
    project_id INT PRIMARY KEY,
    project_type TEXT NOT NULL,
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE Investments (
    project_id INT,
    investment_year INT,
    investment_amount REAL,
    PRIMARY KEY (project_id, investment_year),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE Inserted (
    user_id INT,
    project_id INT,
    inserted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE Modified (
    user_id INT,
    project_id INT,
    modified_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);