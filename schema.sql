CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

CREATE TABLE Projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL
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
    inserting_user INT,
    project_id INT,
    inserted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (inserting_user) REFERENCES Users(id),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE Modified (
    modifying_user INT,
    project_id INT,
    modification_type TEXT,
    modified_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (modifying_user) REFERENCES Users(id),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
);

CREATE TABLE Classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE Project_definitions (
    id INTEGER PRIMARY KEY,
    project_id INTEGER REFERENCES Projects,
    title TEXT,
    value TEXT
);

CREATE TABLE ProjectPermissions (
    project_id INTEGER,
    user_id INTEGER,
    can_modify BOOLEAN NOT NULL DEFAULT 0,
    granted_by INTEGER,
    granted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (project_id, user_id),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id),
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (granted_by) REFERENCES Users(id)
);

CREATE INDEX idx_projects_name ON Projects(project_name);
CREATE INDEX idx_investments_project_id ON Investments(project_id);
CREATE INDEX idx_investments_year ON Investments(investment_year);
CREATE INDEX idx_projdef_project ON Project_definitions(project_id);
CREATE INDEX idx_projdef_title ON Project_definitions(title);