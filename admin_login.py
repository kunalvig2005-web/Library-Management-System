from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import *
import admin_dashboard
from PIL import Image,ImageTk
import smtplib
from email.message import EmailMessage
import random

class login:
    def __init__(self):
        self.root=Tk()
        self.root.state("zoomed")
        self.root.configure(bg="#D9CBA0")

        self.lb=Label(self.root,text="LIBRARY ADMIN LOGIN",bg="#D9CBA0",fg='#4B3D2D',font=('Helvetica',24,'bold'))
        self.lb.pack(pady=20)

        self.frame=Frame(self.root,bd=6,relief=SOLID,bg="#A67C4D")
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
        self.btn2 = Button(self.root, text="Forget Password",bg="#4B3D2D", font=('Arial',18),command=self.forgot_password,fg='white')
        self.btn2.pack(pady=10)

        self.image = Image.open("lib1.jpg")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.img = self.image.resize((self.width, self.height))
        bg = ImageTk.PhotoImage(self.img)

        c = Canvas(self.root, width=self.width, height=self.height, highlightbackground="black", highlightthickness=2)
        c.pack(fill='both', expand=True)
        c.create_image(0, 0, image=bg, anchor=NW)

        c.create_text(680,40,font=('Helvetica',50,'bold'))

        self.root.mainloop()

    def check_login(self):
        email=self.txt1.get()
        password=self.txt2.get()
        conn=getConnection()
        cr=conn.cursor()
        q=f"select * from admin where email='{email}' and password='{password}'"
        cr.execute(q)
        result=cr.fetchall()
        print(result)
        if email=='' or password=='':
            msg.showerror('error','Please enter full details')
        elif len(result)==1:
            msg.showinfo('Success','Login successful')
            self.reset_login()

            admin_dashboard.main_menu(result)

            conn.commit()
            conn.close()
        else:
            msg.showwarning('warning','wrong Credentials')
    def reset_login(self):
        self.txt1.delete(0, END)
        self.txt2.delete(0, END)

    def forgot_password(self):
        win = Toplevel()
        win.title("Reset Password")
        win.geometry("400x350")
        win.configure(bg="#D9CBA0")

        Label(win, text="Enter your registered Email:", bg="#D9CBA0", font=("Arial", 12)).pack(pady=10)
        email_entry = Entry(win, font=("Arial", 14),fg='white')
        email_entry.pack(pady=10)

        Label(win, text="Enter OTP (sent on email):", bg="#D9CBA0", font=("Arial", 12)).pack(pady=10)
        otp_entry = Entry(win, font=("Arial", 14),fg='white')
        otp_entry.pack(pady=10)

        Label(win, text="Enter New Password:", bg="#D9CBA0", font=("Arial", 12)).pack(pady=10)
        new_pass_entry = Entry(win, font=("Arial", 14), show="*",fg='white')
        new_pass_entry.pack(pady=10)

        def send_otp():
            email = email_entry.get()
            conn = getConnection()
            cr = conn.cursor()
            cr.execute(f"SELECT * FROM admin WHERE email='{email}'")
            result = cr.fetchone()
            if result:
                self.generated_otp = str(random.randint(100000, 999999))
                try:
                    msg1 = EmailMessage()
                    msg1['Subject'] = "Password Reset OTP"
                    msg1['From'] = "vmm.testing.email2@gmail.com"
                    msg1['To'] = email
                    msg1.set_content(f"Your OTP for password reset is: {self.generated_otp}")

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login("vmm.testing.email2@gmail.com", "tirllvbbhctznive")  # Use App Password here
                    server.send_message(msg1)
                    server.quit()

                    msg.showinfo("Success", "OTP sent to your email")
                except Exception as e:
                    msg.showerror("Error", f"Error sending email: {str(e)}")
            else:
                msg.showerror("Error", "Email not found")

        def reset_pass():
            conn=getConnection()
            cr=conn.cursor()
            if otp_entry.get() == self.generated_otp:
                new_pass = new_pass_entry.get()
                cr.execute(f"UPDATE admin SET password='{new_pass}' WHERE email='{email_entry.get()}'")
                conn.commit()
                conn.close()
                msg.showinfo("Success", "Password updated successfully")
                win.destroy()
            else:
                msg.showerror("Error", "Incorrect OTP")


        Button(win, text="Send OTP", font=("Arial", 12), command=send_otp, bg="#4B3D2D",fg='white').pack(pady=5)
        Button(win, text="Reset Password", font=("Arial", 12), command=reset_pass, bg="#4B3D2D",fg='white').pack(pady=10)


ob=login()