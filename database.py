import sqlite3
import os
from datetime import datetime
from dateutil import parser
from tkinter import messagebox

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
# DATABASE FUNCTIONS
# ##############################################################################################

def collect_data(table):
	try:
		con = sqlite3.connect("employeeLeave.db")
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		c.execute(f"SELECT * FROM {table}")
		records = c.fetchall()
		
		con.commit()
		con.close()
		
		return records
	
	except Exception as error:
		messagebox.showerror(title='Add Employee Error', message=error)

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


def search_employee_db(search):
	try:
		con = sqlite3.connect("employeeLeave.db")
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		c.execute(f"""SELECT id, firstName, lastName, startDate
 					FROM
 						employees
 					WHERE
 						firstName LIKE '%{search}%'""")
		
		records = c.fetchall()

		con.commit()
		con.close()

		return records
	except Exception as error:
		messagebox.showerror(title='Search Employee Error', message=error)

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




# MAKE INSERT AND COLLECT FUNCTIONS









# c.execute("INSERT INTO employees (ID, firstName, lastName, startDate) VALUES('910610', 'Devon', 'Schuin', '01/01/2025')")
# c.execute("INSERT INTO annualLeave (ID, leaveTaken, leaveStart, leaveEnd) VALUES('910610', 0, '0', '0')")
# c.execute("INSERT INTO annualLeave (ID, leaveTaken, leaveStart, leaveEnd) VALUES('910610', 22, '22', '22')")


# c.execute("SELECT * FROM employees")
# c.execute("SELECT * FROM annualLeave")
# records = c.fetchall()

# print(records)