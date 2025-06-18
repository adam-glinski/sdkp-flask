from datetime import datetime, timezone

from database import db

from backend.tester import test_code


class Solution(db.Model):
    __tablename__ = "solution"
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    date = db.Column(db.DateTime, nullable=False)
    # Target task
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    task = db.relationship("Task", back_populates="solutions", uselist=False)
    # Owner of the solution
    owner_id = db.Column(db.String, db.ForeignKey("user.student_id"), nullable=False)
    owner = db.relationship("User", back_populates="owned_solutions")
    # Content of the solution
    script = db.Column(db.String, nullable=False, unique=False)

    def __repr__(self) -> str:
        return f"Solution(id={self.id!r}, task={self.task!r}, owner={self.owner!r}, script={self.script!r})"

    def did_pass(self) -> bool:
        return test_code(self.script, self.task.stdin, self.task.stdout)


def init_default_solutions():
    soltion_user = Solution(task_id=2, owner_id="s00003", script="print(\"Hello, World!\")", date=datetime.now(tz=timezone.utc))
    soltion_adam = Solution(task_id=2, owner_id="s00004", script="print(\"Should fail\")", date=datetime.now(tz=timezone.utc))
    try:
        db.session.add_all([soltion_user, soltion_adam])
        db.session.commit()
    except Exception:  # TODO: Check if the same as empty except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
