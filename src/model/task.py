from database import db

import tzlocal
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from model.associations import task_group
from model.group import Group


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)  # Stored in UTC zone
    # Task manager stuff
    manager_id = db.Column(db.String, db.ForeignKey("user.student_id"), nullable=False)
    manager = db.relationship("User", back_populates="owned_tasks")
    # Solutions
    solutions = db.relationship("Solution", back_populates="task")
    groups = db.relationship("Group", back_populates="tasks", secondary=task_group)
    stdin = db.Column(db.String, nullable=True)
    stdout = db.Column(db.String, nullable=True)

    @property
    def date_local(self) -> str:
        local_tz = ZoneInfo(tzlocal.get_localzone_name())
        d: datetime = self.deadline
        d.replace(tzinfo=local_tz)
        return f"{d.year}/{d.month}/{d.day} {d.hour}:{d.minute}"

    @property
    def is_active(self) -> bool:  # Compare as UTC
        # print(f"is_active: {self.deadline} < {datetime.utcnow()} = {self.deadline < datetime.utcnow()}")
        return self.deadline > datetime.utcnow()

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r}, manager={self.manager!r})"


def init_default_tasks():
    local_tz = ZoneInfo(tzlocal.get_localzone_name())
    task1_local = datetime(2025, 6, 10, 18, 59, 00, tzinfo=local_tz)
    task1 = Task(name="Example task that is past deadline", manager_id="s00002", content="This is an example task that is past deadline.", deadline=task1_local.replace(tzinfo=timezone.utc))

    task2_local = datetime(2025, 7, 22, 23, 59, 00, tzinfo=local_tz)
    task2 = Task(name="Example task that is active", manager_id="s00002", content="This is an example task that is still active.", deadline=task2_local.replace(tzinfo=timezone.utc))
    group1 = Group.query.get("c1")
    group1.tasks.append(task1)
    group1.tasks.append(task2)

    try:
        db.session.add_all([task1, task2])
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()
