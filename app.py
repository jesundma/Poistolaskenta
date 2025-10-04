from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
import service_functions
import sqlite3
import db
import config
#import markupsafe # check whether required
import secrets

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
    'edit_project',
    'delete_project'
]

def login_required():
    if "user_id" not in session:
        return redirect(url_for("login"))

def generate_csrf_token():
    token = secrets.token_hex(16)
    session["csrf_token"] = token
    return token

"""
    validate_csrf is helper function, if specific validation from route 
    required. Not called from the code currently.
"""

def validate_csrf():
    form_token = request.form.get("csrf_token")
    return form_token and form_token == session.get("csrf_token")

@app.before_request
def before_request():
    if request.endpoint in protected_routes:
        return login_required()

@app.before_request
def before_request_csrf():
    if request.method in ("POST", "PUT", "DELETE"):
        form_token = request.form.get("csrf_token")
        if not form_token or form_token != session.get("csrf_token"):
            abort(400, description="CSRF tietovirhe")

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
        
    return render_template("login.html", csrf_token=generate_csrf_token())

@app.route("/register")
def register():
    return render_template("register.html", csrf_token=generate_csrf_token())

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
        flash(f"Tunnus on jo varattu, käytä toista tunnusta")
        return render_template("register.html")

    return render_template("post_register.html", csrf_token=generate_csrf_token())

@app.route("/post_register_redirect", methods=["POST"])
def post_register_redirect():
    next_page = request.form.get("next", "login")
    if next_page not in ("login", "main_layout"):
        next_page = "login"
    return redirect(url_for(next_page))

@app.route("/new_project", methods=["GET", "POST"])
def new_project():

    all_classes = service_functions.get_all_classes()
    existing_classes = {}
    mode = "new"
    
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
    
    return render_template(
        "project_form.html",
        next_id=next_id,
        all_classes=all_classes,
        existing_classes=existing_classes,
        mode=mode, csrf_token=generate_csrf_token()
    )

