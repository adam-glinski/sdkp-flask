from database import db


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    # Task manager stuff
    manager_id = db.Column(db.String, db.ForeignKey("user.student_id"), nullable=False)
    manager = db.relationship("User", back_populates="ownedTasks")
    # Solutions
    solutions = db.relationship("Solution", back_populates="task")

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r}, manager={self.manager!r})"


def init_default_tasks():
    task1 = Task(name="Example task", manager_id=2)
    try:
        db.session.add_all([task1])
        db.session.commit()
    except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
