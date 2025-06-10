from database import db

user_group = db.Table('UserGroup',
                      db.Column('student_id', db.Integer, db.ForeignKey('user.student_id'), primary_key=True),
                      db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
                      )


task_group = db.Table('TaskGroup',
                      db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
                      db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
                      )
