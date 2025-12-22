from tkinter import *
from tkinter import messagebox
from tkcalendar import *
import database as db

def add_employee():
	top = Toplevel()
	top.attributes('-topmost', True)
	top.geometry("400x350")
	top.title("Add Employee")

	# Labels and entry
	id_label = Label(top, text="Employee ID:")
	id_label.grid(row=0, column=0, padx=10, pady=5)
	id_entry = Entry(top)
	id_entry.grid(row=0, column=1, padx=10, pady=5)

	fname_label = Label(top, text="First Name:")
	fname_label.grid(row=1, column=0, padx=10, pady=5)
	fname_entry = Entry(top)
	fname_entry.grid(row=1, column=1, padx=10, pady=5)

	sname_label = Label(top, text="Surname Name:")
	sname_label.grid(row=2, column=0, padx=10, pady=5)
	sname_entry = Entry(top)
	sname_entry.grid(row=2, column=1, padx=10, pady=5)

	cal = Calendar(top)
	cal.grid(row=3, column=1, padx=10, pady=5)

	def save():
		id = id_entry.get().upper()
		fname = fname_entry.get().capitalize()
		sname = sname_entry.get().capitalize()
		start = cal.get_date()

		# Save to database
		db.add_employee_db(id, fname, sname, start)

		# Clear entry boxes
		id_entry.delete(0, END)
		fname_entry.delete(0, END)
		sname_entry.delete(0, END)

		# Close Window
		top.destroy()
	
	save_button = Button(top, text="Save", command=save)
	save_button.grid(row=4, column=0, columnspan=4, sticky=NSEW, padx=10, pady=10)

def update_employee():
	top = Toplevel()
	top.attributes('-topmost', True)
	top.geometry("400x350")
	top.title("Add Employee")

	# Labels and entry
	id_label = Label(top, text="Employee ID:")
	id_label.grid(row=0, column=0, padx=10, pady=5)
	id_entry = Entry(top)
	id_entry.grid(row=0, column=1, padx=10, pady=5)

	fname_label = Label(top, text="First Name:")
	fname_label.grid(row=1, column=0, padx=10, pady=5)
	fname_entry = Entry(top)
	fname_entry.grid(row=1, column=1, padx=10, pady=5)

	sname_label = Label(top, text="Surname Name:")
	sname_label.grid(row=2, column=0, padx=10, pady=5)
	sname_entry = Entry(top)
	sname_entry.grid(row=2, column=1, padx=10, pady=5)
	
	start_label = Label(top, text="Start Date:")
	start_label.grid(row=3, column=0, padx=10, pady=5)
	start_entry = Entry(top)
	start_entry.grid(row=3, column=1, padx=10, pady=5)

	# Grey out unneeded entries
	id_entry.config(state='readonly')
	sname_entry.config(state='readonly')
	start_entry.config(state='readonly')
	
	def search():
		# Get search name
		first_name = fname_entry.get()
		fname_entry.delete(0, END)

		# Get matching results
		search_results = db.search_employee_db(first_name)

		# Grey out unneeded entries
		id_entry.config(state='normal')
		sname_entry.config(state='normal')
		start_entry.config(state='normal')

		# Loop through and select right result
		for x in search_results:
			response = messagebox.askyesno('Employee Information', f'{x} : Is this the right employee?')

			if response == 1:
				id_entry.insert(0, x[0])
				fname_entry.insert(0, x[1])
				sname_entry.insert(0, x[2])
				start_entry.insert(0, x[3])
				id_entry.config(state='readonly')
				break

	def update():
		id = id_entry.get()
		fname = fname_entry.get().capitalize()
		sname = sname_entry.get().capitalize()
		start = start_entry.get()

		db.update_employee_db(id, fname, sname, start)

		# Clear entry boxes
		id_entry.config(state='normal')
		id_entry.delete(0, END)
		fname_entry.delete(0, END)
		sname_entry.delete(0, END)
		start_entry.delete(0, END)

	search_button = Button(top, text="Search Employee", command=search)
	search_button.grid(row=4, column=0, columnspan=4, sticky=NSEW, padx=10, pady=10)

	update_button = Button(top, text="Update Employee", command=update)
	update_button.grid(row=5, column=0, columnspan=4, sticky=NSEW, padx=10, pady=10)