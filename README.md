# Smart Study Manager

Smart Study Manager is a full-stack Django web application designed to help students organize their study tasks and track productivity efficiently.

The application allows users to create, manage, and monitor study tasks with authentication, progress tracking, and a clean dashboard interface.

Live Demo: https://your-render-url.onrender.com

---

# Features

## Authentication System
- User registration
- Secure login and logout
- Password hashing using Django authentication system
- Session management

## Task Management
- Create study tasks
- Edit existing tasks
- Mark tasks as completed
- Delete tasks
- Deadline tracking

## Productivity Tracking
- Dashboard with task statistics
- Completion progress percentage
- Visual progress bar

## Search & Filtering
- Search tasks by title or description
- Filter tasks by status (completed / pending)

## User Experience
- Landing page
- Personal dashboard
- Profile page with user statistics
- Clean responsive UI using Bootstrap

## Security
- CSRF protection
- Login required for task access
- User-specific data isolation
- Secure password storage

## Deployment
- Deployed on Render
- Production setup using Gunicorn
- Static files served with WhiteNoise

---

# Tech Stack

## Backend
- Django
- Django Authentication System
- SQLite Database

## Frontend
- HTML
- CSS
- Bootstrap

## Deployment & Tools
- Gunicorn
- WhiteNoise
- Render (cloud hosting)

## Development Tools
- Git
- GitHub
- VS Code

---

# Project Structure

```
SmartStudyManager
│
├── config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   └── urls.py
│
├── templates
│   ├── base.html
│   ├── landing.html
│   ├── dashboard.html
│   ├── profile.html
│   └── registration
│       └── login.html
│
├── static
│
├── manage.py
└── requirements.txt
```

---

# Installation (Run Locally)

Clone the repository

```bash
git clone https://github.com/yourusername/smart-study-manager.git
cd smart-study-manager
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows
```bash
venv\Scripts\activate
```

Mac / Linux
```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Create admin user

```bash
python manage.py createsuperuser
```

Run development server

```bash
python manage.py runserver
```

Open in browser

```
http://127.0.0.1:8000
```

---

# Usage

1. Register a new user account
2. Login using your credentials
3. Create study tasks
4. Track progress from dashboard
5. Edit or complete tasks
6. Monitor statistics in your profile

---

# Deployment

This project is deployed using **Render**.

Production setup includes:
- Gunicorn as the WSGI server
- WhiteNoise for static file handling
- Production configuration with `DEBUG=False`

---

# Future Improvements

- REST API using Django REST Framework
- PostgreSQL database integration
- Task sharing system
- Advanced analytics charts
- Selenium automated testing
- Dark mode UI
- Email notification system

---

# Author

Bhargav

GitHub: https://github.com/bhargav20-ui

---

# License

This project is open-source and available under the MIT License.