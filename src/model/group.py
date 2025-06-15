from database import db
from model.associations import user_group, task_group


class Group(db.Model):
    __tablename__ = "group"
    id = db.Column(db.String, primary_key=True)
    users = db.relationship("User", back_populates="assigned_groups", secondary=user_group)
    tasks = db.relationship("Task", back_populates="groups", secondary=task_group)


def init_default_groups():
    group1 = Group(id="c1")
    group2 = Group(id="c2")
    group3 = Group(id="c3")
    try:
        db.session.add_all([group1, group2, group3])
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()
