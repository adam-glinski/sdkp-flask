import os
import tzlocal

from datetime import datetime
from zoneinfo import ZoneInfo

from flask import Flask, request, render_template, redirect, url_for, Response, flash, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from database import db

from model.user import init_default_users, User, UserRole
from model.group import init_default_groups, Group
from model.task import init_default_tasks, Task
from model.solution import init_default_solutions, Solution

from backend.tester import test_code
from backend.pdf_generation import gen_pdf

basedir = os.path.abspath(os.path.dirname(__file__))


def populate_default_db() -> None:
    """
    Populates example users, tasks and solutions.
    This function calls :func:`~model.user.init_default_users`, :func:`~model.task.init_default_tasks`, :func:`~model.solution.init_default_solutions` in that order.
    Warning:
        This function is only meant for testing during development, and shouldn't be used in production.
    """
    init_default_groups()
    init_default_users()
    init_default_tasks()
    init_default_solutions()


def create_app(is_debug: bool) -> tuple[Flask, LoginManager]:
    """
    Function initalizes Flask application and LoginManager.

    Args:
        is_debug (bool): if True, :func:`populate_default_db` will run.

    Returns:
        tuple[Flask, LoginManager]: initalized Flask and LoginManager classes.
    """
    app = Flask(__name__)
    login_manager = LoginManager()

    db_path = os.path.join(basedir, "..", "data", "sdkp.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SECRET_KEY"] = "PPY_32"
    db.init_app(app)

    with app.app_context():
        db.create_all()
        if is_debug:
            print("[DEBUG] Populating default db entries")
            populate_default_db()

    login_manager.init_app(app)
    login_manager.login_view = "login"
    return app, login_manager


app, login_manager = create_app(False)
# app, login_manager = create_app(True)


@login_manager.user_loader
def load_user(student_id: str) -> (User | None):
    """
    Function is a user loader function for the flask_login module.

    Args:
        student_id (str):  id of the student

    Returns:
        (User | None) - User if user with that `student_id` got found, None if not.
    """
    return User.query.get(student_id)


@app.route('/')
@login_required
def index() -> Response:
    """
    Function exposes the '/' route, which redirects to `/dashboard` view.
    Requires the user to be logged in, if not, redirects to '/login'.
    """
    return redirect(url_for("dashboard"))


