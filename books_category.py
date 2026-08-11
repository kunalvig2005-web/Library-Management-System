from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import getConnection

class category:
    def __init__(self):
        self.window=Tk()
        self.window.title("Add Category")
        self.window.geometry("600x500")
        self.window.configure(bg="#D9CBA0")

        self.lb0=Label(self.window,text="ADD CATEGORY",bg='#D9CBA0',fg='#4B3D2D',font=('Helvetica',24,'bold'))
        self.lb0.pack(pady=20)

        self.mainframe=Frame(self.window,bd=8,relief=GROOVE,bg="#A67C4D")
        self.mainframe.pack(pady=20)

        self.lb1=Label(self.mainframe,text="Book Category",font=('Arial',20),bg="#A67C4D",fg='white')
        self.txt1=Entry(self.mainframe,font=('Arial',20))

        self.lb2=Label(self.mainframe,text="Book Description",font=('Arial',20),bg="#A67C4D",fg='white')
        self.cb1=Entry(self.mainframe,font=('Arial',20))

        self.lb1.grid(row=0,column=0,padx=10,pady=10)
        self.txt1.grid(row=0,column=1,padx=10,pady=10)

        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.cb1.grid(row=1, column=1, padx=10, pady=10)

        self.btn=Button(self.window,text='ADD',font=('Helvetica',20),command=self.add_category,bg="#4B3D2D",fg='white')
        self.btn.pack()



        self.window.mainloop()

    def add_category(self):
        category=self.txt1.get()
        description=self.cb1.get()

        conn=getConnection()
        cr=conn.cursor()

        q0=f"select * from category where Category='{category}'"
        cr.execute(q0)
        res=cr.fetchall()

        if description=="" or category=="":
            msg.showerror('Error','Please enter full details')
        else:
            if len(res)==0:
                q=f"insert into category values('{category}','{description}')"
                cr.execute(q)
                conn.commit()
                conn.close()
                msg.showinfo('Success','Category Successfully added')
                self.reset()
            else:
                msg.showerror('error','Duplicate Category Entry')

    def reset(self):
        self.txt1.delete(0, END)
        self.cb1.delete(0, END)

#ob=category()