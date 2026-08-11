from tkinter import *
import tkinter.ttk as ttk
import  tkinter.messagebox as msg
from connection import *

class Main:
    def __init__(self):
        self.root = Tk()
        self.root.state('zoomed')
        self.root.configure(bg="#D9CBA0")

        self.conn = getConnection()
        self.cr = self.conn.cursor()

        self.mainLabel = Label(self.root, text="View Admin", font=('Arial', 26, 'bold'),bg="#D9CBA0",fg='#4B3D2D')
        self.mainLabel.pack(pady=20)

        self.font = ('Arial', 16)

        self.searchFrame = Frame(self.root)

        self.lb0 = Label(self.searchFrame, text="Enter Text", font=self.font)
        self.txt0 = Entry(self.searchFrame, font=self.font, width=40)
        self.searchBtn = Button(self.searchFrame, text="Search", font=self.font,command=self.searchadmin,bg="#D9CBA0")
        self.resetBtn = Button(self.searchFrame, text="Reset", font=self.font,command=self.resetsearchform,bg="#D9CBA0")
        self.lb0.grid(row=0, column=0, padx=10, pady=10)
        self.txt0.grid(row=0, column=1, padx=10, pady=10)
        self.searchBtn.grid(row=0, column=2, padx=10, pady=10)
        self.resetBtn.grid(row=0, column=3, padx=10, pady=10)

        self.searchFrame.pack(pady=20)

        self.admintable=ttk.Treeview(self.root,show='headings',columns=['id','name','email','mobile','role'])
        self.admintable.pack(pady=20,expand=True,fill='both',padx=30)
        self.admintable.heading('id',text='ID')
        self.admintable.heading('name',text='Name')
        self.admintable.heading('email',text='Email')
        self.admintable.heading('mobile',text='Mobile')
        self.admintable.heading('role',text='Role')

        style = ttk.Style()
        style.configure('Treeview', font=self.font, rowheight=40)
        style.configure('Treeview.Heading', font=self.font,foreground='#4B3D2D')

        self.admintable.bind("<Double-1>", self.openupdatewindow)

        self.getValues()

        self.root.mainloop()

    def getValues(self):
        q = "select id, name, email, mobile, role from admin"
        self.cr.execute(q)
        result = self.cr.fetchall()
        for item in self.admintable.get_children():
            self.admintable.delete(item)
        index = 0
        for i in result:
            self.admintable.insert('', index=index, values=i)
            index += 1
    def searchadmin(self):
        text = self.txt0.get()
        q0 = f"select id, name, email, mobile, role from admin where name like '%{text}%' or email like '%{text}%' or mobile like '%{text}%'"
        self.cr.execute(q0)
        result=self.cr.fetchall()
        for item in self.admintable.get_children():
            self.admintable.delete(item)
        index = 0
        for i in result:
            self.admintable.insert('', index=index, values=i)
            index += 1

    def resetsearchform(self):
        self.txt0.delete(0, END)
        self.getValues()


    def openupdatewindow(self,event):
        id=self.admintable.selection()[0]
        metadata=self.admintable.item(id)
        data=metadata['values']
        print(data)
        self.root1 = Toplevel()
        self.root1.geometry('700x500')
        self.root1.configure(bg="#D9CBA0")
        self.mainLabel2 = Label(self.root1, text="Update/Delete Admin", font=('Arial', 24, 'bold'),bg="#D9CBA0",fg='#4B3D2D')

        self.mainLabel2.pack(pady=20)

        self.formFrame = Frame(self.root1,bg="#A67C4D",bd=5,relief=RIDGE)
        self.formFrame.pack(pady=20)
        self.font = ("Arial", 14)

        self.lb1 = Label(self.formFrame, text="Admin ID", font=self.font,fg='white',bg="#A67C4D")
        self.txt1 = Entry(self.formFrame, font=self.font)
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.txt1.grid(row=0, column=1, padx=10, pady=10)
        self.txt1.insert(0, data[0])
        self.txt1.config(state='readonly')

        self.lb2 = Label(self.formFrame, text="Enter Name", font=self.font,fg='white',bg="#A67C4D")
        self.txt2 = Entry(self.formFrame, font=self.font)
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2.grid(row=1, column=1, padx=10, pady=10)
        self.txt2.insert(0, data[1])

        self.lb3 = Label(self.formFrame, text="Enter Email", font=self.font,fg='white',bg="#A67C4D")
        self.txt3 = Entry(self.formFrame, font=self.font)
        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.txt3.grid(row=2, column=1, padx=10, pady=10)
        self.txt3.insert(0, data[2])

        self.lb4 = Label(self.formFrame, text="Enter Mobile", font=self.font,fg='white',bg="#A67C4D")
        self.txt4 = Entry(self.formFrame, font=self.font)
        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.txt4.grid(row=3, column=1, padx=10, pady=10)
        self.txt4.insert(0, data[3])

        self.lb5 = Label(self.formFrame, text="Select Role", font=self.font,fg='white',bg="#A67C4D")
        self.txt5 = ttk.Combobox(self.formFrame, font=self.font,state='readonly',values=['Super Admin', 'Admin'])
        self.lb5.grid(row=4, column=0, padx=10, pady=10)
        self.txt5.grid(row=4, column=1, padx=10, pady=10)
        self.txt5.set(data[4])

        self.updateBtn = Button(self.root1, text="Update", font=self.font,command=self.updateadmin,bg='#4B3D2D',fg='white')
        self.deleteBtn = Button(self.root1, text="Delete", font=self.font,command=self.deleteadmin,bg='#4B3D2D',fg='white')
        self.updateBtn.pack(pady=10)
        self.deleteBtn.pack(pady=10)

        self.root1.mainloop()
    def updateadmin(self):
        id=self.txt1.get()
        name=self.txt2.get()
        email=self.txt3.get()
        mobile=self.txt4.get()
        role=self.txt5.get()

        if name == "" or email == "" or mobile == "" or role == "":
            msg.showwarning("Warning", "Please fill all fields", parent=self.root1)
        else:
            if verifyMobile(mobile) == True and verifyEmail(email) == True:
                q1 = f"select * from admin where email='{email}' or mobile='{mobile}'"
                self.cr.execute(q1)
                result = self.cr.fetchall()
                print(result)
                if len(result)<=1:
                    q2 = f"update admin set name='{name}', email='{email}', mobile='{mobile}', role='{role}' where id={id}"
                    self.cr.execute(q2)
                    self.conn.commit()
                    self.root1.destroy()
                    msg.showinfo("Success", "Admin successfully updated")
                    self.getValues()
                else:
                    msg.showwarning('Error','Number/Email already exists')
            else:
                msg.showwarning("Warning", "Invalid Email or Mobile Number", parent=self.root1)

    def deleteadmin(self):
        id = self.txt1.get()
        q4 = f"delete from admin where id='{id}'"
        self.cr.execute(q4)
        self.conn.commit()
        self.root1.destroy()
        msg.showinfo("Success", "Admin successfully deleted")
        self.getValues()



#ob=Main()