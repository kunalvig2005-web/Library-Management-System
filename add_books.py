#id,name,des,status,aut name, total copies,category,lib_id,isbn
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import getConnection

class add_books:
    def __init__(self):
        self.root=Tk()
        self.root.state('zoomed')
        self.conn = getConnection()
        self.cr =self.conn.cursor()

        self.pc="#D9CBA0"
        self.sc="#A67C4D"
        self.tc='white'
        self.root.configure(bg=self.pc)

        self.lb=Label(self.root,text="Add Books",font=('Helvetiva',32,'bold'),bg=self.pc,fg="#4B3D2D")
        self.lb.pack(pady=20)

        self.frame=Frame(self.root,bd=12,relief=RIDGE,bg=self.sc)
        self.frame.pack(pady=20)

        self.lb1=Label(self.frame,text="Book Name",font=('Arial',20),bg=self.sc,fg=self.tc)
        self.txt1=Entry(self.frame,font=('Arial',18))

        self.lb2 = Label(self.frame, text="Book Description", font=('Arial', 20),bg=self.sc,fg=self.tc)
        self.txt2 = Entry(self.frame, font=('Arial', 18))

        self.lb3 = Label(self.frame, text="Author Name", font=('Arial', 20),bg=self.sc,fg=self.tc)
        self.txt3 = Entry(self.frame, font=('Arial', 18))

        self.lb4 = Label(self.frame, text="Total Copies", font=('Arial', 20),bg=self.sc,fg=self.tc)
        self.txt4 = Entry(self.frame, font=('Arial', 18))

        self.lb5 = Label(self.frame, text="Book Category", font=('Arial', 20),bg=self.sc,fg=self.tc)
        self.txt5 = ttk.Combobox(self.frame,values=self.get_category(),font=('Arial', 18))

        self.lb6 = Label(self.frame, text="ISBN Code", font=('Arial', 20),bg=self.sc,fg=self.tc)
        self.txt6 = Entry(self.frame, font=('Arial', 18))

        self.lb7 = Label(self.frame, text="Library Id", font=('Arial', 20),bg=self.sc,fg=self.tc)
        self.txt7 = ttk.Combobox(self.frame,values=self.get_lib_id(), font=('Arial', 18))

        self.lb1.grid(row=0,column=0,padx=10,pady=10)
        self.txt1.grid(row=0,column=1,padx=10,pady=10)

        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2.grid(row=1, column=1, padx=10, pady=10)

        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.txt3.grid(row=2, column=1, padx=10, pady=10)

        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.txt4.grid(row=3, column=1, padx=10, pady=10)

        self.lb5.grid(row=4, column=0, padx=10, pady=10)
        self.txt5.grid(row=4, column=1, padx=10, pady=10)

        self.lb6.grid(row=5, column=0, padx=10, pady=10)
        self.txt6.grid(row=5, column=1, padx=10, pady=10)

        self.lb7.grid(row=6, column=0, padx=10, pady=10)
        self.txt7.grid(row=6, column=1, padx=10, pady=10)

        self.btn=Button(self.root,text="ADD",font=('Arial',20),command=self.add,bg="#4B3D2D",highlightthickness=2,fg=self.tc)
        self.btn.pack(pady=20)

        self.get_category()

        self.root.mainloop()
    def add(self):
        name=self.txt1.get()
        des=self.txt2.get()
        auth_name=self.txt3.get()
        t_cpy=self.txt4.get()
        cat=self.txt5.get()
        isbn=self.txt6.get()
        lib_id=self.txt7.get()

        q = f"select * from books where name='{name}' and author_name='{auth_name}'"
        self.cr.execute(q)
        result = self.cr.fetchall()

        if name=='' or des=='' or auth_name=='' or t_cpy=='' or cat=='' or isbn=='' or lib_id=='':
            msg.showwarning('warning','Please fill all details')

        elif len(result)==0:
            if t_cpy.isdigit():
                qy=f"insert into books values(null,'{name}','{des}','Available','{auth_name}',{t_cpy},'{isbn}','{cat}',{lib_id})"
                self.cr.execute(qy)
                msg.showinfo('success','Book Added Successfully')
                self.conn.commit()
                self.conn.close()
                self.reset()
            else:
                msg.showerror('error','Total Copies should be a number')
        else:
            msg.showwarning('warning','Same Author book is available')



    def get_category(self):
        q1=f"select * from category"
        self.cr.execute(q1)
        res1=self.cr.fetchall()
        list1=[]
        for i in range(0,len(res1)):
            list1.append(res1[i][0])
        return list1
    def get_lib_id(self):
        q1=f"select * from admin"
        self.cr.execute(q1)
        res1=self.cr.fetchall()
        list1=[]
        for i in range(0,len(res1)):
            list1.append(res1[i][0])
        return list1
    def reset(self):
        self.txt1.delete(0, END)
        self.txt2.delete(0, END)
        self.txt3.delete(0, END)
        self.txt4.delete(0, END)
        self.txt6.delete(0, END)
        self.txt5.set('')
        self.txt7.set('')
#ob=add_books()