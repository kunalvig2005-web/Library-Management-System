from tkinter import *
import tkinter.ttk as ttk
import  tkinter.messagebox as msg
from connection import *

class Main:
    def __init__(self):
        self.root = Tk()
        self.root.state('zoomed')

        self.conn = getConnection()
        self.cr = self.conn.cursor()
        self.root.configure(bg="#D9CBA0")

        self.mainLabel = Label(self.root, text="View Books", font=('Arial', 26, 'bold'),bg="#D9CBA0",fg='#4B3D2D')
        self.mainLabel.pack(pady=20)

        self.font = ('Arial', 18)

        self.searchFrame = Frame(self.root)

        self.lb0 = Label(self.searchFrame, text="Enter Text", font=self.font)
        self.txt0 = Entry(self.searchFrame, font=self.font, width=40)
        self.searchBtn = Button(self.searchFrame, text="Search", font=self.font,command=self.searchadmin,bg="#D9CBA0")
        self.resetBtn = Button(self.searchFrame, text="Reset", font=self.font,command=self.resetsearchform,bg="#D9CBA0")
        self.lb0.grid(row=0, column=0, padx=10, pady=10)
        self.txt0.grid(row=0, column=1, padx=10, pady=10)
        self.searchBtn.grid(row=0, column=2, padx=10, pady=10)
        self.resetBtn.grid(row=0, column=3, padx=10, pady=10)

        self.searchFrame.pack(pady=10)

        self.book_table=ttk.Treeview(self.root,show='headings',columns=['id','name','des','status','auth_name','t_cpy','isbn','cat','lib_id'])
        self.book_table.pack(pady=20,expand=True,fill='both')
        self.book_table.heading('id',text='ID')
        self.book_table.heading('name',text='Name')
        self.book_table.heading('des',text='Description')
        self.book_table.heading('status',text='Status')
        self.book_table.heading('auth_name',text='Author Name')
        self.book_table.heading('t_cpy', text='Total Copies')
        self.book_table.heading('isbn', text='ISBN')
        self.book_table.heading('cat', text='Category')
        self.book_table.heading('lib_id', text='Library ID')

        self.book_table.column('id', width=8, anchor='center')
        self.book_table.column('name', width=10, anchor='center')
        self.book_table.column('des', width=10, anchor='center')
        self.book_table.column('status', width=10, anchor='center')
        self.book_table.column('auth_name', width=10, anchor='center')
        self.book_table.column('t_cpy', width=10, anchor='center')
        self.book_table.column('isbn', width=10, anchor='center')
        self.book_table.column('cat', width=10, anchor='center')
        self.book_table.column('lib_id', width=10, anchor='center')

        style = ttk.Style()
        style.configure('Treeview', font=self.font, rowheight=40)
        style.configure('Treeview.Heading', font=self.font,foreground='#4B3D2D')

        self.getValues()

        self.root.mainloop()

    def getValues(self):
        q = "select * from books"
        self.cr.execute(q)
        result = self.cr.fetchall()
        for item in self.book_table.get_children():
            self.book_table.delete(item)
        index = 0
        for i in result:
            self.book_table.insert('', index=index, values=i)
            index += 1
    def searchadmin(self):
        text = self.txt0.get()
        q0 = f"select * from admin where name like '%{text}%' or description like '%{text}%' or status like '%{text}%' or author_name like '%{text}%' or total_copies like %{text}% or isbn like '%{text}%' or category like '%{text}%'"
        self.cr.execute(q0)
        result=self.cr.fetchall()
        for item in self.book_table.get_children():
            self.book_table.delete(item)
        index = 0
        for i in result:
            self.book_table.insert('', index=index, values=i)
            index += 1

    def resetsearchform(self):
        self.txt0.delete(0, END)
        self.getValues()
#ob=Main()