@app.route("/edit_project/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    all_classes = service_functions.get_all_classes()
    project = service_functions.get_project_by_id(project_id)
    if not project:
        abort(404)

    user_id = session.get("user_id")
    if not user_id:
        abort(403)

    permission = service_functions.get_user_project_permission(project_id, user_id)
    if not permission or not permission["can_modify"]:
        flash("Sinulla ei ole oikeutta muokata tätä projektia.", "error")
        return redirect(url_for("list_projects"))

    definitions_rows = service_functions.get_project_definitions(project_id)
    existing_classes = {d["title"]: d["value"] for d in definitions_rows}
    mode = "edit"

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

        service_functions.update_project(project_id, project_name, classes, user_id)

        return render_template(
            "main_layout.html",
            message=f"Projekti {project_name} päivitetty"
        )

    return render_template(
        "project_form.html",
        next_id=project_id,
        all_classes=all_classes,
        existing_classes=existing_classes,
        mode=mode,
        project=project,
        csrf_token=generate_csrf_token()
    )

@app.route("/list_projects", methods=["GET"])
def list_projects():
    # Get current filter values from query string
    search_name = request.args.get("project_name") or None
    search_type = request.args.get("project_type") or None
    search_method = request.args.get("depreciation_method") or None

    projects = service_functions.get_projects(
        search_name=search_name,
        search_type=search_type,
        search_method=search_method
    )

    all_classes = service_functions.get_all_classes()
    project_types = all_classes.get("Projektityyppi", [])
    depreciation_methods = all_classes.get("Poistomenetelmä", [])

    for i, project_row in enumerate(projects):
        project = dict(project_row)  # convert row to dict
        definitions = service_functions.get_project_definitions(project["project_id"])
        project["definitions"] = {d["title"]: d["value"] for d in definitions}
        projects[i] = project  # replace the original row with enriched dict

    return render_template(
        "list_projects.html",
        projects=projects,
        project_types=project_types,
        depreciation_methods=depreciation_methods,
        request=request
    )

@app.route("/cashflow_project/<int:project_id>")
def cashflow_project(project_id):

    investments = service_functions.get_project_investments(project_id)

    return render_template(
        'cashflow_project.html',
        project_id=project_id,
        investments=investments
    )

@app.route("/delete_project/<int:project_id>")
def delete_project(project_id):
    user_id = session.get("user_id")
    if not user_id:
        abort(403)

    sql = "SELECT inserting_user FROM Inserted WHERE project_id = ?"
    result = service_functions.query(sql, (project_id,))
    if not result:
        flash(f"Tietokantavirhe, projektille {project_id} ei löytynyt luojaa")
        return redirect(url_for("list_projects"))

    inserting_user = result[0]["inserting_user"]

    if user_id != inserting_user:
        flash(f"Et ole projektin {project_id} luoja", "error")
        return redirect(url_for("list_projects"))

    service_functions.delete_project_by_id(project_id)
    flash(f"Projekti {project_id} poistettu")

    return redirect(url_for("list_projects"))

@app.route('/add_new_cashflow/<int:project_id>', methods=['GET', 'POST'])
def add_new_cashflow(project_id):
    if request.method == 'POST':
        investment_year = request.form['investment_year']
        investment_amount = request.form['investment_amount']

        modifying_user = session.get("user_id")

        service_functions.add_cashflow(project_id, investment_year, investment_amount, modifying_user)

        return redirect(url_for('cashflow_project', project_id=project_id))

    return render_template(
        'add_new_cashflow.html',
        project_id=project_id,
        csrf_token=generate_csrf_token()
    )

@app.route("/management_project/<int:project_id>")
def management_project(project_id):

    project = service_functions.get_project_by_id(project_id)
    if not project:
        flash("Projektia ei löytynyt.", "error")
        return redirect(url_for("list_projects"))

    creator = service_functions.get_project_creator(project_id)

    changes = service_functions.get_project_modifications(project_id)

    return render_template(
        "management_project.html",
        project=project,
        creator=creator,
        changes=changes
    )

@app.route("/project/<int:project_id>/rights", methods=["GET", "POST"])
def rights_project(project_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("Et ole kirjautunut sisään.", "error")
        return redirect(url_for("login"))

    project_name = request.args.get("project_name") or ""
    project_type = request.args.get("project_type") or ""
    depreciation_method = request.args.get("depreciation_method") or ""

    creator_id = service_functions.get_project_creator_id(project_id)
    if creator_id is None:
        flash("Projektia ei löytynyt.", "error")
        return redirect(url_for(
            "list_projects",
            project_name=project_name,
            project_type=project_type,
            depreciation_method=depreciation_method
        ))

    if user_id != creator_id:
        flash("Vain projektin luoja voi muuttaa oikeuksia.", "error")

        # Get projects with filters
        projects_rows = service_functions.get_projects(
            search_name=project_name,
            search_type=project_type,
            search_method=depreciation_method
        )

        # Enrich projects
        projects = []
        for row in projects_rows:
            project = dict(row)
            definitions = service_functions.get_project_definitions(project["project_id"])
            project["definitions"] = {d["title"]: d["value"] for d in definitions}
            project["created"] = service_functions.get_project_creator(project["project_id"])
            project["changes"] = []  # or implement modifications later
            projects.append(project)

        # Dropdown options
        all_classes = service_functions.get_all_classes()
        project_types = all_classes.get("Projektityyppi", [])
        depreciation_methods = all_classes.get("Poistomenetelmä", [])

        return render_template(
            "list_projects.html",
            projects=projects,
            project_types=project_types,
            depreciation_methods=depreciation_methods,
            search_name=project_name,
            search_type=project_type,
            search_method=depreciation_method,
            request=request
        )

    if request.method == "POST":
        permissions = {}
        for user in service_functions.get_all_users():
            if user["id"] == creator_id:
                continue
            can_modify = f"can_modify_{user['id']}" in request.form
            permissions[user["id"]] = can_modify

        service_functions.update_project_permissions(project_id, creator_id, permissions)
        flash("Oikeudet päivitetty.", "success")

        return redirect(url_for(
            "rights_project",
            project_id=project_id,
            project_name=project_name,
            project_type=project_type,
            depreciation_method=depreciation_method
        ))

    users = service_functions.get_project_permissions(project_id)

    return render_template(
        "rights_project.html",
        project_id=project_id,
        users=users,
        creator_id=creator_id,
        csrf_token=generate_csrf_token(),
        project_name=project_name,
        project_type=project_type,
        depreciation_method=depreciation_method
    )

@app.route("/user_statistics")
def user_statistics():
    user_id = session.get("user_id")
    if not user_id:
        flash("Kirjaudu sisään nähdäksesi tilastosi.", "error")
        return redirect(url_for("login"))

    projects = service_functions.get_projects_created_by_user(user_id)

    return render_template(
        "user_statistics.html",
        projects=projects
    )

@app.route("/logout")
def logout():
    session.clear()
    return render_template("logout.html")

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True)