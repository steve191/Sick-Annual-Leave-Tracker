import sqlite3
import os
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from dateutil import parser
from dateutil import relativedelta
# import annual_leave as al

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
# TREE VIEW FUNCTIONS
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
		
		con.commit()
		con.close()
		
		# Get date now
		now = datetime.now()
		date_now = now.strftime("%d/%m/%Y")

		# Make into list
		rec_list = []

		for x in emp_rec:
			rec_list.append([x[0], x[1], x[2], x[3]])

		# Add leave days to employee info
		empolyee_info = []

		for rec in rec_list:
			# convert string to date object
			start_date = datetime.strptime(rec[3], "%d/%m/%Y")
			end_date = datetime.strptime(date_now, "%d/%m/%Y")

			# Get the relativedelta between two dates
			delta = relativedelta.relativedelta(end_date, start_date)

			# Get months difference
			months = delta.months + (delta.years * 12)
			leave_days = months * 1.25
			
			# Get leave days already taken
			for leave in leave_taken:
				if rec[0] == leave[0]:
					leave_days -= leave[1]

			# Add leave days to eployee data
			emp_info = rec + [leave_days]
			# print(emp_info)
			empolyee_info.append(emp_info)

		return empolyee_info
		
	except Exception as error:
		messagebox.showerror(title='Add Employee Error', message=error)

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

			start_date = str(parser.parse(start, dayfirst=True).strftime('%d/%m/%Y'))

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



# ##################
# WORKING
# ##################

# Add employee annual leave
def add_annual_leave_db(id, fname, sname):
	if id == '':
		messagebox.showerror(title='ID Not Exist', message='No Employee Selected, Please Select An Employee')
	else:
		top = Toplevel()
		top.attributes('-topmost', 'true')
		top.geometry("300x300")
		top.title("Rule Name")

		# ID
		id_label = Label(top, text="ID:")
		id_label.grid(row=0, column=0, padx=10, pady=10)
		id_entry = Entry(top)
		id_entry.grid(row=0, column=1, padx=10, pady=10)
		id_entry.insert(0,id)
		id_entry.config(state='readonly')
		
		# First name
		fname_label = Label(top, text="First Name:")
		fname_label.grid(row=1, column=0, padx=10, pady=10)
		fname_entry = Entry(top)
		fname_entry.grid(row=1, column=1, padx=10, pady=10)
		fname_entry.insert(0,fname)
		fname_entry.config(state='readonly')
		
		# Last name
		sname_label = Label(top, text="Last Name:")
		sname_label.grid(row=2, column=0, padx=10, pady=10)
		sname_entry = Entry(top)
		sname_entry.grid(row=2, column=1, padx=10, pady=10)
		sname_entry.insert(0,sname)
		sname_entry.config(state='readonly')

		# Leave taken (No. days)
		leave_label = Label(top, text="Leave Taken in days:")
		leave_label.grid(row=3, column=0, padx=10, pady=10)
		leave_entry = Entry(top)
		leave_entry.grid(row=3, column=1, padx=10, pady=10)

		# Leave Start 
		leave_start_label = Label(top, text="Leave Start Date:")
		leave_start_label.grid(row=4, column=0, padx=10, pady=10)
		leave_start_entry = Entry(top)
		leave_start_entry.grid(row=4, column=1, padx=10, pady=10)

		# Leave End
		leave_end_label = Label(top, text="Leave End Date:")
		leave_end_label.grid(row=5, column=0, padx=10, pady=10)
		leave_end_entry = Entry(top)
		leave_end_entry.grid(row=5, column=1, padx=10, pady=10)

		def save():
			id = id_entry.get()
			leave_days = leave_entry.get()
			leave_start = leave_start_entry.get()
			leave_end = leave_end_entry.get()

			# Add leave to database
			try:
				con = sqlite3.connect("employeeLeave.db")
				c = con.cursor()

				# Turn on foreign keys
				c.execute('PRAGMA foreign_keys = ON')

				# Parse dates to right format
				start_leave = str(parser.parse(leave_start, dayfirst=True).strftime('%d/%m/%Y'))
				end_leave = str(parser.parse(leave_end, dayfirst=True).strftime('%d/%m/%Y'))

				# Check to see nothing was left out
				if leave_days == '' or leave_start == '' or leave_end == '':
					response = messagebox.askyesno(title='Add Employee Annual Leave', message='Some Employee Info Blank. Is This OK?')
					
					if response == 1:
						c.execute("INSERT INTO annualLeave VALUES (:id, :leaveTaken, :leaveStart, :leaveEnd)",
								{
									'id' : id,
									'leaveTaken' : leave_days,
									'leaveStart' : start_leave,
									'leaveEnd' : end_leave
								})
						
						# Display complete
						messagebox.showinfo(title='Add Employee Annual Leave', message='Added Employee Annual Leave Successfully')

						# Close window
						top.destroy()
				else:
					c.execute("INSERT INTO annualLeave VALUES (:id, :leaveTaken, :leaveStart, :leaveEnd)",
								{
									'id' : id,
									'leaveTaken' : leave_days,
									'leaveStart' : start_leave,
									'leaveEnd' : end_leave
								})
					
					# Display complete
					messagebox.showinfo(title='Add Employee Annual Leave', message='Added Employee Annual Leave Successfully')

					# Close window
					top.destroy()
				con.commit()
				con.close()
				
			except Exception as error:
				messagebox.showerror(title='Add Employee Annual Leave', message=error)

		save_button = Button(top, text="Save", command=save)
		save_button.grid(row=6, column=0, columnspan=2, sticky=NSEW, padx=10, pady=10)