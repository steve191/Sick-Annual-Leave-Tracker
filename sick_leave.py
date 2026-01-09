from tkinter import *
from tkinter import ttk
import database as db


def edit():
	top = Toplevel()
	top.attributes('-topmost', 'true')
	top.geometry("1150x550")
	top.title("Edit Sick Leave")

	def builder():
		records = db.collect_data_sick_leave_tree()

		my_tree.delete(*my_tree.get_children())

		global count
		count = 0
		for record in records:
			if count % 2 == 0:
				my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
			else:
				my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
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
	tree_frame = Frame(top)
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
	my_tree['columns'] = ("ID", "First Name", "Sick Leave Days", "Start Date", "End Date")

	# Format Columns
	my_tree.column("#0", width=0, stretch=NO)
	my_tree.column("ID", anchor=W, width=150)
	my_tree.column("First Name", anchor=W, width=150)
	my_tree.column("Sick Leave Days", anchor=W, width=150)
	my_tree.column("Start Date", anchor=CENTER, width=100)
	my_tree.column("End Date", anchor=CENTER, width=110)

	# Create Headings
	my_tree.heading("#0", text="", anchor=W)
	my_tree.heading("ID", text="ID", anchor=W)
	my_tree.heading("First Name", text="First Name", anchor=W)
	my_tree.heading("Sick Leave Days", text="Sick Leave Days", anchor=W)
	my_tree.heading("Start Date", text="Start Date", anchor=CENTER)
	my_tree.heading("End Date", text="End Date", anchor=CENTER)

	# Create Striped Row Tags
	my_tree.tag_configure('oddrow', background="white")
	my_tree.tag_configure('evenrow', background="lightblue")

	# ##############################################################################################
	# FUNCTIONS
	# ##############################################################################################

	def select_record(e):
		# Clear entry boxes
		id_entry.config(state="normal")
		id_entry.delete(0, END)
		first_entry.delete(0, END)
		leave_days_entry.delete(0, END)
		start_entry.delete(0, END)
		end_entry.delete(0, END)
		
		# Grab record Number
		selected = my_tree.focus()

		# Grab record values
		values = my_tree.item(selected, 'values')

		# output to entry boxes
		id_entry.insert(0, values[0])
		id_entry.config(state="readonly")
		first_entry.insert(0, values[1])
		first_entry.config(state="readonly")
		leave_days_entry.insert(0, values[2])
		start_entry.insert(0, values[3])
		end_entry.insert(0, values[4])

	def clear_input():
		id_entry.config(state="normal")
		id_entry.delete(0, END)
		first_entry.delete(0, END)
		leave_days_entry.delete(0, END)
		start_entry.delete(0, END)
		end_entry.delete(0, END)

	def update_leave():
		id = id_entry.get()
		days = leave_days_entry.get()
		start_date = start_entry.get()
		end_date = end_entry.get()

		# Update info
		db.update_sick_leave_db(top, id, days, start_date, end_date)

		# Clear input
		id_entry.config(state="normal")
		id_entry.delete(0, END)
		first_entry.config(state="normal")
		first_entry.delete(0, END)
		leave_days_entry.delete(0, END)
		start_entry.delete(0, END)
		end_entry.delete(0, END)

		# Refresh
		my_tree.delete(*my_tree.get_children())
		builder()

	def delete_leave():
		id = id_entry.get()
		start_date = start_entry.get()
		end_date = end_entry.get()

		# Delete leave
		db.delete_sick_leave_db(top, id, start_date, end_date)

			# Clear input
		id_entry.config(state="normal")
		id_entry.delete(0, END)
		first_entry.config(state="normal")
		first_entry.delete(0, END)
		leave_days_entry.delete(0, END)
		start_entry.delete(0, END)
		end_entry.delete(0, END)

		# Refresh
		my_tree.delete(*my_tree.get_children())
		builder()

	# ##############################################################################################
	# WIDGETS
	# ##############################################################################################

	# Data Frame
	data_frame = LabelFrame(top, text="Record")
	data_frame.pack(fill="x", expand="no", padx=20)

	id_label = Label(data_frame, text="ID")
	id_label.grid(row=0, column=0, padx=10, pady=10)
	id_entry = Entry(data_frame)
	id_entry.grid(row=0, column=1, padx=10, pady=10)

	first_label = Label(data_frame, text="First Name")
	first_label.grid(row=0, column=2, padx=10, pady=10)
	first_entry = Entry(data_frame)
	first_entry.grid(row=0, column=3, padx=10, pady=10)

	leave_days_label = Label(data_frame, text="Leave Days")
	leave_days_label.grid(row=0, column=4, padx=10, pady=10)
	leave_days_entry = Entry(data_frame)
	leave_days_entry.grid(row=0, column=5, padx=10, pady=10)

	start_label = Label(data_frame, text="Start Date")
	start_label.grid(row=0, column=6, padx=10, pady=10)
	start_entry = Entry(data_frame)
	start_entry.grid(row=0, column=7, padx=10, pady=10)

	end_label = Label(data_frame, text="End Date")
	end_label.grid(row=0, column=8, padx=10, pady=10)
	end_entry = Entry(data_frame)
	end_entry.grid(row=0, column=9, padx=10, pady=10)

	# Button Frame
	button_frame = LabelFrame(top, text="Leave Buttons")
	button_frame.pack(fill="x", expand="no", padx=20, pady=(20,0))

	clear_button = Button(button_frame, text='Clear', width=12, command=clear_input)
	clear_button.grid(row=0, column=0, padx=10, pady=10)

	update_button = Button(button_frame, text='Update Leave', width=12, command=update_leave)
	update_button.grid(row=0, column=1, padx=10, pady=10)

	delete_button = Button(button_frame, text='Delete Leave', width=12, command=delete_leave)
	delete_button.grid(row=0, column=2, padx=10, pady=10)

	# Bind the treeview
	my_tree.bind("<ButtonRelease-1>", select_record)

	# Build tree
	builder()

	return top