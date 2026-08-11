from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import getConnection, verifyEmail, verifyMobile

class students:
    def __init__(self):
        self.root=Tk()
        self.root.state('zoomed')
        self.root.configure(bg="#D9CBA0")

        self.lb=Label(self.root,text="ADD STUDENTS",font=('Helvetica',30,'bold'),fg='#4B3D2D',bg="#D9CBA0")
        self.lb.pack(pady=20)

        self.frame=Frame(self.root,bd=10,relief=GROOVE,bg='#A67C4D')
        self.frame.pack(pady=20)

        self.lb1=Label(self.frame,text="Enter Name",font=('Arial',20),bg="#A67C4D",fg='white')
        self.txt1=Entry(self.frame,font=('Arial',20))
        self.lb2=Label(self.frame,text="Enter Email",font=('Arial',20),bg="#A67C4D",fg='white')
        self.txt2=Entry(self.frame,font=('Arial',20))
        self.lb3=Label(self.frame,text="Enter Mobile Number",font=('Arial',20),bg="#A67C4D",fg='white')
        self.txt3=Entry(self.frame,font=('Arial',20))
        self.lb4=Label(self.frame,text="Enter Address",font=('Arial',20),bg="#A67C4D",fg='white')
        self.txt4=Entry(self.frame,font=('Arial',20))

        self.lb5=Label(self.frame,text="Select Gender",font=('Arial',20),bg="#A67C4D",fg='white')
        self.cb1=ttk.Combobox(self.frame,state='readonly',values=['Male','Female'],font=('Arial',20))

        self.lb6=Label(self.frame,text="Enter Password",font=('Arial',20),bg="#A67C4D",fg='white')
        self.txt5=Entry(self.frame,font=('Arial',20),show='*')


        self.lb1.grid(row=0,column=0,padx=10,pady=10)
        self.txt1.grid(row=0, column=1, padx=10, pady=10)

        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2.grid(row=1, column=1, padx=10, pady=10)

        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.txt3.grid(row=2, column=1, padx=10, pady=10)

        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.txt4.grid(row=3, column=1, padx=10, pady=10)

        self.lb5.grid(row=4, column=0, padx=10, pady=10)
        self.cb1.grid(row=4, column=1, padx=10, pady=10)

        self.lb6.grid(row=5, column=0, padx=10, pady=10)
        self.txt5.grid(row=5, column=1, padx=10, pady=10)

        self.btn=Button(self.root,text="SUBMIT",font=("Arial",20),command=self.add_students,bg='#4B3D2D',fg='white')
        self.btn.pack(pady=20)

        self.root.mainloop()

    def add_students(self):
        name=self.txt1.get()
        email=self.txt2.get()
        mobile=self.txt3.get()
        address=self.txt4.get()
        gender=self.cb1.get()
        password=self.txt5.get()

        if name=='' or email=='' or mobile=='' or address=='' or gender=='':
            msg.showerror('error','Please fill all details')
        elif verifyMobile(mobile)==True and verifyEmail(email)==True:
            conn=getConnection()
            cr=conn.cursor()
            q=f"select * from students where mobile='{mobile}' or email='{email}'"
            cr.execute(q)
            result=cr.fetchall()
            if len(result)==0:
                q1=f"insert into students values(null,'{name}','{email}','{mobile}','{address}','{gender}','{password}')"
                cr.execute(q1)
                msg.showinfo('success','Details added successfully')
                conn.commit()
                conn.close()
                self.reset()

            else:
                msg.showerror('error','mobile/email already added')
        else:
            msg.showerror('error','Invalid mobile/email')

    def reset(self):
        self.txt1.delete(0, END)
        self.txt2.delete(0, END)
        self.txt3.delete(0, END)
        self.txt4.delete(0, END)
        self.txt5.delete(0,END)
        self.cb1.set('')


#ob=students()