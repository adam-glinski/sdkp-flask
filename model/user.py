import enum

from flask_login import UserMixin

from database import db


class UserRole(enum.Enum):
    ADMIN = "admin"
    TASK_MANAGER = "task manager"
    USER = "user"


class User(UserMixin, db.Model):
    __tablename__ = "user"
    student_id = db.Column(db.String, primary_key=True, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    surname = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    ownedTasks = db.relationship("Task", back_populates="manager")
    ownedSolutions = db.relationship("Solution", back_populates="owner")

    def get_id(self):
        return self.student_id

    def __repr__(self) -> str:
        return f"User(id={self.student_id!r}, name={self.name!r}, surname={self.surname!r}, password={self.password!r})"


def init_default_users():
    admin = User(student_id="s00001", name="Admin", surname="Admin", password="toor", role=UserRole.ADMIN)
    taskmanager = User(student_id="s00002", name="Task", surname="Manager", password="task", role=UserRole.TASK_MANAGER)
    user = User(student_id="s00003", name="User", surname="User", password="user", role=UserRole.USER)

    adam = User(student_id="s30593", name="Adam", surname="Glinski", password="test", role=UserRole.USER)

    try:
        db.session.add_all([admin, taskmanager, user, adam])
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
