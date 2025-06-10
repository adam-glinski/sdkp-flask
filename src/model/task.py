from database import db

from model.associations import task_group
from model.group import Group


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    # Task manager stuff
    manager_id = db.Column(db.String, db.ForeignKey("user.student_id"), nullable=False)
    manager = db.relationship("User", back_populates="owned_tasks")
    # Solutions
    solutions = db.relationship("Solution", back_populates="task")
    groups = db.relationship("Group", back_populates="tasks", secondary=task_group)

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r}, manager={self.manager!r})"


def init_default_tasks():
    task1 = Task(name="Example task", manager_id="s00002", content="This is an example task.", deadline=db.Date())
    group1 = Group.query.get("c32")
    group1.tasks.append(task1)

    try:
        db.session.add_all([task1])
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
