# POC
## Project structure
```text
sdkp-flask/
├── app/
│   ├── __init__.py              # Create Flask app and init extensions
│   ├── models/                  # SQLAlchemy models
│   │   ├── user.py              # User model
│   │   ├── task.py              # Task model
│   │   └── solution.py          # Solution model
│   ├── services/                # Business logic layer
│   │   ├── solution_service.py  # Validate, store, log solutions
│   │   ├── task_service.py      # Manage task deadlines, checks
│   │   └── user_service.py      # Register, login, manage users
│   ├── routes/                  # Flask route blueprints
│   │   ├── auth.py              # /login, /register, etc.
│   │   ├── task.py              # /tasks, /submit, etc.
│   │   └── main.py              # /dashboard, /
│   ├── validators/              # Input validation logic
│   │   └── solution_validator.py
│   ├── scheduler/               # Periodic checking logic
│   │   └── task_checker.py      # Run validation jobs
│   ├── static/                  # CSS/JS
│   ├── templates/               # Jinja2 templates
│   └── extensions.py            # db, login_manager, etc.
├── data/                        # Uploaded files, local DB
├── config.py                    # Flask config
├── app.py                       # Entrypoint with `create_app()`
├── requirements.txt
└── README.md
```

## Models
### User
fields:
- `student_id` (*PK*)
- ~~`name`~~
- ~~`surname`~~
- `password` - preferably hashed
- `role` - Either Student (User) or Teacher(Task manager)
- `groups` - **TODO** groups the user is in
- `assigned tasks` - accessible thru groups hes in
information from users level:
- [ ] group's he's assigned to 
    - [ ] tasks he's assigned to
- [ ] owned tasks
#### Task manager
information displayed:
- his tasks
    - with an option to edit current task (stdin stdout)
- uploaded solutions
#### Admin
- existing groups
    - allow him to create new groups
- existing users
    - let him assign users to new groups
### Task
fields:
- `id` (*PK*)
- `title`
- `content` (body of the task - in markdown)
- `owner`
- `groups` that this task is assigned to
- `solutions` sent by users from the groups that the task got assigned to
- `deadlines` - list of DateTime (number of elements = number of deadlines, last element = last deadline)
- `state` of the task (unpublished, open, closed)
    - unpublished - task hasn't been published to the groups yet
    - open - assigned users can upload their solutions
    - closed - assigned users can't upload their solutions anymore, but can view their results from each deadline
additional notes:
- one user may send multiple solutions to one task
- *tasks have defined deadlines (once the deadline is due, the tasks are checking all of the recived solutions)*
- *task has to have definded tests and score for the test -> (list of strings as code or smting)*
- convert `state` into association table (`TaskDeadline`, or Milestone, name is wip) cuz:
    - each group might have diffrent deadlines
    - for each group we'd like to track the current state of that task 
    (to know wheter to even display that tasks for the users in group)
    - only the latest uploaded solution should be kept on the server, and the latest
### Solution
fields:
- `id` (PK)
- `task` target task for which this solution is for
- `owner` of the solution
- `script` solution code
- `date` when the solution got uploaded

