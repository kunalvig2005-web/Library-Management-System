from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import *
import student_dashboard
from PIL import Image,ImageTk

class login:
    def __init__(self):
        self.root=Tk()
        self.root.state("zoomed")
        self.root.configure(bg="#D9CBA0")

        self.lb=Label(self.root,text="Student Login",bg="#D9CBA0",font=('Helvetica',24,'bold'),fg='#4B3D2D')
        self.lb.pack(pady=20)

        self.frame=Frame(self.root,bd=10,relief=SOLID,bg="#A67C4D")
        self.frame.pack(pady=20)

        self.lb1=Label(self.frame,text="Email",bg="#A67C4D",font=('Arial',20),fg='white')
        self.txt1=Entry(self.frame,font=('Arial',20))

        self.lb2=Label(self.frame,text="Password",bg="#A67C4D",font=('Arial',20),fg='white')
        self.txt2=Entry(self.frame,font=('Arial',20),show="*")


        self.lb1.grid(row=0,column=0,padx=10,pady=10)
        self.txt1.grid(row=0, column=1, padx=10, pady=10)

        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2.grid(row=1, column=1, padx=10, pady=10)

        self.btn1=Button(self.root,text="Login",bg="#4B3D2D",font=('Arial',18),command=self.check_login,fg='white')
        self.btn1.pack(pady=10)
        self.btn2 = Button(self.root, text="Forget Password",bg="#4B3D2D", font=('Arial',18),fg='white')
        self.btn2.pack(pady=10)

        self.image = Image.open("lib1.jpg")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.img = self.image.resize((self.width, self.height))
        bg = ImageTk.PhotoImage(self.img)

        c = Canvas(self.root, width=self.width, height=self.height, highlightbackground="black", highlightthickness=2)
        c.pack(fill='both', expand=True)
        c.create_image(0, 0, image=bg, anchor=NW)

        c.create_text(680, 40, font=('Helvetica', 50, 'bold'))

        self.root.mainloop()

    def check_login(self):
        email=self.txt1.get()
        password=self.txt2.get()
        conn=getConnection()
        cr=conn.cursor()
        q=f"select * from students where email='{email}' and password='{password}'"
        cr.execute(q)
        result=cr.fetchall()
        print(result)
        if email=='' or password=='':
            msg.showerror('error','Please enter full details')
        elif len(result)==1:
            msg.showinfo('Success','Login successful')
            self.reset_login()

            student_dashboard.student(result)

            conn.commit()
            conn.close()
        else:
            msg.showwarning('warning','wrong Credentials')
    def reset_login(self):
        self.txt1.delete(0, END)
        self.txt2.delete(0, END)


ob=login()