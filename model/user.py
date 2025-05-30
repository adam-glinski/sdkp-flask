import enum
from enum import unique

from flask_login import UserMixin

from database import db


class UserRole(enum.Enum):
    ADMIN = "admin"
    TASK_MANAGER = "task manager"
    USER = "user"


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    student_id = db.Column(db.String, unique=True, nullable=True) # Change to false
    name = db.Column(db.String, unique=False, nullable=False)
    surname = db.Column(db.String, unique=False, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    ownedTasks = db.relationship("Task", back_populates="manager")
    ownedSolutions = db.relationship("Solution", back_populates="owner")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, surname={self.surname!r}, password={self.password!r})"


def init_default_users():
    admin = User(name="Admin", surname="Admin", password="toor", role=UserRole.ADMIN)
    taskmanager = User(name="Task", surname="Manager", password="task", role=UserRole.TASK_MANAGER)
    user = User(name="User", surname="User", password="user", role=UserRole.USER)

    adam = User(name="Adam", surname="Glinski", password="test", role=UserRole.USER)

    try:
        db.session.add_all([admin, taskmanager, user, adam])
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
