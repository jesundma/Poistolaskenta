"""
All sql functions here, app.py should be clean and contain only logic for required data, 
presenting data and rendering pages.
"""
from db import execute, query, last_insert_id, get_connection
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

    sql = """
        SELECT project_id, project_name
        FROM Projects
        WHERE project_id = ?
    """
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

def get_project_modifications(project_id: int):
    sql = """
        SELECT 
            u.username AS user, 
            m.modified_at AS time,
            m.modification_type AS modification
        FROM Modified m
        JOIN Users u ON m.modifying_user = u.id
        WHERE m.project_id = ?
        ORDER BY m.modified_at DESC
    """
    return query(sql, (project_id,))

def log_modification(project_id: int, modifying_user: int, modification_type: str):

    sql = """
        INSERT INTO Modified (modifying_user, project_id, modification_type)
        VALUES (?, ?, ?)
    """
    execute(sql, (modifying_user, project_id, modification_type))

def add_cashflow(project_id, investment_year, investment_amount, modifying_user: int):
    sql = '''
        INSERT INTO Investments (project_id, investment_year, investment_amount) 
        VALUES (?, ?, ?)
        ON CONFLICT (project_id, investment_year) DO UPDATE SET
            investment_amount = excluded.investment_amount
    '''
    execute(sql, (project_id, investment_year, investment_amount))

    log_modification(project_id, modifying_user, "Kassavirtoja lisätty")

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
    
    log_modification(project_id, modifying_user, "Projektin tietoja päivitetty")

def delete_project_by_id(project_id: int):
    # individual deletion from each table, SQLite3 ON CASCADE did not work
    execute("DELETE FROM Project_definitions WHERE project_id = ?", [project_id])
    execute("DELETE FROM Inserted WHERE project_id = ?", [project_id])
    execute("DELETE FROM Modified WHERE project_id = ?", [project_id])
    execute("DELETE FROM Investments WHERE project_id = ?", [project_id])
    execute("DELETE FROM ProjectPermissions WHERE project_id = ?", [project_id])

    execute("DELETE FROM Projects WHERE project_id = ?", [project_id])

def add_user_to_db(username: str, password_hash: str) -> bool:
    sql = "INSERT INTO Users (username, password_hash) VALUES (?, ?)"
    con = get_connection()
    try:
        execute(sql, [username, password_hash])
        return True
    except sqlite3.IntegrityError:
        con.rollback()
        return False
    
def get_user_by_username(username: str):

    sql = "SELECT id, password_hash FROM Users WHERE username = ?"
    row = query(sql, [username])
    if row:
        return row[0]
    return None

def get_all_users():
    sql = "SELECT id, username FROM Users"
    return query(sql)

def get_project_creator_id(project_id: int):
    sql = "SELECT inserting_user FROM Inserted WHERE project_id = ?"
    result = query(sql, (project_id,))
    return result[0]["inserting_user"] if result else None

def get_project_permissions(project_id: int):
    sql = """
        SELECT u.id, u.username, 
               COALESCE(pp.can_modify, 0) AS can_modify
        FROM Users u
        LEFT JOIN ProjectPermissions pp 
            ON u.id = pp.user_id AND pp.project_id = ?
        ORDER BY u.username
    """
    return query(sql, (project_id,))

def get_user_project_permission(project_id: int, user_id: int):
    sql = """
        SELECT can_modify
        FROM ProjectPermissions
        WHERE project_id = ? AND user_id = ?
    """
    rows = query(sql, (project_id, user_id))
    return rows[0] if rows else None

def update_project_permissions(project_id, creator_id, permissions):

    sql = """
        INSERT INTO ProjectPermissions (project_id, user_id, can_modify, granted_by)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(project_id, user_id) DO UPDATE SET
            can_modify=excluded.can_modify,
            granted_by=excluded.granted_by,
            granted_at=CURRENT_TIMESTAMP
    """

    execute(sql, (project_id, creator_id, 1, creator_id))

    for user_id, can_modify in permissions.items():
        execute(sql, (project_id, user_id, 1 if can_modify else 0, creator_id))