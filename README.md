# Office Task Management App

This is a task management backend I built as part of the Cybexel Technologies technical assignment.

The idea is simple: a manager can create tasks and assign them to employees. Employees can see and update only the tasks assigned to them.

## What I used

* Python + Django 6.0.1
* Django REST Framework for the API layer
* JWT for authentication
* SQLite for the database
* django-filter for filtering and search
* python-decouple for keeping the secret key outside the code

## What I worked on

I mainly worked on the Django backend and REST APIs.

I created the database models for users, profiles, tasks and comments, then connected them with Django REST Framework serializers and views.

I also implemented JWT authentication, role-based access, task management, comments, dashboard statistics, search, filtering and pagination.

One of the main requirements was security: an employee should not be able to access another employee's task just by changing the task ID. I handled this at the backend level and tested it using Postman.

## How the application works

The basic flow is:

```text
User Login
    ↓
JWT Authentication
    ↓
Role-based Access
    ↓
Dashboard
    ↓
Admin creates and assigns tasks
    ↓
Employee views assigned tasks
    ↓
Employee updates task status
    ↓
Employee adds comments
    ↓
Dashboard shows task statistics
```

## How roles work

There are two roles in the application:

### Admin / Manager

The admin can:

* Create tasks
* Assign tasks to employees
* View tasks
* Update tasks
* Delete tasks
* View dashboard statistics
* View comments

### Employee

Employees can:

* View their assigned tasks
* Update their assigned tasks
* Add comments to their tasks
* View their own task statistics

Employees cannot access another employee's tasks, assign tasks, or delete tasks.

The role is stored in a separate `Profile` model connected to Django's built-in `User` model.

## Authentication

I used JWT authentication with Django REST Framework Simple JWT.

After login, the API returns a JWT access token. The token is then used to access protected APIs.

```text
POST /api/login/
POST /api/login/refresh/
```

## Task Management

The `Task` model contains:

* Title
* Description
* Assigned employee
* Priority
* Status
* Due date
* Created date
* Updated date

The task supports different priorities:

```text
Low
Medium
High
```

And different statuses:

```text
Pending
In Progress
Completed
Cancelled
```

## Task Comments

I created a separate `TaskComment` model for comments.

Each comment is connected to a task and the user who created it.

The comment author is taken from the authenticated user on the backend instead of trusting an author ID from the request.

## Dashboard

The dashboard API provides:

* Total tasks
* Pending tasks
* In Progress tasks
* Completed tasks
* Overdue tasks

Admins see statistics for all tasks, while employees see statistics only for their assigned tasks.

```text
GET /api/tasks/dashboard/
```

## Search and Filtering

The task API supports filtering by:

```text
status
priority
assigned_to
```

It also supports searching by task title.

Examples:

```text
/api/tasks/?status=Pending
/api/tasks/?priority=High
/api/tasks/?search=report
```

## API Endpoints

### Authentication

```text
POST /api/login/
POST /api/login/refresh/
```

### Tasks

```text
GET    /api/tasks/
POST   /api/tasks/
GET    /api/tasks/{id}/
PUT    /api/tasks/{id}/
PATCH  /api/tasks/{id}/
DELETE /api/tasks/{id}/
GET    /api/tasks/dashboard/
```

### Comments

```text
GET  /api/comments/
POST /api/comments/
```

## Security

This was one of the main parts of the assignment.

I did not depend only on frontend restrictions. The employee's task access is controlled at the backend level.

For employees, the task queryset is filtered using the logged-in user:

```python
Task.objects.filter(assigned_to=user)
```

Because of this, if an employee tries to access another employee's task by manually changing the task ID, that task is not returned.

I tested this using Postman by logging in as different employees and trying to access each other's tasks.

## Database Structure

The main models are:

```text
User
 └── Profile
      └── role

User
 └── Task
      └── TaskComment
```

A user can have multiple assigned tasks, and a task can have multiple comments.

## Testing

I tested the APIs using Postman.

Some of the scenarios I tested:

* Admin login
* Employee login
* Creating tasks
* Assigning tasks
* Viewing tasks
* Updating task status
* Adding comments
* Searching tasks
* Filtering tasks
* Dashboard statistics
* Trying to access another employee's task
* Checking authenticated API access

## Project Structure

```text
office-task-manager/
│
├── manage.py
├── requirements.txt
├── .gitignore
│
├── taskmanager/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── tasks/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    ├── tests.py
    └── migrations/
```

## Getting it running

Clone the repository:

```bash
git clone https://github.com/jayakanth2727/office-task-manager-.git
cd office-task-manager-
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
SECRET_KEY=your-secret-key-here
```

Run migrations:

```bash
python manage.py migrate
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Start the server:

```bash
python manage.py runserver
```

Admin panel:

```text
http://127.0.0.1:8000/admin/
```

API:

```text
http://127.0.0.1:8000/api/
```

## Notes

React was optional in the assignment, so I focused mainly on completing the Django backend, REST APIs, authentication, task management and permission/security requirements.

SQLite was used for local development and testing. The database can be changed to PostgreSQL or MySQL later through the Django database configuration.

The `.env` file is not included in the repository because it contains configuration values that should not be committed to GitHub.
