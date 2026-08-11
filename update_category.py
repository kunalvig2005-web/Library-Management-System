from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import getConnection

class category_view:
    def __init__(self):
        self.root=Tk()
        self.root.state('zoomed')

        self.conn=getConnection()
        self.cr=self.conn.cursor()
        self.root.configure(bg="#D9CBA0")

        self.mainLabel = Label(self.root, text="View Category", font=('Arial', 26, 'bold'),bg="#D9CBA0",fg='#4B3D2D')
        self.mainLabel.pack(pady=20)

        self.font = ('Arial', 20)

        self.searchFrame = Frame(self.root)
        self.searchFrame.pack(pady=20)

        self.lb0 = Label(self.searchFrame, text="Enter Text", font=('Arial',20,'bold'))
        self.txt0 = Entry(self.searchFrame, font=self.font, width=40)
        self.searchBtn = Button(self.searchFrame, text="Search", font=self.font,command=self.search_category,bg="#D9CBA0")
        self.resetBtn = Button(self.searchFrame, text="Reset", font=self.font,command=self.resetsearchform,bg="#D9CBA0")
        self.lb0.grid(row=0, column=0, padx=10, pady=10)
        self.txt0.grid(row=0, column=1, padx=10, pady=10)
        self.searchBtn.grid(row=0, column=2, padx=10, pady=10)
        self.resetBtn.grid(row=0, column=3, padx=10, pady=10)

        self.category_table = ttk.Treeview(self.root, show='headings', columns=['book_category','des'])
        self.category_table.pack(pady=20, expand=True, fill='both', padx=30)
        self.category_table.heading('book_category', text='Category')
        self.category_table.heading('des', text='Description')
        self.category_table.column('book_category', anchor='center')
        self.category_table.column('des', anchor='center')
        style = ttk.Style()
        style.configure('Treeview', font=self.font, rowheight=40)
        style.configure('Treeview.Heading', font=self.font,foreground='#4B3D2D')



        self.getValues()
        self.category_table.bind("<Double-1>", self.openupdatewindow)

        self.root.mainloop()

    def getValues(self):
        q = "select Category, description from category"
        self.cr.execute(q)
        result = self.cr.fetchall()
        print(result)
        for item in self.category_table.get_children():
            self.category_table.delete(item)
        index = 0
        for i in result:
            self.category_table.insert('', index=index, values=i)
            index += 1

    def search_category(self):
        text = self.txt0.get()
        q0 = f"select Category, description from category where Category like '%{text}%' or description like '%{text}%'"
        self.cr.execute(q0)
        result=self.cr.fetchall()
        for item in self.category_table.get_children():
            self.category_table.delete(item)
        index = 0
        for i in result:
            self.category_table.insert('', index=index, values=i)
            index += 1
    def resetsearchform(self):
        self.txt0.delete(0, END)
        self.getValues()

    def openupdatewindow(self,event):
        id=self.category_table.selection()[0]
        metadata=self.category_table.item(id)
        data=metadata['values']
        print(data)
        self.old_category = data[0]
        self.root1 = Toplevel()
        self.root1.geometry('500x400')
        self.root1.configure(bg="#D9CBA0")
        self.mainLabel2 = Label(self.root1, text="Update/Delete Category", font=('Arial', 24, 'bold'),fg='#4B3D2D',bg="#D9CBA0")

        self.mainLabel2.pack(pady=20)

        self.formFrame = Frame(self.root1,bg="#A67C4D",bd=5,relief=RIDGE)
        self.formFrame.pack(pady=20)
        self.font = ("Arial", 14)

        self.lb1 = Label(self.formFrame, text="Category", font=self.font,fg='white',bg="#A67C4D")
        self.txt1 = Entry(self.formFrame, font=self.font)
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.txt1.grid(row=0, column=1, padx=10, pady=10)
        self.txt1.insert(0, data[0])

        self.lb2 = Label(self.formFrame, text="Description", font=self.font,fg='white',bg="#A67C4D")
        self.txt2 = Entry(self.formFrame, font=self.font)
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2.grid(row=1, column=1, padx=10, pady=10)
        self.txt2.insert(0, data[1])



        self.updateBtn = Button(self.root1, text="Update", font=self.font,command=self.updatecategory,bg='#4B3D2D',fg='white')
        self.deleteBtn = Button(self.root1, text="Delete", font=self.font,command=self.deletecategory,bg='#4B3D2D',fg='white')
        self.updateBtn.pack(pady=10)
        self.deleteBtn.pack(pady=10)

        self.root1.mainloop()

    def updatecategory(self):
        category = self.txt1.get().strip()
        des = self.txt2.get().strip()

        if category == "" or des == "":
            msg.showwarning("Warning", "Please fill all fields", parent=self.root1)
            return

        # Check if this category is used in books
        q_check_books = f"SELECT COUNT(*) FROM books WHERE category='{self.old_category}'"
        self.cr.execute(q_check_books)
        count = self.cr.fetchone()[0]

        # Prevent renaming if used in books
        if count > 0 and category != self.old_category:
            msg.showwarning("Error", "This category is assigned to books. You cannot rename it while it's in use.",
                            parent=self.root1)
            return

        # If name is changing, check if new category name already exists
        if category != self.old_category:
            q_check_duplicate = f"SELECT * FROM category WHERE Category='{category}'"
            self.cr.execute(q_check_duplicate)
            if self.cr.fetchone():
                msg.showwarning("Error", "This category name already exists.", parent=self.root1)
                return

        # Perform the update
        q_update = f"UPDATE category SET Category='{category}', description='{des}' WHERE Category='{self.old_category}'"
        self.cr.execute(q_update)
        self.conn.commit()

        self.root1.destroy()
        msg.showinfo("Success", "Category successfully updated")
        self.getValues()

    def deletecategory(self):
        q4 = f"delete from category where Category='{self.old_category}'"
        self.cr.execute(q4)
        self.conn.commit()
        self.root1.destroy()
        msg.showinfo("Success", "Category successfully deleted")
        self.getValues()


#ob=category_view()