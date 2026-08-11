from tkinter import *
import tkinter.ttk as ttk
from connection import getConnection

class view_return_books:
    def __init__(self):
        self.root=Tk()
        self.root.state('zoomed')
        self.root.title('View Return Books')
        self.conn=getConnection()
        self.cr=self.conn.cursor()
        self.root.configure(bg = "#D9CBA0")

        self.lb=Label(self.root,text="View Return Books",font=('Helvetica',28,'bold'),bg="#D9CBA0",fg='#4B3D2D')
        self.lb.pack(pady=20)

        self.table = ttk.Treeview(self.root, show='headings',columns=['b_name','s_name','s_email','status','lib_name','return_date'])

        self.table.pack(pady=20, expand=True, fill='both')
        self.table.heading('b_name', text='Book Name',anchor='center')
        self.table.heading('s_name',text='Student Name')
        self.table.heading('s_email', text='Student Email')
        self.table.heading('status', text='Status')
        self.table.heading('lib_name', text='Library Name')
        self.table.heading('return_date', text='Return Date')

        self.table.column('b_name', anchor='center')
        self.table.column('s_name', anchor='center')
        self.table.column('s_email', anchor='center')
        self.table.column('status', anchor='center')
        self.table.column('lib_name', anchor='center')
        self.table.column('return_date', anchor='center')

        self.style=ttk.Style()
        self.style.configure("Treeview",font=('Arial',16),rowheight=40)
        self.style.configure('Treeview.Heading',font=('Arial',16),foreground='#4B3D2D')
        self.get_values()

        self.root.mainloop()

    def get_values(self):
        q=f"select * from issue"
        self.cr.execute(q)
        result=self.cr.fetchall()
        for item in self.table.get_children():
            self.table.delete(item)
        for i in result:
            if i[4]=='returned':
                q1=f"select * from books where id={i[6]}"
                self.cr.execute(q1)
                res1=self.cr.fetchall()
                q2=f"select * from students where id={i[8]}"
                self.cr.execute(q2)
                res2=self.cr.fetchall()
                q3=f"select * from admin where id={i[7]}"
                self.cr.execute(q3)
                res3=self.cr.fetchall()

                self.table.insert("", "end", values=(res1[0][1],res2[0][1],res2[0][2],"Returned",res3[0][1],i[3]))


ob=view_return_books()