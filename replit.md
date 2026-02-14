# Sick & Annual Leave Tracker

## Overview
A Python desktop (tkinter) application for tracking employee sick leave and annual leave. Forked from [steve191/Sick-Annual-Leave-Tracker](https://github.com/steve191/Sick-Annual-Leave-Tracker).

## Current State
- Application imported and running via VNC output
- Uses SQLite database (created automatically by database.py)

## Project Architecture
- **main.py** - Entry point, main GUI window with employee table and action buttons
- **database.py** - SQLite database operations (CRUD for employees, leave records)
- **annual_leave.py** - Annual leave management UI
- **sick_leave.py** - Sick leave management UI
- **view_leave.py** - View all leave records, export to Excel
- **med_docs.py** - Medical document folder management
- **backup.py** - Employee data backup on deletion

## Dependencies
- Python 3.11 (Full, with tkinter)
- tkcalendar - Calendar widget for date selection
- python-dateutil - Date utilities
- openpyxl - Excel file read/write

## How to Run
The app runs as a desktop GUI via VNC workflow: `python main.py`
