import sqlite3
import os
import sys
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from datetime import date
from dateutil import parser
from dateutil import relativedelta


# ##############################################################################################
# GET DATABASE LOCATION
# ##############################################################################################

def get_db_path(db_filename):
	"""
	Returns the path to the database.
	- If Frozen (EXE): Returns path inside the _internal folder.
	- If Live (Dev): Returns path in the project folder.
	"""
	if getattr(sys, 'frozen', False):
		# sys._MEIPASS points to the _internal folder in --onedir mode
		base_path = sys._MEIPASS
	else:
		# We are running as a normal Python script
		base_path = os.path.dirname(os.path.abspath(__file__))
		
	return os.path.join(base_path, db_filename)


# ##############################################################################################
# INITIALIZE DATABASE
# ##############################################################################################

# Get database path
database_path = get_db_path('employeeLeave.db')

if not os.path.exists(database_path):
	con = sqlite3.connect(database_path)
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
			firstName Text,
			leaveTaken INTEGER,
			leaveStart TEXT,
			leaveEnd TEXT,
			FOREIGN KEY (ID) REFERENCES employees (ID)
			ON DELETE CASCADE
			)'''
		)
	
	c.execute('''CREATE TABLE IF NOT EXISTS sickLeave (
			ID TEXT,
			firstName Text,
			leaveTaken INTEGER,
			leaveStart TEXT,
			leaveEnd TEXT,
			FOREIGN KEY (ID) REFERENCES employees (ID)
			ON DELETE CASCADE
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
		con = sqlite3.connect(database_path)
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		c.execute(f"SELECT * FROM employees")
		emp_rec = c.fetchall()

		c.execute(f"SELECT * FROM annualLeave")
		leave_taken = c.fetchall()
		
		c.execute(f"SELECT * FROM sickLeave")
		sick_taken = c.fetchall()
		
		con.commit()
		con.close()

		# GET ANNUAL LEAVE		
		# Get date now
		now = datetime.now()
		date_now = now.strftime("%d/%m/%Y")

		# Make into list
		emp_rec_list = []

		for x in emp_rec:
			emp_rec_list.append([x[0], x[1], x[2], x[3]])

		# Add leave days to employee info
		empolyee_info = []

		for rec in emp_rec_list:
			# ##################################
			# GET ANNUAL LEAVE
			# ##################################

			# Convert string to date object
			start_date = datetime.strptime(rec[3], "%d/%m/%Y")
			end_date = datetime.strptime(date_now, "%d/%m/%Y")

			# Get the relativedelta between two dates
			delta = relativedelta.relativedelta(end_date, start_date)

			# Get months difference for annual leave
			months = delta.months + (delta.years * 12)
			leave_days = months * 1.25

			# Get leave days already taken
			for leave in leave_taken:
				if rec[0] == leave[0]:
					leave_days -= leave[2]

			# ##################################
			# GET SICK LEAVE
			# ##################################
			
			# Get todays date and employee start date into date object
			today_date = date.today()
			format_start_date = start_date.strftime("%d.%m.%Y")
			# datetime.strptime(rec[3], "%d/%m/%Y").strftime("%d.%m.%Y")
			emp_start_date = datetime.strptime(format_start_date, "%d.%m.%Y").date()

			# Calculate the relative difference
			delta = relativedelta.relativedelta(today_date, emp_start_date)

			# Convert years to months and add remaining months
			total_months = delta.years * 12 + delta.months

			# Get current cycle
			current_cycle = int(total_months / 36)

			# Get start and end cycle dates
			start_cycle_date = emp_start_date + relativedelta.relativedelta(months=(current_cycle * 36))
			end_cycle_date = emp_start_date + relativedelta.relativedelta(months=((current_cycle + 1) * 36))

			# Check if leave is taken in current cycle
			sick_leave_taken = 0

			for leave in sick_taken:
				# Convert date to right format
				if rec[0] == leave[0]:
					format_date = datetime.strptime(leave[3], "%d/%m/%Y").strftime("%d.%m.%Y")
					leave_start_date = datetime.strptime(format_date, "%d.%m.%Y").date()

					# Check if leave dates in current cycle
					if start_cycle_date <= leave_start_date <= end_cycle_date:
						sick_leave_taken += leave[2]	
			
			# ##################################
			# APPEND ALL LEAVE TO LIST
			# ##################################

			# Add leave days to eployee data
			emp_info = rec + [leave_days] + [36 - sick_leave_taken]
			# print(emp_info)
			empolyee_info.append(emp_info)

		return empolyee_info
		
	except Exception as error:
		messagebox.showerror(title='Add Employee Error', message=error)

def collect_data_annual_leave_tree():		
	try:
		con = sqlite3.connect(database_path)
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		c.execute(f"SELECT * FROM annualLeave ORDER BY ID ASC")
		records = c.fetchall()
		
		con.commit()
		con.close()
		
		return records
		
	except Exception as error:
		messagebox.showerror(title='Add Employee Error', message=error)

def collect_data_sick_leave_tree():		
	try:
		con = sqlite3.connect(database_path)
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		c.execute(f"SELECT * FROM sickLeave ORDER BY ID ASC")
		records = c.fetchall()
		
		con.commit()
		con.close()
		
		return records
		
	except Exception as error:
		messagebox.showerror(title='Add Employee Error', message=error)

def collect_data_view(id=None):
		con = sqlite3.connect(database_path)
		c = con.cursor()

		# Turn on foreign keys
		c.execute('PRAGMA foreign_keys = ON')

		if id == None:
			c.execute("SELECT * FROM employees")
			employees = c.fetchall()

			c.execute("SELECT * FROM annualLeave")
			annual_leave_taken = c.fetchall()
			
			c.execute("SELECT * FROM sickLeave")
			sick_leave_taken = c.fetchall()
		else:
			c.execute(f"SELECT * FROM employees WHERE id = {id}")
			employees = c.fetchall()

			c.execute(f"SELECT * FROM annualLeave WHERE id = {id}")
			annual_leave_taken = c.fetchall()
			
			c.execute(f"SELECT * FROM sickLeave WHERE id = {id}")
			sick_leave_taken = c.fetchall()
		
		con.commit()
		con.close()

		# Put all employee info and leave in to dic
		emp_info = {}

		for x in employees:
			id = x[0]
			fname = x[1]
			sname = x[2]
			start_date = x[3]

			# Add ID key to dict
			emp_info[id] = {}

			# Add employee info to dict
			emp_info[id]['info'] = [fname, sname, start_date]

		for x in annual_leave_taken:
			id = x[0]
			al_days = x[2]
			lsd = x[3]
			led = x[4]

			# Add employee annual leave to dict
			emp_info[id].setdefault('annual', []).append([al_days, lsd, led])


		for x in sick_leave_taken:
			id = x[0]
			sl_days = x[2]
			ssd = x[3]
			sed = x[4]

			# Add employee sick leave to dict
			emp_info[id].setdefault('sick', []).append([al_days, lsd, led])

		return emp_info

def collect_data_docs():
	con = sqlite3.connect(database_path)
	c = con.cursor()

	# Turn on foreign keys
	c.execute('PRAGMA foreign_keys = ON')

	c.execute(f"SELECT * FROM employees")
	employees = c.fetchall()
	
	con.commit()
	con.close()

	return employees

# ##############################################################################################
# SETUP EMPLOYEE FUNCTIONS
# ##############################################################################################

# Add employee to database
def add_employee_db(id, fname, sname, start):
	try:
		con = sqlite3.connect(database_path)
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
		con = sqlite3.connect(database_path)
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
		con = sqlite3.connect(database_path)
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

	# ############
	# ANNUAL LEAVE
	# ############

# Add employee annual leave
def add_annual_leave_db(id, fname, sname):
	if id == '':
		messagebox.showerror(title='ID Not Exist', message='No Employee Selected, Please Select An Employee')
	else:
		top = Toplevel()
		top.attributes('-topmost', 'true')
		top.geometry("300x300")
		top.title("Add Annual Leave")

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
				con = sqlite3.connect(database_path)
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
						c.execute("INSERT INTO annualLeave VALUES (:id, :firstName, :leaveTaken, :leaveStart, :leaveEnd)",
								{
									'id' : id,
									'firstName' : fname,
									'leaveTaken' : leave_days,
									'leaveStart' : start_leave,
									'leaveEnd' : end_leave
								})
						
						# Display complete
						messagebox.showinfo(title='Add Employee Annual Leave', message='Added Employee Annual Leave Successfully')

						# Close window
						top.destroy()
				else:
					c.execute("INSERT INTO annualLeave VALUES (:id, :firstName, :leaveTaken, :leaveStart, :leaveEnd)",
								{
									'id' : id,
									'firstName' : fname,
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

		return top
	
# Edit annual Leave
def update_leave_db(top, id, days, start_date, end_date):
	try:
		if days == '' or start_date == '' or end_date == '':
			raise Exception("Information Empty!")
		else:
			response = messagebox.askyesno(title='Update Leave', message='Are You Sure You Want To Update Leave Infomation', 
			parent=top)

			if response == 1:
				con = sqlite3.connect(database_path)
				c = con.cursor()

				# Turn on foreign keys
				c.execute('PRAGMA foreign_keys = ON')

				c.execute('''UPDATE annualLeave SET
								leaveTaken = :leaveTaken,
								leaveStart = :leaveStart,
								leaveEnd = :leaveEnd
					
								WHERE id = :id''',
								{
									'id' : id,
									'leaveTaken' : days,
									'leaveStart' : start_date,
									'leaveEnd' : end_date
								})
				
				con.commit()
				con.close()
				
				# Display complete
				messagebox.showinfo(title='Update Leave', message='Updated Employee Leave Successfully', parent=top)

	except Exception as error:
		messagebox.showerror(title='Update Leave Error', message=error, parent=top)

# Delete annual Leave
def delete_leave_db(top, id, start_date, end_date):
	try:
		response = messagebox.askyesno(title='Delete Leave', message='Are You Sure You Want To Delete Leave Infomation', 
			parent=top)
		
		if response == 1:
			con = sqlite3.connect(database_path)
			c = con.cursor()

			# Turn on foreign keys
			c.execute('PRAGMA foreign_keys = ON')

			c.execute('''DELETE FROM annualLeave 
						WHERE id = :id 
						AND leaveStart = :leaveStart 
						AND leaveEnd = :leaveEnd''',
						{
							'id' : id,
							'leaveStart' : start_date,
							'leaveEnd' : end_date
							
						})
			
			con.commit()
			con.close()

			# Display complete
			messagebox.showinfo(title='Delete Leave', message='Deleted Employee Leave Successfully', parent=top)

	except Exception as error:
		messagebox.showerror(title='Delete Leave Error', message=error, parent=top)

	# ############
	# SICK LEAVE
	# ############

# Add employee sick leave
def add_sick_leave_db(id, fname, sname):
	if id == '':
		messagebox.showerror(title='ID Not Exist', message='No Employee Selected, Please Select An Employee')
	else:
		top = Toplevel()
		top.attributes('-topmost', 'true')
		top.geometry("300x300")
		top.title("Add Sick Leave")

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
				con = sqlite3.connect(database_path)
				c = con.cursor()

				# Turn on foreign keys
				c.execute('PRAGMA foreign_keys = ON')

				# Parse dates to right format
				start_leave = str(parser.parse(leave_start, dayfirst=True).strftime('%d/%m/%Y'))
				end_leave = str(parser.parse(leave_end, dayfirst=True).strftime('%d/%m/%Y'))

				# Check to see nothing was left out
				if leave_days == '' or leave_start == '' or leave_end == '':
					response = messagebox.askyesno(title='Add Employee Sick Leave', message='Some Employee Info Blank. Is This OK?')
					
					if response == 1:
						c.execute("INSERT INTO sickLeave VALUES (:id, :firstName, :leaveTaken, :leaveStart, :leaveEnd)",
								{
									'id' : id,
									'firstName' : fname,
									'leaveTaken' : leave_days,
									'leaveStart' : start_leave,
									'leaveEnd' : end_leave
								})
						
						# Display complete
						messagebox.showinfo(title='Add Employee Sick Leave', message='Added Employee Annual Leave Successfully')

						# Close window
						top.destroy()
				else:
					c.execute("INSERT INTO sickLeave VALUES (:id, :firstName, :leaveTaken, :leaveStart, :leaveEnd)",
								{
									'id' : id,
									'firstName' : fname,
									'leaveTaken' : leave_days,
									'leaveStart' : start_leave,
									'leaveEnd' : end_leave
								})
					
					# Display complete
					messagebox.showinfo(title='Add Employee Sick Leave', message='Added Employee Annual Leave Successfully')

					# Close window
					top.destroy()
					
				con.commit()
				con.close()
				
			except Exception as error:
				messagebox.showerror(title='Add Employee Sick Leave', message=error)
			
		save_button = Button(top, text="Save", command=save)
		save_button.grid(row=6, column=0, columnspan=2, sticky=NSEW, padx=10, pady=10)

		return top

# Edit sick annual Leave
def update_sick_leave_db(top, id, days, start_date, end_date):
	try:
		if days == '' or start_date == '' or end_date == '':
			raise Exception("Information Empty!")
		else:
			response = messagebox.askyesno(title='Update Sick Leave', message='Are You Sure You Want To Update Leave Infomation', 
			parent=top)

			if response == 1:
				con = sqlite3.connect(database_path)
				c = con.cursor()

				# Turn on foreign keys
				c.execute('PRAGMA foreign_keys = ON')

				c.execute('''UPDATE sickLeave SET
								leaveTaken = :leaveTaken,
								leaveStart = :leaveStart,
								leaveEnd = :leaveEnd
					
								WHERE id = :id''',
								{
									'id' : id,
									'leaveTaken' : days,
									'leaveStart' : start_date,
									'leaveEnd' : end_date
								})
				
				con.commit()
				con.close()
				
				# Display complete
				messagebox.showinfo(title='Update Sick Leave', message='Updated Employee Sick Leave Successfully', parent=top)

	except Exception as error:
		messagebox.showerror(title='Update Sick Leave Error', message=error, parent=top)

# Delete sick Leave
def delete_sick_leave_db(top, id, start_date, end_date):
	try:
		response = messagebox.askyesno(title='Delete Sick Leave', message='Are You Sure You Want To Delete Sick Leave Infomation', 
			parent=top)
		
		if response == 1:
			con = sqlite3.connect(database_path)
			c = con.cursor()

			# Turn on foreign keys
			c.execute('PRAGMA foreign_keys = ON')

			c.execute('''DELETE FROM sickLeave 
						WHERE id = :id 
						AND leaveStart = :leaveStart 
						AND leaveEnd = :leaveEnd''',
						{
							'id' : id,
							'leaveStart' : start_date,
							'leaveEnd' : end_date
							
						})
			
			con.commit()
			con.close()

			# Display complete
			messagebox.showinfo(title='Delete Sick Leave', message='Deleted Employee Sick Leave Successfully', parent=top)

	except Exception as error:
		messagebox.showerror(title='Delete Sick Leave Error', message=error, parent=top)