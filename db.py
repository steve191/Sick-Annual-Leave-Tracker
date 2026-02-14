import sqlite3
import os
from datetime import datetime, date
from dateutil import parser, relativedelta
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'employeeLeave.db')

def parse_date(date_str):
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt)
        except (ValueError, TypeError):
            continue
    return parser.parse(date_str, dayfirst=True)

def get_connection():
    con = sqlite3.connect(DATABASE_PATH)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA foreign_keys = ON')
    return con

def init_db():
    con = get_connection()
    c = con.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS employees (
        ID TEXT NOT NULL PRIMARY KEY,
        firstName TEXT,
        lastName TEXT,
        startDate TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS annualLeave (
        ID TEXT,
        firstName TEXT,
        leaveTaken INTEGER,
        leaveStart TEXT,
        leaveEnd TEXT,
        comment TEXT,
        FOREIGN KEY (ID) REFERENCES employees (ID) ON DELETE CASCADE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS sickLeave (
        ID TEXT,
        firstName TEXT,
        leaveTaken INTEGER,
        leaveStart TEXT,
        leaveEnd TEXT,
        comment TEXT,
        FOREIGN KEY (ID) REFERENCES employees (ID) ON DELETE CASCADE
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        force_password_change INTEGER DEFAULT 1,
        is_admin INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')

    try:
        c.execute("ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0")
        con.commit()
        c.execute("UPDATE users SET is_admin = 1 WHERE username = 'admin'")
    except sqlite3.OperationalError:
        pass

    con.commit()
    con.close()

def create_admin_user(password):
    con = get_connection()
    c = con.cursor()
    pw_hash = generate_password_hash(password)
    try:
        c.execute("INSERT INTO users (username, password_hash, force_password_change, is_admin) VALUES (?, ?, 1, 1)",
                  ('admin', pw_hash))
        con.commit()
    except sqlite3.IntegrityError:
        pass
    finally:
        con.close()

def create_user(username, password, is_admin=0):
    con = get_connection()
    c = con.cursor()
    pw_hash = generate_password_hash(password)
    try:
        c.execute("INSERT INTO users (username, password_hash, force_password_change, is_admin) VALUES (?, ?, 1, ?)",
                  (username.strip().lower(), pw_hash, is_admin))
        con.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        con.close()

def get_all_users():
    con = get_connection()
    c = con.cursor()
    c.execute("SELECT id, username, is_admin, force_password_change, created_at FROM users ORDER BY username")
    rows = c.fetchall()
    con.close()
    return [dict(r) for r in rows]

def delete_user(user_id):
    con = get_connection()
    c = con.cursor()
    c.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    if user and user['username'] == 'admin':
        con.close()
        raise ValueError("Cannot delete the primary admin account.")
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    con.commit()
    con.close()

def reset_user_password(user_id, new_password):
    con = get_connection()
    c = con.cursor()
    pw_hash = generate_password_hash(new_password)
    c.execute("UPDATE users SET password_hash = ?, force_password_change = 1 WHERE id = ?",
              (pw_hash, user_id))
    con.commit()
    con.close()

def is_admin(username):
    con = get_connection()
    c = con.cursor()
    c.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    con.close()
    return user and user['is_admin'] == 1

def get_user(username):
    con = get_connection()
    c = con.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    con.close()
    return user

def verify_password(username, password):
    user = get_user(username)
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None

def update_password(username, new_password):
    con = get_connection()
    c = con.cursor()
    pw_hash = generate_password_hash(new_password)
    c.execute("UPDATE users SET password_hash = ?, force_password_change = 0 WHERE username = ?",
              (pw_hash, username))
    con.commit()
    con.close()

def get_employees():
    con = get_connection()
    c = con.cursor()
    c.execute("SELECT * FROM employees")
    rows = c.fetchall()
    con.close()
    return [dict(r) for r in rows]

def get_employee(emp_id):
    con = get_connection()
    c = con.cursor()
    c.execute("SELECT * FROM employees WHERE ID = ?", (emp_id,))
    row = c.fetchone()
    con.close()
    return dict(row) if row else None

def add_employee(emp_id, fname, sname, start):
    if not emp_id or not fname or not sname or not start:
        raise ValueError("All fields must be filled out.")
    start_date = parser.parse(start, dayfirst=True).strftime('%d/%m/%Y')
    con = get_connection()
    c = con.cursor()
    c.execute("INSERT INTO employees VALUES (?, ?, ?, ?)",
              (emp_id.upper(), fname.capitalize(), sname.capitalize(), start_date))
    con.commit()
    con.close()

def update_employee(emp_id, fname, sname, start_date):
    con = get_connection()
    c = con.cursor()
    c.execute("UPDATE employees SET firstName = ?, lastName = ?, startDate = ? WHERE ID = ?",
              (fname.capitalize(), sname.capitalize(), start_date, emp_id))
    con.commit()
    con.close()

def delete_employee(emp_id):
    con = get_connection()
    c = con.cursor()
    c.execute("DELETE FROM employees WHERE ID = ?", (emp_id,))
    con.commit()
    con.close()

def get_employee_summary():
    con = get_connection()
    c = con.cursor()

    c.execute("SELECT * FROM employees")
    emp_rec = c.fetchall()

    c.execute("SELECT * FROM annualLeave")
    leave_taken = c.fetchall()

    c.execute("SELECT * FROM sickLeave")
    sick_taken = c.fetchall()

    con.close()

    now = datetime.now()
    date_now = now.strftime("%d/%m/%Y")

    employee_info = []

    for x in emp_rec:
        rec = [x['ID'], x['firstName'], x['lastName'], x['startDate']]

        start_date = parse_date(rec[3])
        end_date = datetime.strptime(date_now, "%d/%m/%Y")

        delta = relativedelta.relativedelta(end_date, start_date)
        months = delta.months + (delta.years * 12)
        leave_days = months * 1.25

        for leave in leave_taken:
            if rec[0] == leave['ID']:
                leave_days -= leave['leaveTaken']

        allotted_leave = 30
        today_date = date.today()
        emp_start_date = start_date.date()

        delta = relativedelta.relativedelta(today_date, emp_start_date)
        total_months = delta.years * 12 + delta.months

        current_cycle = int(total_months / 36) if total_months > 0 else 0
        start_cycle_date = emp_start_date + relativedelta.relativedelta(months=(current_cycle * 36))
        end_cycle_date = emp_start_date + relativedelta.relativedelta(months=((current_cycle + 1) * 36))

        if total_months <= 6:
            allotted_leave = total_months * 1

        sick_leave_taken = 0
        for leave in sick_taken:
            if rec[0] == leave['ID']:
                try:
                    format_date = parse_date(leave['leaveStart']).date()
                    if start_cycle_date <= format_date <= end_cycle_date:
                        sick_leave_taken += leave['leaveTaken']
                except (ValueError, TypeError):
                    pass

        emp_info = {
            'ID': rec[0],
            'firstName': rec[1],
            'lastName': rec[2],
            'startDate': rec[3],
            'leaveAvailable': round(leave_days, 2),
            'sickLeaveAvailable': allotted_leave - sick_leave_taken
        }
        employee_info.append(emp_info)

    return employee_info

def add_annual_leave(emp_id, fname, days, start, end, comment):
    start_leave = parser.parse(start, dayfirst=True).strftime('%d/%m/%Y')
    end_leave = parser.parse(end, dayfirst=True).strftime('%d/%m/%Y')
    con = get_connection()
    c = con.cursor()
    c.execute("INSERT INTO annualLeave VALUES (?, ?, ?, ?, ?, ?)",
              (emp_id, fname, int(days), start_leave, end_leave, comment))
    con.commit()
    con.close()

def get_annual_leave():
    con = get_connection()
    c = con.cursor()
    c.execute("SELECT rowid, * FROM annualLeave ORDER BY ID ASC")
    rows = c.fetchall()
    con.close()
    return [dict(r) for r in rows]

def update_annual_leave(rowid, days, start, end, comment):
    start_date = parser.parse(start, dayfirst=True).strftime('%d/%m/%Y')
    end_date = parser.parse(end, dayfirst=True).strftime('%d/%m/%Y')
    con = get_connection()
    c = con.cursor()
    c.execute("UPDATE annualLeave SET leaveTaken = ?, leaveStart = ?, leaveEnd = ?, comment = ? WHERE rowid = ?",
              (int(days), start_date, end_date, comment, rowid))
    con.commit()
    con.close()

def delete_annual_leave(rowid):
    con = get_connection()
    c = con.cursor()
    c.execute("DELETE FROM annualLeave WHERE rowid = ?", (rowid,))
    con.commit()
    con.close()

def add_sick_leave(emp_id, fname, days, start, end, comment):
    start_leave = parser.parse(start, dayfirst=True).strftime('%d/%m/%Y')
    end_leave = parser.parse(end, dayfirst=True).strftime('%d/%m/%Y')
    con = get_connection()
    c = con.cursor()
    c.execute("INSERT INTO sickLeave VALUES (?, ?, ?, ?, ?, ?)",
              (emp_id, fname, int(days), start_leave, end_leave, comment))
    con.commit()
    con.close()

def get_sick_leave():
    con = get_connection()
    c = con.cursor()
    c.execute("SELECT rowid, * FROM sickLeave ORDER BY ID ASC")
    rows = c.fetchall()
    con.close()
    return [dict(r) for r in rows]

def update_sick_leave(rowid, days, start, end, comment):
    start_date = parser.parse(start, dayfirst=True).strftime('%d/%m/%Y')
    end_date = parser.parse(end, dayfirst=True).strftime('%d/%m/%Y')
    con = get_connection()
    c = con.cursor()
    c.execute("UPDATE sickLeave SET leaveTaken = ?, leaveStart = ?, leaveEnd = ?, comment = ? WHERE rowid = ?",
              (int(days), start_date, end_date, comment, rowid))
    con.commit()
    con.close()

def delete_sick_leave(rowid):
    con = get_connection()
    c = con.cursor()
    c.execute("DELETE FROM sickLeave WHERE rowid = ?", (rowid,))
    con.commit()
    con.close()

def get_all_leave_data(emp_id=None):
    con = get_connection()
    c = con.cursor()

    if emp_id is None:
        c.execute("SELECT * FROM employees")
        employees = c.fetchall()
        c.execute("SELECT * FROM annualLeave")
        annual = c.fetchall()
        c.execute("SELECT * FROM sickLeave")
        sick = c.fetchall()
    else:
        c.execute("SELECT * FROM employees WHERE ID = ?", (emp_id,))
        employees = c.fetchall()
        c.execute("SELECT * FROM annualLeave WHERE ID = ?", (emp_id,))
        annual = c.fetchall()
        c.execute("SELECT * FROM sickLeave WHERE ID = ?", (emp_id,))
        sick = c.fetchall()

    con.close()

    emp_info = {}
    for x in employees:
        eid = x['ID']
        emp_info[eid] = {
            'info': [x['firstName'], x['lastName'], x['startDate']],
            'annual': [],
            'sick': []
        }

    for x in annual:
        eid = x['ID']
        if eid in emp_info:
            emp_info[eid]['annual'].append([x['leaveTaken'], x['leaveStart'], x['leaveEnd'], x['comment']])

    for x in sick:
        eid = x['ID']
        if eid in emp_info:
            emp_info[eid]['sick'].append([x['leaveTaken'], x['leaveStart'], x['leaveEnd'], x['comment']])

    return emp_info
