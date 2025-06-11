import enum

from flask_login import UserMixin

from database import db
from model.associations import user_group
from model.group import Group


class UserRole(enum.Enum):
    ADMIN = "admin"
    TASK_MANAGER = "task manager"
    USER = "user"


class User(UserMixin, db.Model):
    __tablename__ = "user"
    student_id = db.Column(db.String, primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    owned_tasks = db.relationship("Task", back_populates="manager")
    owned_solutions = db.relationship("Solution", back_populates="owner")
    assigned_groups = db.relationship("Group", back_populates="users", secondary=user_group)

    @property
    def assigned_tasks(self):
        return {task for group in self.assigned_groups for task in group.tasks}

    def get_id(self):
        return self.student_id

    def __repr__(self) -> str:
        return f"User(id={self.student_id!r},  password={self.password!r}, role={self.role!r}, owned_tasks={self.owned_tasks!r}, owned_solutions={self.owned_solutions!r})"


def init_default_users():
    admin = User(student_id="s00001", password="toor", role=UserRole.ADMIN)
    taskmanager = User(student_id="s00002", password="task", role=UserRole.TASK_MANAGER)
    user = User(student_id="s00003", password="user", role=UserRole.USER)

    adam = User(student_id="s30593", password="test", role=UserRole.USER)
    group1 = Group.query.get("c32")
    adam.assigned_groups.append(group1)

    try:
        db.session.add_all([admin, taskmanager, user, adam])
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()
