"""
All sql functions here, app.py should be clean and contain only logic for required data, 
presenting data and rendering pages.
"""
from db import execute, query, last_insert_id
import sqlite3

def get_next_project_id():
    result = query("SELECT MAX(project_id) AS max_id FROM Projects")
    max_id = result[0]["max_id"]
    if max_id is None:
        return 1
    return max_id + 1

def insert_project(project_name: str, classes: list[tuple[str, str]], inserting_user: int):

    """
    Insert a project and its class definitions.

    :param project_name: Name of the project
    :param classes: List of (title, value) pairs for project definitions
    :param inserting_user: ID of the user creating the project
    :return: ID of the newly created project
    """

    execute(
        "INSERT INTO Projects (project_name) VALUES (?)",
        [project_name]
    )
    project_id = last_insert_id()

    sql = "INSERT INTO project_definitions (project_id, title, value) VALUES (?, ?, ?)"
    for class_title, class_value in classes:
        execute(sql, [project_id, class_title, class_value])
    
    execute(
        "INSERT INTO Inserted (inserting_user, project_id) VALUES (?, ?)",
        [inserting_user, project_id]
    )

    return project_id

def get_projects(search_name=None, search_type=None, search_method=None):
    sql = """
        SELECT p.project_id, p.project_name
        FROM Projects p
        LEFT JOIN Project_definitions d1 
            ON p.project_id = d1.project_id AND d1.title = 'Projektityyppi'
        LEFT JOIN Project_definitions d2 
            ON p.project_id = d2.project_id AND d2.title = 'Poistomenetelmä'
        WHERE 1=1
    """
    params = []

    if search_name:
        sql += " AND p.project_name LIKE ?"
        params.append(f"%{search_name}%")

    if search_type:
        sql += " AND d1.value = ?"
        params.append(search_type)

    if search_method:
        sql += " AND d2.value = ?"
        params.append(search_method)

    return query(sql, params)

def get_project_definitions(project_id: int):

    sql = """
        SELECT title, value
        FROM project_definitions
        WHERE project_id = ?
        ORDER BY id
    """

    result = query(sql, [project_id])
    
    return [{"title": row["title"], "value": row["value"]} for row in result]

def get_project_by_id(project_id):

    sql = '''
        SELECT project_id, project_name
        FROM Projects
        WHERE project_id = ?
    '''
    rows = query(sql, (project_id,))
    return rows[0] if rows else None

def get_project_investments(project_id):

    sql = '''
        SELECT investment_year, investment_amount 
        FROM Investments 
        WHERE project_id = ?
    '''
    investments = query(sql, (project_id,))
    
    return investments

def add_cashflow(project_id, investment_year, investment_amount):
    sql = '''
        INSERT INTO Investments (project_id, investment_year, investment_amount) 
        VALUES (?, ?, ?)
    '''
    execute(sql, (project_id, investment_year, investment_amount))

def update_project(project_id, project_name, classes, modifying_user: int):

    execute(
        "UPDATE Projects SET project_name = ? WHERE project_id = ?",
        (project_name, project_id)
    )

    execute(
        "DELETE FROM Project_definitions WHERE project_id = ?",
        (project_id,)
    )

    for title, value in classes:
        execute(
            "INSERT INTO Project_definitions (project_id, title, value) VALUES (?, ?, ?)",
            (project_id, title, value)
        )
    
    execute(        
        "INSERT INTO Modified (modifying_user, project_id) VALUES (?, ?)",
        [modifying_user, project_id]
    )

def delete_project_by_id(project_id: int):

    execute("DELETE FROM Project_definitions WHERE project_id = ?", [project_id])

    execute("DELETE FROM Inserted WHERE project_id = ?", [project_id])

    execute("DELETE FROM Projects WHERE project_id = ?", [project_id])

def get_all_classes():

    sql = "SELECT title, value FROM classes ORDER BY id"
    result = query(sql)

    classes = {}
    for title, value in result:
        if title not in classes:
            classes[title] = []
        classes[title].append(value)

    return classes

def get_project_creator(project_id):

    sql = """
        SELECT u.id AS user_id, u.username AS username, i.inserted_at AS time
        FROM Inserted i
        JOIN Users u ON i.inserting_user = u.id
        WHERE i.project_id = ?
    """
    result = query(sql, (project_id,))
    if result:
        return {
            "user_id": result[0]["user_id"],
            "user": result[0]["username"],
            "time": result[0]["time"]
        }
    return None

def add_user_to_db(username: str, password_hash: str) -> bool:

    sql = "INSERT INTO Users (username, password_hash) VALUES (?, ?)"
    try:
        execute(sql, [username, password_hash])
        return True
    except sqlite3.IntegrityError:
        return False

def get_user_by_username(username: str):

    sql = "SELECT id, password_hash FROM Users WHERE username = ?"
    row = query(sql, [username])
    if row:
        return row[0]
    return None