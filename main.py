from tkinter import *
from tkinter import messagebox
from tkcalendar import *
import database as db

root = Tk()

# ##############################################################################################
# FUNCTIONS
# ##############################################################################################
def add_employee():
	top = Toplevel()
	top.attributes('-topmost', True)
	top.geometry("400x350")
	top.title("Add Employee")

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
	
	save_button = Button(top, text="Save", command=save)
	save_button.grid(row=4, column=0, columnspan=4, sticky=NSEW, padx=10, pady=10)

def update_employee():
	pass


# ##############################################################################################
# WIDGETS
# ##############################################################################################

# Setup buttons
setup_label = Label(root, text='EMPLOYEE SETUP',borderwidth=1, relief='solid')

add_employee_button = Button(root, text='Add Employee', width=12, command=add_employee)
update_employee_button = Button(root, text='Add Employee', width=12, command=update_employee)

# ##############################################################################################
# BIND WIDGETS
# ##############################################################################################

# Setup Buttons
setup_label.grid(row=0, column=0, columnspan=4 ,sticky=W+E, padx=(5,5), pady=(0,10))

add_employee_button.grid(row=1, column=0, padx=(5,10))
update_employee_button.grid(row=1, column=1, padx=(5,10))
# setup_button2.grid(row=1, column=1, padx=(0,10))
# setup_button3.grid(row=1, column=2, padx=(0,10))
# setup_button4.grid(row=1, column=3, padx=(0,5))
# setup_button5.grid(row=2, column=0, columnspan=2 ,sticky=W+E, padx=(5,5) ,pady=(10,10))
# setup_button6.grid(row=2, column=2, columnspan=2 ,sticky=W+E, padx=(5,5) ,pady=(10,10))

















# ROOT WINDOW CONFIG
root.title('Annual / Sick Leave')
# root.iconbitmap('icons/smoking.ico')
root.geometry('440x490')
# root.columnconfigure(0, weight=1)

# RUN WINDOW
root.mainloop()