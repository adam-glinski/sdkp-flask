import os
from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from database import db

from model.user import init_default_users, User, UserRole
from model.task import init_default_tasks
from model.solution import init_default_solutions

basedir = os.path.abspath(os.path.dirname(__file__))


def populate_default_db():
    init_default_users()
    init_default_tasks()
    init_default_solutions()


login_manager = LoginManager()


def create_app(isDebug: bool):
    app = Flask(__name__)

    db_path = os.path.join(basedir, "data", "sdkp.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SECRET_KEY"] = "PPY_32"
    db.init_app(app)

    with app.app_context():
        db.create_all()

        if isDebug:
            populate_default_db()

    login_manager.init_app(app)
    login_manager.login_view = "login"

    return app


app = create_app(True)


@login_manager.user_loader
def load_user(student_id):
    return User.query.get(int(student_id))


# ROUTING
@app.route('/')
@login_required
def index():
    return redirect(url_for("dashboard"))


# Register route
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        name = request.form.get("name")
        surname = request.form.get("surname")
        role = request.form.get("role")
        password = request.form.get("password")  # Should store only hashed passwords but its poc

        if User.query.filter_by(student_id=student_id).first():
            return render_template("sign_up.html", error="Account with that student id already exists")

        if not student_id or not name or not surname or not password or not role:
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

        new_user = User(student_id=student_id, name=name, surname=surname, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("sign_up.html")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
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
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


if __name__ == '__main__':
    app.run(debug=True)
