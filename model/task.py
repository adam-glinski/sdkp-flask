from database import db


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    # Task manager stuff
    manager_id = db.Column(db.String, db.ForeignKey("user.student_id"), nullable=False)
    manager = db.relationship("User", back_populates="ownedTasks")
    # Solutions
    solutions = db.relationship("Solution", back_populates="task")

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, title={self.title!r}, manager={self.manager!r})"


def init_default_tasks():
    task1 = Task(title="Example task", manager_id="s00002")
    try:
        db.session.add_all([task1])
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
