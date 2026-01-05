import database as db
import annual_leave
from tkinter import *
from tkinter import ttk


root = Tk()

# Add our data to the screen
def builder():
	records = db.collect_data_tree()

	global count
	count = 0
	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4], record[5]), tags=('oddrow',))
		# increment counter
		count += 1
	
# ##############################################################################################
# TREE VIEW
# ##############################################################################################
# Add Some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#D3D3D3")

# Change Selected Color
style.map('Treeview',
	background=[('selected', "#347083")])

# Create a Treeview Frame
tree_frame = Frame()
tree_frame.pack(pady=10)

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
my_tree.pack()

# Configure the Scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Columns
my_tree['columns'] = ("ID", "First Name", "Last Name", "Start Date", "Leave Available", "Sick Leave Available")

# Format Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=150)
my_tree.column("First Name", anchor=W, width=150)
my_tree.column("Last Name", anchor=W, width=150)
my_tree.column("Start Date", anchor=CENTER, width=80)
my_tree.column("Leave Available", anchor=CENTER, width=90)
my_tree.column("Sick Leave Available", anchor=CENTER, width=110)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("First Name", text="First Name", anchor=W)
my_tree.heading("Last Name", text="Last Name", anchor=W)
my_tree.heading("Start Date", text="Start Date", anchor=CENTER)
my_tree.heading("Leave Available", text="Leave Available", anchor=CENTER)
my_tree.heading("Sick Leave Available", text="Sick Leave Available", anchor=CENTER)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

# ##############################################################################################
# FUNCTIONS
# ##############################################################################################

	# ###############
	# EMPLOYEE SETUP
	# ###############
def clear_input():
	id_entry.config(state="normal")
	id_entry.delete(0, END)
	first_entry.delete(0, END)
	last_entry.delete(0, END)
	start_entry.delete(0, END)
	
def add_employee():
	# SORT OUT DATE FORMATE
	id = id_entry.get().upper()
	fname = first_entry.get().capitalize()
	sname = last_entry.get().capitalize()
	start = start_entry.get()

	# Save to database
	db.add_employee_db(id, fname, sname, start)

	# Clear entry boxes
	id_entry.delete(0, END)
	first_entry.delete(0, END)
	last_entry.delete(0, END)
	start_entry.delete(0, END)

	# Refresh
	my_tree.delete(*my_tree.get_children())
	builder()

def update_employee():
	id = id_entry.get()
	fname = first_entry.get().capitalize()
	sname = last_entry.get().capitalize()
	start = start_entry.get()

	# Update in database
	db.update_employee_db(id, fname, sname, start)

	# Clear entry boxes
	id_entry.config(state='normal')
	id_entry.delete(0, END)
	first_entry.delete(0, END)
	last_entry.delete(0, END)
	start_entry.delete(0, END)

	# Refresh
	my_tree.delete(*my_tree.get_children())
	builder()

def delete_employee():
	id = id_entry.get()

	# Delete in database
	db.delete_employee_db(id)

	# Clear entry boxes
	id_entry.config(state='normal')
	id_entry.delete(0, END)
	first_entry.delete(0, END)
	last_entry.delete(0, END)
	start_entry.delete(0, END)

	# Refresh
	my_tree.delete(*my_tree.get_children())
	builder()

# Select Record
def select_record(e):
	# Clear entry boxes
	id_entry.config(state="normal")
	id_entry.delete(0, END)
	first_entry.delete(0, END)
	last_entry.delete(0, END)
	start_entry.delete(0, END)
	
	# Grab record Number
	selected = my_tree.focus()

	# Grab record values
	values = my_tree.item(selected, 'values')

	# output to entry boxes
	id_entry.insert(0, values[0])
	id_entry.config(state="readonly")
	first_entry.insert(0, values[1])
	last_entry.insert(0, values[2])
	start_entry.insert(0, values[3])

	# ###############
	# LEAVE
	# ###############
