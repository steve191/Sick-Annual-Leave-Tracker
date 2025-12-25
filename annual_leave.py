from tkinter import *
from tkinter import messagebox
from datetime import datetime
from dateutil import relativedelta


def cal_acc_leave(emp_rec, leave_taken):
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

def add_annual_leave(id, fname, sname):
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
			pass
		# 	rule_name = name_entry.get()
		# 	appliedTo = des_entry.get()
		# 	category = cat_entry.get()

		# 	cr.auto_add_rule(rule_name, appliedTo, category)

		# 	cr.auto_apply_rules(account_name)

		# 	# Clear Tree View
		# 	self.my_tree.delete(*self.my_tree.get_children())
			
		# 	# query_database(account_name)
		# 	self.builder(account_name)

		# 	top.destroy()

		save_button = Button(top, text="Save", command=save)
		save_button.grid(row=6, column=0, columnspan=2, sticky=NSEW, padx=10, pady=10)
