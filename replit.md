# Sick & Annual Leave Tracker

## Overview
A Flask web application for tracking employee sick leave and annual leave. Re-engineered from a tkinter desktop app, originally forked from [steve191/Sick-Annual-Leave-Tracker](https://github.com/steve191/Sick-Annual-Leave-Tracker).

## Current State
- Web application running on Flask (port 5000)
- Uses SQLite database (employeeLeave.db)
- Admin authentication with forced password change on first login
- Install script generates random admin credentials

## Project Architecture
- **app.py** - Flask web application, routes, and request handlers
- **db.py** - SQLite database operations (CRUD for employees, leave records, auth)
- **install.py** - Installation script that sets up DB and creates admin user
- **templates/** - Jinja2 HTML templates (base, login, employees, leave, documents)
- **static/style.css** - Application styling
- **uploads/** - Medical document storage (per-employee folders)
- **backups/** - Employee backup data on deletion

### Legacy Files (original tkinter app, kept for reference)
- main.py, database.py, annual_leave.py, sick_leave.py, view_leave.py, med_docs.py, backup.py

## Dependencies
- Python 3.11
- Flask - Web framework
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
