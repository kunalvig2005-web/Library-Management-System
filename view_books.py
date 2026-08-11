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
        self.mainLabel.pack(pady=10)

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

        self.book_table = ttk.Treeview(self.root, show='headings',
                                       columns=['id', 'name', 'des', 'status', 'auth_name', 't_cpy', 'isbn', 'cat',
                                                'lib_id'])
        self.book_table.pack(pady=10, expand=True, fill='both')
        self.book_table.heading('id', text='ID')
        self.book_table.heading('name', text='Name')
        self.book_table.heading('des', text='Description')
        self.book_table.heading('status', text='Status')
        self.book_table.heading('auth_name', text='Author Name')
        self.book_table.heading('t_cpy', text='Total Copies')
        self.book_table.heading('isbn', text='ISBN')
        self.book_table.heading('cat', text='Category')
        self.book_table.heading('lib_id', text='Library ID')

        self.book_table.column('id',width=8, anchor='center')
        self.book_table.column('name',width=10, anchor='center')
        self.book_table.column('des',width=10, anchor='center')
        self.book_table.column('status',width=10, anchor='center')
        self.book_table.column('auth_name',width=10, anchor='center')
        self.book_table.column('t_cpy',width=10, anchor='center')
        self.book_table.column('isbn',width=10, anchor='center')
        self.book_table.column('cat',width=10, anchor='center')
        self.book_table.column('lib_id',width=10, anchor='center')

        style = ttk.Style()
        style.configure('Treeview', font=self.font, rowheight=40)
        style.configure('Treeview.Heading', font=self.font,foreground='#4B3D2D')

        self.book_table.bind("<Double-1>", self.openupdatewindow)

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


    def openupdatewindow(self,event):
        id=self.book_table.selection()[0]
        metadata=self.book_table.item(id)
        data=metadata['values']
        print(data)
        self.root1 = Toplevel()
        self.root1.geometry('700x500')
        self.root1.configure(bg="#D9CBA0")
        self.mainLabel2 = Label(self.root1, text="Update/Delete Books", font=('Arial', 24, 'bold'),bg="#D9CBA0",fg='#4B3D2D')

        self.mainLabel2.pack(pady=10)

        self.formFrame = Frame(self.root1,bg="#A67C4D",bd=5,relief=RIDGE)
        self.formFrame.pack(pady=10)
        self.font = ("Arial", 16)

        self.lb1 = Label(self.formFrame, text="Book ID", font=self.font,fg='white',bg="#A67C4D")
        self.txt1 = Entry(self.formFrame, font=self.font)
        self.lb1.grid(row=0, column=0, padx=10,pady=5)
        self.txt1.grid(row=0, column=1, padx=10,pady=5)
        self.txt1.insert(0, data[0])
        self.txt1.config(state='readonly')

        self.lb2 = Label(self.formFrame, text="Enter Name", font=self.font,fg='white',bg="#A67C4D")
        self.txt2 = Entry(self.formFrame, font=self.font)
        self.lb2.grid(row=1, column=0, padx=10,pady=5)
        self.txt2.grid(row=1, column=1, padx=10,pady=5)
        self.txt2.insert(0, data[1])

        self.lb3 = Label(self.formFrame, text="Enter Description", font=self.font,fg='white',bg="#A67C4D")
        self.txt3 = Entry(self.formFrame, font=self.font)
        self.lb3.grid(row=2, column=0, padx=10,pady=5)
        self.txt3.grid(row=2, column=1, padx=10,pady=5)
        self.txt3.insert(0, data[2])

        self.lb4 = Label(self.formFrame, text="Enter status", font=self.font,fg='white',bg="#A67C4D")
        self.txt4 = ttk.Combobox(self.formFrame,state='readonly',values=['Available','Unavailable'], font=self.font)
        self.lb4.grid(row=3, column=0, padx=10,pady=5)
        self.txt4.grid(row=3, column=1, padx=10,pady=5)
        self.txt4.insert(0, data[3])
        self.txt4.set('Available')

        self.lb5 = Label(self.formFrame, text="Enter Author Name", font=self.font,fg='white',bg="#A67C4D")
        self.txt5 = Entry(self.formFrame, font=self.font)
        self.lb5.grid(row=4, column=0, padx=10,pady=5)
        self.txt5.grid(row=4, column=1, padx=10,pady=5)
        self.txt5.insert(0, data[4])

        self.lb6 = Label(self.formFrame, text="Enter Total copies", font=self.font,fg='white',bg="#A67C4D")
        self.txt6 = Entry(self.formFrame, font=self.font)
        self.lb6.grid(row=5, column=0, padx=10,pady=5)
        self.txt6.grid(row=5, column=1, padx=10)
        self.txt6.insert(0, data[5])

        self.lb7 = Label(self.formFrame, text="Enter ISBN Code", font=self.font,fg='white',bg="#A67C4D")
        self.txt7 = Entry(self.formFrame, font=self.font)
        self.lb7.grid(row=6, column=0, padx=10,pady=5)
        self.txt7.grid(row=6, column=1, padx=10,pady=5)
        self.txt7.insert(0, data[6])

        self.updateBtn = Button(self.root1, text="Update", font=self.font,command=self.updateadmin,bg='#4B3D2D',fg='white')
        self.deleteBtn = Button(self.root1, text="Delete", font=self.font,command=self.deleteadmin,bg='#4B3D2D',fg='white')
        self.updateBtn.pack(pady=10)
        self.deleteBtn.pack(pady=10)

        self.root1.mainloop()

    def updateadmin(self):
        id = self.txt1.get()
        name = self.txt2.get()
        des = self.txt3.get()
        status = self.txt4.get()
        auth_name = self.txt5.get()
        t_cpy = self.txt6.get()
        isbn = self.txt7.get()

        if name == "" or des == "" or status == "" or auth_name == "" or t_cpy == "" or isbn == "":
            msg.showwarning("Warning", "Please fill all fields", parent=self.root1)
        elif not t_cpy.isdigit():
            msg.showerror("Error", "Total copies must be a number", parent=self.root1)
        else:
            q1 = "SELECT * FROM books WHERE name=%s AND author_name=%s"
            self.cr.execute(q1, (name, auth_name))
            result = self.cr.fetchall()
            print(result)

            if len(result) <= 1:
                q2 = """
                     UPDATE books
                     SET name=%s, \
                         description=%s, \
                         status=%s, \
                         author_name=%s, \
                         total_copies=%s, \
                         isbn=%s
                     WHERE id = %s \
                     """
                self.cr.execute(q2, (name, des, status, auth_name, int(t_cpy), isbn, id))
                self.conn.commit()
                self.root1.destroy()
                msg.showinfo("Success", "Admin successfully updated")
                self.getValues()
            else:
                msg.showwarning('Error', 'Same author and book already exists', parent=self.root1)

    def deleteadmin(self):
        id = self.txt1.get()
        q4 = f"delete from books where id='{id}'"
        self.cr.execute(q4)
        self.conn.commit()
        self.root1.destroy()
        msg.showinfo("Success", "Admin successfully deleted")
        self.getValues()



#ob=Main()