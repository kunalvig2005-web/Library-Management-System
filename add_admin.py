from tkinter import *
import tkinter.messagebox as msg
import tkinter.ttk as ttk
from connection import getConnection, verifyEmail, verifyMobile

class Main:
    def __init__(self):
        self.root = Tk()
        self.root.state('zoomed')
        self.root.title("Add Admin")
        self.pc="#D9CBA0"
        self.root.configure(bg=self.pc)
        self.sc="#A67C4D"

        self.tc='white'

        self.conn = getConnection()
        self.cr = self.conn.cursor()

        self.mainLabel = Label(self.root, text="Add Library Admin",bg=self.pc,
                               font=("Arial", 28, "bold"),fg="#4B3D2D")
        self.mainLabel.pack(pady=20)

        self.formFrame = Frame(self.root,bd=10,relief=RIDGE,bg=self.sc)
        self.formFrame.pack(pady=20)

        self.font = ("Arial", 20)

        self.lb1 = Label(self.formFrame, text="Enter Name", font=self.font,bg=self.sc,fg=self.tc)
        self.txt1 = Entry(self.formFrame, font=self.font)
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.txt1.grid(row=0, column=1, padx=10, pady=10)

        self.lb2 = Label(self.formFrame, text="Enter Email", font=self.font,bg=self.sc,fg=self.tc)
        self.txt2 = Entry(self.formFrame, font=self.font)
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2.grid(row=1, column=1, padx=10, pady=10)

        self.lb3 = Label(self.formFrame, text="Enter Mobile", font=self.font,bg=self.sc,fg=self.tc)
        self.txt3 = Entry(self.formFrame, font=self.font)
        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.txt3.grid(row=2, column=1, padx=10, pady=10)

        self.lb4 = Label(self.formFrame, text="Enter Password", font=self.font,bg=self.sc,fg=self.tc)
        self.txt4 = Entry(self.formFrame, font=self.font, show='*')
        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.txt4.grid(row=3, column=1, padx=10, pady=10)

        self.lb5 = Label(self.formFrame, text="Select Role", font=self.font,bg=self.sc,fg=self.tc)
        self.txt5 = ttk.Combobox(self.formFrame, font=self.font, values=['Super Admin', 'Admin'], state='readonly')
        self.lb5.grid(row=4, column=0, padx=10, pady=10)
        self.txt5.grid(row=4, column=1, padx=10, pady=10)

        self.btn = Button(self.root, text="Submit", font=self.font, command=self.insertAdmin,bg="#4B3D2D",fg=self.tc)
        self.btn.pack(pady=20)

        self.root.mainloop()

    def insertAdmin(self):
        name = self.txt1.get()
        email = self.txt2.get()
        mobile = self.txt3.get()
        password = self.txt4.get()
        role = self.txt5.get()

        if name=="" or email=="" or mobile=="" or password=="" or role=="":
            msg.showinfo('Error', 'please enter full details')

        elif verifyMobile(mobile) == True and verifyEmail(email) == True:
            q1 = f"select * from admin where email='{email}' or mobile='{mobile}'"
            self.cr.execute(q1)
            result = self.cr.fetchall()
            print(result)
            if len(result) == 0:
                q = f"insert into admin values(null,'{name}', '{email}', '{mobile}', '{password}', '{role}')"
                self.cr.execute(q)
                self.conn.commit()
                msg.showinfo("Success", "Admin successfully added")
                self.resetForm()
            else:
                msg.showwarning("Warning", "Email / Mobile already exists")
        else:
            msg.showwarning('Warning', 'Invalid Email / Mobile Number')



    def resetForm(self):
        self.txt1.delete(0, END)
        self.txt2.delete(0, END)
        self.txt3.delete(0, END)
        self.txt4.delete(0, END)
        self.txt5.set('')


#obj = Main()