def add_annual_leave():
	id = id_entry.get()
	fname = first_entry.get()
	sname = last_entry.get()
	
	# Send data to add annual leave	
	add_emp_window = db.add_annual_leave_db(id, fname, sname)
	root.wait_window(add_emp_window)

	# Clear entry boxes
	id_entry.config(state="normal")
	id_entry.delete(0, END)
	first_entry.delete(0, END)
	last_entry.delete(0, END)
	start_entry.delete(0, END)

	# Refresh
	my_tree.delete(*my_tree.get_children())
	builder()

def edit_annual_leave():
	annual_leave.edit()

def add_sick_leave():
	id = id_entry.get()
	fname = first_entry.get()
	sname = last_entry.get()
	
	# Send data to add annual leave	
	add_emp_window = db.add_sick_leave_db(id, fname, sname)
	root.wait_window(add_emp_window)

	# Clear entry boxes
	id_entry.config(state="normal")
	id_entry.delete(0, END)
	first_entry.delete(0, END)
	last_entry.delete(0, END)
	start_entry.delete(0, END)

	# Refresh
	my_tree.delete(*my_tree.get_children())
	builder()

# ##############################################################################################
# WIDGETS
# ##############################################################################################

# Data Frame
data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="x", expand="no", padx=20)

id_label = Label(data_frame, text="ID")
id_label.grid(row=0, column=0, padx=10, pady=10)
id_entry = Entry(data_frame)
id_entry.grid(row=0, column=1, padx=10, pady=10)

first_label = Label(data_frame, text="First Name")
first_label.grid(row=0, column=2, padx=10, pady=10)
first_entry = Entry(data_frame)
first_entry.grid(row=0, column=3, padx=10, pady=10)

last_label = Label(data_frame, text="Last Name")
last_label.grid(row=0, column=4, padx=10, pady=10)
last_entry = Entry(data_frame)
last_entry.grid(row=0, column=5, padx=10, pady=10)

start_label = Label(data_frame, text="Start Date")
start_label.grid(row=0, column=6, padx=10, pady=10)
start_entry = Entry(data_frame)
start_entry.grid(row=0, column=7, padx=10, pady=10)

# Setup Frame
setup_frame = LabelFrame(root, text="Setup Employees")
setup_frame.pack(fill="x", expand="no", padx=20, pady=(20,0))

clear_button = Button(setup_frame, text='Clear', width=12, command=clear_input)
clear_button.grid(row=0, column=0, padx=10, pady=10)

add_employee_button = Button(setup_frame, text='Add Employee', width=12, padx=0, command=add_employee)
add_employee_button.grid(row=0, column=1, padx=10, pady=10)

update_employee_button = Button(setup_frame, text='Update Employee', width=15, command=update_employee)
update_employee_button.grid(row=0, column=2, padx=10, pady=10)

delete_employee_button = Button(setup_frame, text='Delete Employee', width=15, command=delete_employee)
delete_employee_button.grid(row=0, column=3, padx=10, pady=10)

# Leave Frame
leave_frame = LabelFrame(root, text="Annual Leave and Sick Leave")
leave_frame.pack(fill="x", expand="no", padx=20, pady=(20,0))

leave_frame.grid_columnconfigure(2, weight=1)

add_annual_button = Button(leave_frame, text='Add Annual Leave Taken', width=19, command=add_annual_leave)
add_annual_button.grid(row=0, column=0, padx=10, pady=10)

edit_annual_button = Button(leave_frame, text='Edit Annual Leave', width=19, command=edit_annual_leave)
edit_annual_button.grid(row=0, column=1, padx=10, pady=10)

add_sick_button = Button(leave_frame, text='Add Sick Leave Taken', width=19, command=add_sick_leave)
add_sick_button.grid(row=0, column=2, padx=10, pady=10, sticky=E)

# edit_sick_button = Button(leave_frame, text='Edit Sick Leave', width=19, command=edit_sick_leave)
# edit_sick_button.grid(row=0, column=3, padx=10, pady=10, sticky=E)

# Bind the treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# ROOT WINDOW CONFIG
root.title('Annual / Sick Leave')
# root.iconbitmap('icons/smoking.ico')
root.geometry("1000x550")
# root.columnconfigure(0, weight=1)

# RUN BUILDER
builder()

# RUN WINDOW
root.mainloop()