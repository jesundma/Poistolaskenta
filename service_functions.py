"""
All sql functions here, app.py should be clean and contain only logic for required data, 
presenting data and rendering pages.
"""
from db import execute, query, last_insert_id

def get_next_project_id():
    result = query("SELECT MAX(project_id) AS max_id FROM Projects")
    max_id = result[0]["max_id"]
    if max_id is None:
        return 1
    return max_id + 1

def insert_project(project_name: str, project_depreciation_method: int):
    execute(
        "INSERT INTO Projects (project_name, project_depreciation_method) VALUES (?, ?)",
        [project_name, project_depreciation_method]
    )
    return last_insert_id()

def get_projects():
    sql = "SELECT project_id, project_name, project_depreciation_method FROM Projects"
    result = query(sql)
    return result

def get_project_by_id(project_id):

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
