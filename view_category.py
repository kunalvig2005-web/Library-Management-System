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

        self.mainLabel = Label(self.root, text="View Category", font=('Arial', 26, 'bold'),bg="#D9CBA0")
        self.mainLabel.pack(pady=20)

        self.font = ('Arial', 18)

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
        style = ttk.Style()
        style.configure('Treeview', font=self.font, rowheight=40)
        style.configure('Treeview.Heading', font=self.font,foreground='#4B3D2D')

        self.getValues()

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

#ob=category_view()