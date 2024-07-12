
import tkinter
from tkinter import *
import csv
import tkinter.ttk
import matplotlib.pyplot as plt
from PIL import ImageTk, Image


class ExpTrack(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personal Expenses Tracker")
        self.geometry("1500x1000")
        self.expenses = []
        self.types = [
            "Food", 
            "Transportation", 
            "Tuition", "Clothes", 
            "Entertainment", "Others"
        ]
        self.type_var = tkinter.StringVar(self)
        self.type_var.set(self.types[0])
        self.create_widgets()
        self.images()

    def create_widgets(self):
        self.label = tkinter.Label(
            self, text="Personal Expense Tracker", font=("Giddyup Std", 22, "bold")
        )

        # Label and Combobox Definition
        self.label.pack(pady=10)
        self.frame_input = Frame(self)
        self.frame_input.pack(pady=10)
        self.expense_label = Label(
            self.frame_input, text="Expense Amount ($):", font=("Times New Roman", 12)
        )
        self.expense_label.grid(row=0, column=0, padx=10)
        self.expense_entry = Entry(
            self.frame_input, font=("Times New Roman", 12), width=15
        )
        self.expense_entry.grid(row=0, column=1, padx=10)
        self.item_label = Label(
            self.frame_input, text="Item Description:", font=("Times New Roman", 12)
        )
        self.item_label.grid(row=0, column=2, padx=10)
        self.item_entry = Entry(self.frame_input, font=("Times New Roman", 12), width=20)
        self.item_entry.grid(row=0, column=3, padx=10)
        self.category_label = Label(
            self.frame_input, text="Type of Expense:", font=("Times New Roman", 12)
        )
        self.category_label.grid(row=0, column=4, padx=10)
        self.category_dropdown = tkinter.ttk.Combobox(
            self.frame_input,
            textvariable=self.type_var,
            values=self.types,
            font=("Times New Roman", 12),
            width=15,
        )
        self.category_dropdown.grid(row=0, column=5, padx=5)
        self.date_label = Label(
            self.frame_input, text="Date (MM-DD):", font=("Times New Roman", 12)
        )
        self.date_label.grid(row=0, column=6, padx=5)
        self.date_entry = Entry(self.frame_input, font=("Times New Roman", 12), width=15)
        self.date_entry.grid(row=0, column=7, padx=5)
    
    # Button Definitions

        # Enter a completed expense
        self.add_exp = Button(self, 
                                      text ="Add Expense", 
                                      command = self.add_action)
        self.add_exp.pack(pady=5)
        self.frame_list = Frame(self)
        self.frame_list.pack(pady=10)
        self.scrollbar = Scrollbar(self.frame_list)
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
       
       # Main box storing the input data
        self.listbox = Listbox(self.frame_list,
                                       font = ("Times New Roman", 12),
                                       width = 100, 
                                       yscrollcommand=self.scrollbar.set)
        self.listbox.pack(pady=5)
        self.scrollbar.config(command=self.listbox.yview)

        self.edit_exp = Button(self, text="Edit Expense", command=self.edit_action)
        self.edit_exp.pack(pady=5)


        self.delete_exp = Button(self, text="Delete Expense", command=self.delete_action)
        self.delete_exp.pack(pady=5)


        self.save_exp = Button(self, text="Save Expenses", command=self.save_action)
        self.save_exp.pack(pady=5)

        self.total_label = Label(self, text="Total Expenses:", font=("Giddyup Std", 25, "bold")
        )
        self.total_label.pack(pady=5)


        self.chart_button = Button(
            self, text="Show Expenses Chart", command=self.show_expenses_chart
        )
        self.chart_button.pack(pady=5)
        self.update_total_label()


    def add_action(self):
        expense = self.expense_entry.get()
        item = self.item_entry.get()
        types = self.type_var.get()
        date = self.date_entry.get()

        if expense and date and types:
            self.expenses.append((expense, item, types, date))
            self.listbox.insert(tkinter.END,
                                f"{expense} - {item} - {types} - {date}")
            
            self.expense_entry.delete(0, tkinter.END)
            self.item_entry.delete(0, tkinter.END)
            self.date_entry.delete(0, tkinter.END)

        else:
            tkinter.messagebox.warning("Empty Fields Entered.")

        self.update_total_label()     


    def delete_action(self):
        expense_to_delete = self.listbox.curselection()
        if expense_to_delete:
            expense_to_delete = expense_to_delete[0]
            del self.expenses[expense_to_delete]     
            self.listbox.delete(expense_to_delete)  
            self.update_total_label() 


    def edit_action(self):
        expense_to_edit = self.listbox.curselection()
        if expense_to_edit:
            expense_to_edit = expense_to_edit[0]
            expense = self.expenses[expense_to_edit]
            new_expense = tkinter.simpledialog.askstring(
                "Edit", "Enter new expense:", initialvalue=expense_to_edit[0]
            )
            if new_expense:
                self.expenses[expense_to_edit] = (new_expense,expense_to_edit[1],expense_to_edit[2],expense_to_edit[3] )
                self.refresh_list()
                self.update_total_label()


    def refresh_list(self):
        self.expense_listbox.delete(0, tkinter.END)
        for expense, item, category, date in self.expenses:
            self.listbox.insert(
                tkinter.END, f"{expense} - {item} - {category} ({date})"
            )


    
    def update_total_label(self):
        total_expenses = sum(float(expense[0]) for expense in self.expenses)
        self.total_label.config(text=f"Total Expenses: {total_expenses:.2f} $CAD")

    def save_action(self):
        with open("expenses.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            column_headers = ["Expense Amount", "Item Description", "Type", "Date"]
            writer.writerow(column_headers)
            for expense in self.expenses:
                writer.writerow(expense)


    def show_expenses_chart(self):
        totals_per_type = {}
        for expense, _, types, _ in self.expenses:
            try:
                amount = float(expense)
            except ValueError:
                continue
            totals_per_type[types] = totals_per_type.get(types, 0) + amount

        types_ofexpense = list(totals_per_type.keys())
        expenses = list(totals_per_type.values())
        plt.figure(figsize=(8, 8))
        plt.pie(
            expenses, labels=types_ofexpense, autopct="%1.1f%%", startangle=120, shadow=False
        )
        plt.axis("equal")
        plt.title("Expenses Distribution (CAD)")
        plt.show()

    def images(self):
        self.image1 = ImageTk.PhotoImage(
            Image.open("/Users/ameebhavsar/vscodeprojects/ExpenseTracker/images/emoticon_one.jpeg").resize((306,180), Image.Resampling.LANCZOS))
        img_label = Label(self, image=self.image1)
        img_label.pack(side="top", padx=10, pady = 50)

if __name__ == "__main__":
    app = ExpTrack()
    app.mainloop()




