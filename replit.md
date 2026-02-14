# Sick & Annual Leave Tracker

## Overview
A Flask web application for tracking employee sick leave and annual leave, developed by SD Solutions. Re-engineered from a tkinter desktop app, originally forked from [Devon-GS/Sick-Annual-Leave-Tracker](https://github.com/Devon-GS/Sick-Annual-Leave-Tracker).

## Current State
- Web application running on Flask (port 5000)
- Uses SQLite database (employeeLeave.db)
- Multi-user authentication with admin and regular user roles
- Admin can add/delete users and reset passwords
- All users forced to change password on first login
- Complex password policy: min 14 chars, uppercase, lowercase, number, special character
- Install script generates random admin credentials
- CSRF protection on all forms
- SD Solutions branded logo on login page and navigation bar
- Excel export for all leave data
- Medical document upload and management per employee
- Employee backup on deletion (data + documents)

## Project Architecture
- **app.py** - Flask web application, routes, and request handlers
- **db.py** - SQLite database operations (CRUD for employees, leave records, auth, user management)
- **install.py** - Installation script that sets up DB and creates admin user with random password
- **templates/** - Jinja2 HTML templates (base, login, employees, leave, documents, users, change_password, add_leave, folder)
- **static/style.css** - Application styling
- **static/logo.png** - SD Solutions logo
- **uploads/** - Medical document storage (per-employee folders)
- **backups/** - Employee backup data on deletion

### Legacy Files (original tkinter app, kept for reference)
- main.py, database.py, annual_leave.py, sick_leave.py, view_leave.py, med_docs.py, backup.py

## Dependencies
- Python 3.11
- Flask - Web framework
- Flask-WTF - CSRF protection
- Werkzeug - Password hashing and utilities
- python-dateutil - Date parsing
- openpyxl - Excel file generation

## How to Run
1. Run `python install.py` to initialize the database and create admin credentials
2. Run `python app.py` to start the web server on port 5000
3. Login with the credentials shown during install
4. Change password on first login (required)

## User Preferences
- Local SQLite database (no external DB services)
- Admin authentication required
- Web-based UI for local hosting
- SD Solutions branding
