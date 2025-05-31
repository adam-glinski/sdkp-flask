from database import db


class Solution(db.Model):
    __tablename__ = "solution"
    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    # Target task
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), nullable=False)
    task = db.relationship("Task", back_populates="solutions", uselist=False)
    # Owner of the solution
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    owner = db.relationship("User", back_populates="ownedSolutions")
    # Content of the solution
    script = db.Column(db.String, nullable=False, unique=False)

    def __repr__(self) -> str:
        return f"Solution(id={self.id!r}, task={self.task!r}, owner={self.owner!r}, script={self.script!r})"


def init_default_solutions():
    soltion_user = Solution(task_id=1, owner_id=3, script="User's solution to task 1.")
    soltion_adam = Solution(task_id=1, owner_id=4, script="Adam's solution to task 1.")
    try:
        db.session.add_all([soltion_user, soltion_adam])
        db.session.commit()
    except Exception:  # TODO: Check if the same as empty except:
        db.session.rollback()
        raise
    finally:
        db.session.close()
