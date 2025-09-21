from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
import service_functions
import sqlite3
import db
import config
import markupsafe

app = Flask(__name__)
app.config["SECRET_KEY"] = config.secret_key

def users_exists():
    
    sql = "SELECT COUNT(*) FROM Users"
    con = db.get_connection()
    try:
        result = con.execute(sql)
        count = result.fetchone()[0]
        return count > 0
    except sqlite3.OperationalError:
        return None
    finally:
        con.close()

with app.app_context():
    if users_exists() is None:
        db.init_db()

protected_routes = [
    'new_project',
    'list_projects',
    'cashflow_project',
    'add_new_cashflow',
    'delete_project'
]

def login_required():
    if "user_id" not in session:
        return redirect(url_for("login"))

@app.before_request
def before_request():
    if request.endpoint in protected_routes:
        return login_required()

@app.route("/")
def user_check():
    exists = users_exists()
    if exists:
        return redirect(url_for("login"))
    else:
        return redirect(url_for("register"))
    
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = service_functions.get_user_by_username(username)
        if not user:
            return "Virhe: käyttäjää ei löydy"

        user_id, password_hash = user

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/main_layout")
        else:
            return "Virhe: salasana väärin"

    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/main_layout")
def main_layout():
    return render_template("main_layout.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form.get("username")
    password1 = request.form.get("password1")
    password2 = request.form.get("password2")

    if not username or not password1 or not password2:
        return "VIRHE: kaikki kentät on täytettävä"

    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    password_hash = generate_password_hash(password1)

    success = service_functions.add_user_to_db(username, password_hash)
    if not success:
        return "VIRHE: tunnus on jo varattu"

    return render_template("post_register.html")

@app.route("/post_register_redirect", methods=["POST"])
def post_register_redirect():
    next_page = request.form.get("next", "login")
    if next_page not in ("login", "main_layout"):
        next_page = "login"
    return redirect(url_for(next_page))

@app.route("/new_project", methods=["GET", "POST"])
def new_project():

    all_classes = service_functions.get_all_classes()

    if request.method == "POST":
        project_name = request.form["project_name"]
        classes = []

        for entry in request.form.getlist("classes"):
            if entry:
                class_title, class_value = entry.split(":")
                if class_title not in all_classes:
                    abort(403)
                if class_value not in all_classes[class_title]:
                    abort(403)
                classes.append((class_title, class_value))

        user_id = session.get("user_id")
        if not user_id:
            abort(403)

        project_id = service_functions.insert_project(project_name, classes, user_id)

        return render_template(
            "main_layout.html",
            message=f"Projekti {project_name} tallennettu tunnuksella {project_id}"
        )

    next_id = service_functions.get_next_project_id()
    return render_template("new_project.html", next_id=next_id, all_classes=all_classes)

@app.route("/list_projects", methods=["GET"])
def list_projects():

    search_name = request.args.get("project_name", "").strip()

    query_projects = service_functions.get_projects(search_name if search_name else None)
    
    projects = []

    for row in query_projects:
        project_id = row["project_id"]
        project_name = row["project_name"]

        definitions_rows = service_functions.get_project_definitions(project_id)
        definitions = {}
        for d in definitions_rows:
            title = d["title"]
            value = d["value"]
            if title not in definitions:
                definitions[title] = []
            definitions[title].append(value)
        
        for title in definitions:
            if len(definitions[title]) == 1:
                definitions[title] = definitions[title][0]

        project = {
            "project_id": project_id,
            "project_name": project_name,
            "definitions": definitions
        }
        projects.append(project)

    return render_template("list_projects.html", projects=projects)

@app.route("/cashflow_project/<int:project_id>")
def cashflow_project(project_id):

    investments = service_functions.get_project_by_id(project_id)

    return render_template(
        'cashflow_project.html',
        project_id=project_id,
        investments=investments
    )

@app.route("/delete_project/<int:project_id>")
def delete_project(project_id):

    service_functions.delete_project_by_id(project_id)
    flash(f"Projekti {project_id} poistettu")

    return redirect(url_for("list_projects"))

@app.route('/add_new_cashflow/<int:project_id>', methods=['GET', 'POST'])
def add_new_cashflow(project_id):

    if request.method == 'POST':
        investment_year = request.form['investment_year']
        investment_amount = request.form['investment_amount']
        
        service_functions.add_cashflow(project_id, investment_year, investment_amount)

        return redirect(url_for('cashflow_project', project_id=project_id))

    return render_template('add_new_cashflow.html', project_id=project_id)

@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)