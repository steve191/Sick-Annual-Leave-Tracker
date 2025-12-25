import sqlite3
import os
from datetime import datetime
from dateutil import parser
from tkinter import messagebox
import annual_leave as al

# ##############################################################################################
# INITIALIZE DATABASE
# ##############################################################################################

if not os.path.exists('employeeLeave.db'):
	con = sqlite3.connect("employeeLeave.db")
	c = con.cursor()

	# Turn on foreign keys
	c.execute('PRAGMA foreign_keys = ON')

	c.execute('''CREATE TABLE IF NOT EXISTS employees (
			ID TEXT NOT NULL PRIMARY KEY,
			firstName TEXT,
			lastName TEXT,
			startDate TEXT
			)'''
		)

	c.execute('''CREATE TABLE IF NOT EXISTS annualLeave (
			ID TEXT,
			leaveTaken INTEGER,
			leaveStart TEXT,
			LeaveEnd TEXT,
			FOREIGN KEY (ID) REFERENCES employees (ID)
			)'''
		)

	con.commit()
	con.close()

# ##############################################################################################
# SETUP EMPLOYEE FUNCTIONS
# ##############################################################################################

# Add employee to database
def add_employee_db(id, fname, sname, start):
	try:
		con = sqlite3.connect("employeeLeave.db")
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		# Check to see if not empty strings
		if id != '' or fname != '' or sname != '' or start != '':

			start_date = str(parser.parse(start).strftime('%d/%m/%Y'))

			c.execute("INSERT INTO employees VALUES (:id, :firstName, :lastName, :startDate)",
						{
							'id' : id,
							'firstName' : fname,
							'lastName' : sname,
							'startDate' : start_date
						})
		else:
			raise Exception("All Information Must Be Filled Out!")
		
		con.commit()
		con.close()
		
		# Display complete
		messagebox.showinfo(title='Add Employee', message='Added Employee Successfully')

	except Exception as error:
		messagebox.showerror(title='Add Employee Error', message=error)

# Update employee in database
def update_employee_db(id, fname, sname, start_date):
	try:
		con = sqlite3.connect("employeeLeave.db")
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		c.execute('''UPDATE employees SET
						firstName = :firstName,
						lastName = :lastName,
						startDate = :startDate

						WHERE id = :id''',
						{
							'id' : id,
							'firstName' : fname,
							'lastName' : sname,
							'startDate' : start_date
						})
		
		con.commit()
		con.close()
		
		# Display complete
		messagebox.showinfo(title='Update Employee', message='Updated Employee Successfully')

	except Exception as error:
		messagebox.showerror(title='Update Employee Error', message=error)

# Update employee in database
def delete_employee_db(id):
	try:
		con = sqlite3.connect("employeeLeave.db")
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		c.execute("DELETE FROM employees WHERE id = :id",
						{
							'id' : id
						})
		
		con.commit()
		con.close()
		
		# Display complete
		messagebox.showinfo(title='Delete Employee', message='Deleted Employee Successfully')

	except Exception as error:
		messagebox.showerror(title='Delete Employee Error', message=error)


# ##############################################################################################
# DATABSE FUNCTIONS
# ##############################################################################################

# Collect info from database for tree view
def collect_data_tree():		
	try:
		con = sqlite3.connect("employeeLeave.db")
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		c.execute(f"SELECT * FROM employees")
		emp_rec = c.fetchall()

		c.execute(f"SELECT * FROM annualLeave")
		leave_taken = c.fetchall()

		empoyee_info = al.cal_acc_leave(emp_rec, leave_taken)
		
		con.commit()
		con.close()
		
		return empoyee_info
	
	except Exception as error:
		messagebox.showerror(title='Add Employee Error', message=error)

# Add employee annual leave
def add_annual_leave_db():
	pass