# Register route
@app.route('/register', methods=["GET", "POST"])
def register() -> Response:
    """
    Function exposes the '/register' route, which lets the user register an account.
    It also checks upon registration whether an account with given `student_id` already exists.
    """
    if request.method == "POST":
        student_id = request.form.get("student_id")
        role = request.form.get("role")
        password = request.form.get("password")  # Should store only hashed passwords but its poc

        if User.query.filter_by(student_id=student_id).first():
            return render_template("sign_up.html", error="Account with that student id already exists")

        if not student_id or not password or not role:
            return render_template("sign_up.html", error="Please fill all fields")

        # if role not in ["admin", "task manager", "user"]:
        #     return render_template("sign_up.html", error="Invalid role")
        match role.lower():
            case "student":
                role = UserRole.USER
            case "teacher":
                role = UserRole.TASK_MANAGER
            case _:
                return render_template("sign_up.html", error="Invalid role")

        # hashed_password = generate_password_hash(password, method="pbkdf2:sha256") # DELETEME

        new_user = User(student_id=student_id, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("sign_up.html")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Function exposes the '/login' route, which lets the user login.
    If the login was successful, redirects to '/dashboard'
    """
    if request.method == "POST":
        student_id = request.form.get("student_id")
        password = request.form.get("password")

        user = User.query.filter_by(student_id=student_id).first()

        if user and user.password == password:
            login_user(user, force=True)
            return redirect(url_for("dashboard"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


# Logout route
@app.route("/logout")
@login_required
def logout() -> Response:
    """
    Function exposes the '/logout' route, which lets the user to logout.
    Requires the user to be logged in, if not, redirects to '/'.
    """
    logout_user()
    return redirect(url_for("index"))


@app.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    """
    Function exposes the '/dashboard' route, which displays the dashboard for each user role.
    Requires the user to be logged in, if not, redirects to '/login'.
    """
    match current_user.role:
        case UserRole.USER:
            return render_template("dashboard_user.html", user=current_user)
        case UserRole.TASK_MANAGER:
            return render_template("dashboard_task_manager.html", user=current_user)
        case UserRole.ADMIN:
            if request.method == "POST":
                new_group_id: str = request.form.get("new_group_id")
                action = request.form.get("action")
                if action == "Create new group":
                    if Group.query.get(new_group_id) is None:
                        new_group = Group(id=new_group_id)
                        db.session.add(new_group)
                        db.session.commit()
                elif action == "Add selected users to selected groups":
                    selected_users: list[User] = request.form.getlist("users")
                    selected_groups: list[Group] = request.form.getlist("groups")
                    for group_id in selected_groups:
                        for user_id in selected_users:
                            user = User.query.get(user_id)
                            # if not any(g == group_id for g in user.assigned_groups):  # If user not already assigned
                            if user.assigned_groups.count(group_id) == 0:
                                group = Group.query.get(group_id)
                                group.users.append(user)
                    db.session.commit()
                return redirect("/dashboard")
            return render_template("dashboard_admin.html", user=current_user, all_groups=Group.query.all(), all_users=User.query.filter_by(role=UserRole.USER))
        case _:
            return render_template("dashboard.html", user=current_user)


@app.route("/task/<int:id>", methods=["GET", "POST"])
@login_required
def task(id: int):  # TODO: Add validation whether the user actually has this task assigned if not do not let him view it
    """
    Function exposes the '/task/<int>' route, which displays the current task for GET request
    and saves user solution for POST request

    Args:
        id (int): Id of the task
    """
    if request.method == "POST":
        student_id = current_user.student_id
        code = request.form.get("solution")
        print(f"Recived solution from {student_id} {code=}")

        new_solution = Solution(task_id=id, owner_id=student_id, script=code, date=datetime.now(ZoneInfo("UTC")))

        db.session.add(new_solution)
        db.session.commit()
        flash("Successfully uploaded solution.", 'success')
        return redirect(url_for("task", id=id))

    task = Task.query.get(id)
    if not task.is_active and task.manager_id != current_user.student_id:
        return redirect("/dashboard")
    return render_template("task.html", task=task)


@app.route("/task/new", methods=["GET", "POST"])
@login_required
def task_new():
    """
    Function exposes the '/task/new' route, which displays form to create new task for GET request
    and saves thew newly created task for POST request
    """
    if current_user.role != UserRole.TASK_MANAGER:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        name = request.form.get("name")
        content = request.form.get("content")
        stdin = request.form.get("stdin")
        stdout = request.form.get("stdout")
        groups = request.form.getlist("assigned_groups")
        deadline = request.form.get("deadline")

        local_aware = datetime.strptime(deadline, "%Y-%m-%d %H:%M").replace(
                tzinfo=ZoneInfo(tzlocal.get_localzone_name()))

        new_task = Task(manager_id=current_user.student_id, name=name, content=content,
                        stdin=stdin, stdout=stdout, deadline=local_aware.astimezone(ZoneInfo("UTC")))
        # Assign new task to selected groups
        # NOTE: Ideally we should keep a state of these tasks (eg unpublished, published, overdue etc)
        for group_name in groups:
            group = Group.query.get(group_name)
            group.tasks.append(new_task)
        db.session.add(new_task)
        db.session.commit()
        print(f"Added {new_task=}")

    all_groups = Group.query.all()
    return render_template("task_new.html", user=current_user, all_groups=all_groups)


@app.route("/task/<int:id>/solutions", methods=["POST"])
@login_required
def task_solutions(id: int):
    """
    Function exposes the '/task/<int>/solutions' route, which displays the tested solutions in a form of pdf for POST request

    Args:
        id (int): Id of the task
    """
    task = Task.query.get(id)
    if current_user.role != UserRole.TASK_MANAGER or task.manager_id != current_user.student_id:
        return redirect(url_for("dashboard"))

    student_passed = {}

    uploaded_solutions: list[Solution] = task.solutions
    if request.method == "POST":
        uploaded_solutions.sort(key=lambda s: s.date)
        for solution in uploaded_solutions:
            student_passed[solution.owner_id] = None
            if student_passed[solution.owner_id] is not None:
                continue
            student_passed[solution.owner_id] = test_code(solution.script, task.stdin, task.stdout)

    pdf = gen_pdf(f"Results for \"{task.name}\"", student_passed)
    pdf.seek(0)  # reset cursor
    response = make_response(pdf.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={task.name}_results.pdf'
    return response


if __name__ == '__main__':
    app.run()
