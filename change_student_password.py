from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg

from connection import *


class login:
    def __init__(self,email):
        self.root=Toplevel()
        self.root.state("zoomed")
        self.root.configure(bg='#D9CBA0')

        self.mainLabel = Label(self.root, text="Change Student Password",
                               font=("Arial", 26, "bold"),bg='#D9CBA0',fg='#4B3D2D')
        self.mainLabel.pack(pady=20)

        self.formFrame = Frame(self.root,bd=8,relief=SOLID,bg='#A67C4D')
        self.formFrame.pack(pady=20)

        self.font = ("Arial", 20)

        self.lb1 = Label(self.formFrame, text="Email", font=self.font,fg='white',bg='#A67C4D')
        self.txt1 = Entry(self.formFrame, font=self.font)
        self.lb1.grid(row=1, column=0, padx=10, pady=10)
        self.txt1.grid(row=1, column=1, padx=10, pady=10)
        self.txt1.insert(0,email)
        self.txt1.configure(state='readonly')

        self.lb2 = Label(self.formFrame, text="Enter Old Password", font=self.font,fg='white',bg='#A67C4D')
        self.txt2 = Entry(self.formFrame, font=self.font,show="*")
        self.lb2.grid(row=3, column=0, padx=10, pady=10)
        self.txt2.grid(row=3, column=1, padx=10, pady=10)

        self.lb3 = Label(self.formFrame, text="Enter New Password", font=self.font,fg='white',bg='#A67C4D')
        self.txt3 = Entry(self.formFrame, font=self.font,show="*")
        self.lb3.grid(row=4, column=0, padx=10, pady=10)
        self.txt3.grid(row=4, column=1, padx=10, pady=10)

        self.btn = Button(self.root, text="Submit", font=('Arial', 16), command=self.change_password,bg='#4B3D2D',fg='white')
        self.btn.pack()

        self.root.mainloop()
    def change_password(self):
        email=self.txt1.get()
        old_pass=self.txt2.get()
        new_pass=self.txt3.get()

        conn=getConnection()
        cr=conn.cursor()

        if old_pass=='':
            msg.showerror('error','Please enter old password')
        else:
            q1 = f"select * from students where email='{email}' and password='{old_pass}'"

            cr.execute(q1)
            result =cr.fetchall()
            print(result)
            if len(result)==1:
                id = result[0][0]
                q2=f"update students set password='{new_pass}' where id='{id}'"
                if new_pass=='':
                    msg.showerror('error','Please enter new password')
                else:
                    cr.execute(q2)
                    msg.showinfo('success','Password changed')
                    conn.commit()
                    conn.close()
                    self.root.destroy()
            else:
                msg.showwarning('warning','Wrong old password')



#ob=login()