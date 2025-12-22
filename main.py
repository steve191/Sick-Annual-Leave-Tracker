from tkinter import *
from tkinter import ttk
import employee_setup as setup
import database as db

root = Tk()

# Add our data to the screen
def builder():
	records = db.collect_data('employees')

	my_tree.delete(*my_tree.get_children())

	global count
	count = 0
	for record in records:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3]), tags=('oddrow',))
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
my_tree['columns'] = ("ID", "First Name", "Last Name", "Start Date")

# Format Columns
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=200)
my_tree.column("First Name", anchor=W, width=200)
my_tree.column("Last Name", anchor=W, width=200)
my_tree.column("Start Date", anchor=CENTER, width=100)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("First Name", text="First Name", anchor=W)
my_tree.heading("Last Name", text="Last Name", anchor=W)
my_tree.heading("Start Date", text="Start Date", anchor=CENTER)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

# ##############################################################################################
# FUNCTIONS
# ##############################################################################################

def add_employee():
	# SORT OUT DATE FORMATE
	id = id_entry.get().upper()
	fname = first_entry.get().capitalize()
	sname = last_entry.get().capitalize()
	start = start_entry.get()

	# # Save to database
	db.add_employee_db(id, fname, sname, start)

	# Clear entry boxes
	id_entry.delete(0, END)
	first_entry.delete(0, END)
	last_entry.delete(0, END)
	start_entry.delete(0, END)

	# Refresh
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
	
# ##############################################################################################
# WIDGETS
# ##############################################################################################

# Data Frame
data_frame = LabelFrame(root, text="Record")
data_frame.pack(fill="x", expand="yes", padx=20)

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
setup_frame.pack(fill="x", expand="yes", padx=20)

add_employee_button = Button(setup_frame, text='Add Employee', width=12, command=add_employee)
add_employee_button.grid(row=1, column=0, padx=10, pady=10)
update_employee_button = Button(setup_frame, text='Update Employee', width=12, command=setup.update_employee)
update_employee_button.grid(row=1, column=1, padx=10, pady=10)

# Bind the treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# ROOT WINDOW CONFIG
root.title('Annual / Sick Leave')
# root.iconbitmap('icons/smoking.ico')
root.geometry("1000x500")
# root.columnconfigure(0, weight=1)

# RUN BUILDER
builder()

# RUN WINDOW
root.mainloop()