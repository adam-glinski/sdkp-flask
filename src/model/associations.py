from database import db

user_group = db.Table('user_group',
                      db.Column('student_id', db.String, db.ForeignKey('user.student_id'), primary_key=True),
                      db.Column('group_id', db.String, db.ForeignKey('group.id'), primary_key=True)
                      )


task_group = db.Table('task_group',
                      db.Column('task_id', db.Integer, db.ForeignKey('task.id'), primary_key=True),
                      db.Column('group_id', db.String, db.ForeignKey('group.id'), primary_key=True)
                      )
