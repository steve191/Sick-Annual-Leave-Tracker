import sqlite3
import os
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

def add_employee_db(id, fname, sname, start_date):
	try:
		con = sqlite3.connect("employeeLeave.db")
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		c.execute("INSERT INTO employees VALUES (:id, :firstName, :lastName, :startDate)",
						{
							'id' : id,
							'firstName' : fname,
							'lastName' : sname,
							'startDate' : start_date
						})
		
		con.commit()
		con.close()
		
		# Display complete
		messagebox.showinfo(title='Add Employee', message='Added Employee Successfully')

	except Exception as error:
		messagebox.showerror(title='Add Employee Error', message=error)




# def search():
# 				# Get search name
# 				english_name = ename_entry.get()
# 				ename_entry.delete(0, END)

# 				# Get matching results
# 				search_results = pay.search_employees(english_name)

# 				# Loop through and select right result
# 				for x in search_results:
# 					response = messagebox.askyesno('Employee Information', f'{x} : Is this the right employee?')

# 					if response == 1:
# 						ename_entry.insert(0, x[0])
# 						fname_entry.insert(0, x[1])
# 						sname_entry.insert(0, x[2])
# 						id_entry.insert(0, x[3])
# 						break


# c.execute(f"""SELECT englishName,
# 						fullName,
# 						Surname,
# 						idPass
# 					FROM
# 						employeeNames
# 					WHERE
# 						englishName LIKE '%{search}%'""")


# MAKE INSERT AND COLLECT FUNCTIONS









# c.execute("INSERT INTO employees (ID, firstName, lastName, startDate) VALUES('910610', 'Devon', 'Schuin', '01/01/2025')")
# c.execute("INSERT INTO annualLeave (ID, leaveTaken, leaveStart, leaveEnd) VALUES('910610', 0, '0', '0')")
# c.execute("INSERT INTO annualLeave (ID, leaveTaken, leaveStart, leaveEnd) VALUES('910610', 22, '22', '22')")


# c.execute("SELECT * FROM employees")
# c.execute("SELECT * FROM annualLeave")
# records = c.fetchall()

# print(records)