# Sick & Annual Leave Tracker

A Flask web application for tracking employee sick leave and annual leave. Re-engineered from a tkinter desktop application.

Developed by **SD Solutions**.

## Features

- **Employee Management** - Add, update, and delete employees with automatic leave calculation
- **Annual Leave Tracking** - Record and manage annual leave with start/end dates and comments
- **Sick Leave Tracking** - Track sick leave within 36-month cycles with automatic balance calculation
- **Medical Documents** - Upload, view, and manage medical certificates per employee
- **Excel Export** - Export all leave data to formatted Excel spreadsheets
- **Multi-User Authentication** - Admin and regular user roles with secure password management
- **Employee Backups** - Automatic backup of employee data and documents on deletion
- **CSRF Protection** - All forms protected against cross-site request forgery

## Security

- Complex password policy: minimum 14 characters, must include uppercase, lowercase, number, and special character
- All new users forced to change password on first login
- Session-based authentication with secure cookie handling
- Parameterized SQL queries to prevent injection
- CSRF protection on all forms
- File uploads sanitized with secure filenames

## Installation

### Prerequisites

- Python 3.11+

### Setup

1. Run the install script:

```bash
python install.py
```

The install script will:
- Automatically install all required Python dependencies
- Create the SQLite database (`employeeLeave.db`)
- Set up all required tables
- Generate a random secure admin password
- Display the admin credentials on screen

**Important:** Save the admin password shown during installation. You will need it to log in.

2. Start the application:

```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

4. Log in with the admin credentials from step 1

5. You will be prompted to change the password on first login

## User Management

- **Admin users** can add/delete users and reset passwords via the Users page
- **Regular users** can manage employees, leave records, and documents
- The primary admin account cannot be deleted

## Dependencies

- Flask - Web framework
- Flask-WTF - CSRF protection
- Werkzeug - Password hashing and security utilities
- python-dateutil - Date parsing
- openpyxl - Excel file generation

## Project Structure

```
app.py              - Flask application and route handlers
db.py               - SQLite database operations
install.py          - Installation and setup script
static/
  style.css         - Application styling
  logo.png          - SD Solutions logo
templates/          - Jinja2 HTML templates
uploads/            - Medical document storage (per-employee folders)
backups/            - Employee backup data on deletion
```

## Leave Calculation

- **Annual Leave**: Employees accrue 1.25 days per month of service
- **Sick Leave**: 30 days per 36-month cycle. Employees in their first 6 months accrue 1 day per month

## Original Project

Forked from [Devon-GS/Sick-Annual-Leave-Tracker](https://github.com/Devon-GS/Sick-Annual-Leave-Tracker) and re-engineered as a web application.
