Create TABLE Users (
    id INT PRIMARY KEY,
    name TEXT UNIQUE,
    password_hash TEXT,
)

Create TABLE Projects (
    project_id INT PRIMARY KEY,
    project_name TEXT,
    project_depreciation_method INT
)

Create TABLE Investments (
    project_id INT,
    investment_year INT,
    investment_amount REAL
)

Create TABLE Inserted (
    user_id INT,
    project_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
)

Create TABLE Modified (
    user_id INT,
    project_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)

)