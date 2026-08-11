#id,issue_date,due_date,return_date,status,fine,book_d(fk),lib-id(fk),student_id(fk)

from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import *
from tkcalendar import DateEntry
from datetime import *

class issue_book():
    def __init__(self):
        self.background = "#D9CBA0"
        self.maincolor = "#4B3D2D"
        self.seccolor = 'white'

        self.textcolor = 'BLACK'
        self.buttoncolor = '#D9CBA0'
        self.labelfont = ('Times New Roman', 20, 'bold')
        self.conn = getConnection()
        self.cr = self.conn.cursor()
        self.font = ('Times New Roman', 16, 'bold')

        self.root = Tk()
        self.root.state('zoomed')
        self.root.title('LIBRARY MANAGEMENT || ISSUE BOOKS')
        self.root.configure(background=self.background)

        self.mainlabel = Label(self.root, text="ISSUE BOOKS", font=('Times New Roman', 30, 'bold'), bg=self.background,fg='#4B3D2D')
        self.mainlabel.pack(pady=20, side=TOP)

        self.searchFrame = Frame(self.root, bg=self.seccolor, padx=20, pady=20,bd=5,relief=SOLID)
        self.searchFrame.pack(pady=10)

        self.searchLabel = Label(self.searchFrame, text="Search", font=('Arial',20,'bold'), bg=self.seccolor,
                                 foreground=self.textcolor)
        self.searchLabel.grid(row=0, column=0, pady=10, padx=10)
        self.searchEntry = Entry(self.searchFrame, width=30, font=self.font, highlightthickness=2,
                                 highlightbackground='black')
        self.searchEntry.grid(row=0, column=1, pady=10, padx=10)

        self.searchBtn = Button(self.searchFrame, width=10, text="Search", font=self.font,
                                command=self.searchbooks,
                                relief=SOLID, bg=self.buttoncolor, foreground=self.textcolor, highlightthickness=2)
        self.searchBtn.grid(row=0, column=2, pady=10, padx=10)

        self.refreshBtn = Button(self.searchFrame, width=10, text="Refresh", font=self.font, relief=SOLID,
                                 command=self.refreshdata, bg=self.buttoncolor, foreground=self.textcolor,
                                 highlightthickness=2)
        self.refreshBtn.grid(row=0, column=3, pady=10, padx=10)

        self.booksTable = ttk.Treeview(self.root, columns=(
        'id', 'name', 'description', 'status', 'author_name', 'total_copies', 'isbn', 'library_id', 'library_Id',
        'category_name'))
        self.booksTable.heading('id', text='Enter ID ', anchor=CENTER)
        self.booksTable.heading('name', text='Name', anchor=CENTER)
        self.booksTable.heading('description', text='Description', anchor=CENTER)
        self.booksTable.heading('status', text='Status', anchor=CENTER)
        self.booksTable.heading('author_name', text='Author Name', anchor=CENTER)
        self.booksTable.heading('total_copies', text='Total Copies', anchor=CENTER)
        self.booksTable.heading('isbn', text='ISBN', anchor=CENTER)
        self.booksTable.heading('library_id', text='Category Name', anchor=CENTER)
        self.booksTable.heading('library_Id', text='Library ID', anchor=CENTER)
        self.booksTable.heading('category_name', text='Library Name', anchor=CENTER)
        self.booksTable['show'] = 'headings'
        self.booksTable.column('id', width=8, anchor=CENTER)
        self.booksTable.column('name', width=10, anchor=CENTER)
        self.booksTable.column('description', width=10, anchor=CENTER)
        self.booksTable.column('status', width=10, anchor=CENTER)
        self.booksTable.column('author_name', width=10, anchor=CENTER)
        self.booksTable.column('total_copies', width=10, anchor=CENTER)
        self.booksTable.column('isbn', width=10, anchor=CENTER)
        self.booksTable.column('library_id', width=10, anchor=CENTER)
        self.booksTable.column('library_Id', width=10, anchor=CENTER)
        self.booksTable.column('category_name', width=10, anchor=CENTER)

        self.booksTable.pack(expand=1, fill='both', padx=10, pady=10)
        self.getBooksInfo()

        self.style = ttk.Style()
        self.style.configure('Treeview.Heading', font=self.font, foreground='#4B3D2D')
        self.style.configure('Treeview', font=self.font, rowheight=40, )

        self.booksTable.bind('<Double-1>', self.openIssueBook)

        self.root.mainloop()

    def openIssueBook(self, event):
        row = self.booksTable.selection()
        row_id = row[0]
        items = self.booksTable.item(row_id)
        data = items["values"]

        self.root1 = Toplevel()  # create new window
        self.root1.geometry('600x600')
        self.root1.title('Issue Books')

        self.root1.configure(bg="#D9CBA0")

        self.mainlable1 = Label(self.root1, text="Issue Books", font=("Courier New", 24, 'bold'), bg="#D9CBA0",
                                foreground='#4B3D2D')
        self.mainlable1.pack(pady=20)

        self.updateForm = Frame(self.root1, bg="#A67C4D", padx=20, pady=20,
                                bd=5,relief=SOLID)
        self.updateForm.pack(pady=10)

        self.lb1 = Label(self.updateForm, text="Book ID", font=self.font, bg="#A67C4D",
                         fg='white')
        self.lib_id = data[8]


        self.txt1 = Entry(self.updateForm, font=self.font)
        self.lb1.grid(row=0, column=0, padx=10, pady=10)
        self.txt1.grid(row=0, column=1, padx=10, pady=10)
        self.txt1.insert(0, data[0])
        self.txt1.configure(state='readonly')

        self.lb2 = Label(self.updateForm, text="Book Name", font=self.font, bg="#A67C4D",
                         fg='white')
        self.txt2 = Entry(self.updateForm, font=self.font)
        self.lb2.grid(row=1, column=0, padx=10, pady=10)
        self.txt2.grid(row=1, column=1, padx=10, pady=10)
        self.txt2.insert(0, data[1])
        self.txt2.configure(state='readonly')

        self.lb3 = Label(self.updateForm, text="ISBN ", font=self.font, bg="#A67C4D",
                         fg='white')
        self.txt3 = Entry(self.updateForm, font=self.font)
        self.lb3.grid(row=2, column=0, padx=10, pady=10)
        self.txt3.grid(row=2, column=1, padx=10, pady=10)
        self.txt3.insert(0, data[6])
        self.txt3.configure(state='readonly')

        self.lb4 = Label(self.updateForm, text="Status", font=self.font, bg="#A67C4D",
                         fg='white')
        self.txt4 = Entry(self.updateForm, font=self.font)
        self.lb4.grid(row=3, column=0, padx=10, pady=10)
        self.txt4.grid(row=3, column=1, padx=10, pady=10)
        self.txt4.insert(0, data[3])
        self.txt4.configure(state='readonly')

        self.lb5 = Label(self.updateForm, text="Issue Date", font=self.font, bg="#A67C4D",
                         fg='white')
        self.lb5.grid(row=4, column=0, padx=10, pady=10)
        self.txt5 = DateEntry(self.updateForm, width=18, font=self.font,
                              foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.txt5.grid(row=4, column=1, padx=10, pady=10)

        self.lb6 = Label(self.updateForm, text="Select Student ID", font=self.font, bg="#A67C4D",
                         fg='white')
        self.txt6 =ttk.Combobox(self.updateForm,values=self.get_student_id(), font=self.font)
        self.lb6.grid(row=5, column=0, padx=10, pady=10)
        self.txt6.grid(row=5, column=1, padx=10, pady=10)


        self.updateBtn = Button(self.root1, text="Issue", font=self.labelfont, width=10, relief=RAISED,
                                command=self.issuebook, bg="#4B3D2D", fg='white')
        self.updateBtn.pack(pady=20)

        self.root1.mainloop()

    def getcategory(self):
        q = f"select * from category"
        self.cr.execute(q)
        result = self.cr.fetchall()
        data = []
        for i in result:
            data.append(i[0])
        return data

    def issuebook(self):
        book_id = self.txt1.get()
        issue_date = self.txt5.get()

        student_id = self.txt6.get()
        lib_id = self.lib_id

        issue_date_obj = datetime.strptime(issue_date, "%Y-%m-%d").date()

        due_date = issue_date_obj + timedelta(days=15)

        self.cr.execute(f"SELECT total_copies FROM books WHERE id = '{book_id}'")
        result = self.cr.fetchone()

        if not result:
            msg.showerror("Error", "Book not found.", parent=self.updateForm)
            return



        total_copies = int(result[0])

        if total_copies <= 0:
            msg.showwarning("Unavailable", "This book is currently not available.", parent=self.updateForm)
        else:
            q = f"INSERT INTO issue (issue_date, due_date, status, book_id, lib_id, student_id)VALUES ('{issue_date_obj}', '{due_date}', 'issue', '{book_id}', '{lib_id}', '{student_id}')"
            self.cr.execute(q)
            update_q = f"UPDATE books SET total_copies = total_copies - 1 WHERE id = '{book_id}'"
            self.cr.execute(update_q)

            self.cr.execute(f"SELECT total_copies FROM books WHERE id = '{book_id}'")
            updated_result = self.cr.fetchone()
            updated_copies = int(updated_result[0])

            if updated_copies == 0:
                update_status_q = f"UPDATE books SET status = 'unavailable' WHERE id = '{book_id}'"
                self.cr.execute(update_status_q)

            # Commit all changes

            self.conn.commit()
            msg.showinfo("Success", "Book Issued Successfully.", parent=self.updateForm)
            self.root1.destroy()
            self.getBooksInfo()



    def getBooksInfo(self):
        q = f"SELECT books.id,books.name,books.description,books.status,books.author_name,books.total_copies,books.isbn,books.category,admin.id AS lib_id,admin.name AS name FROM books JOIN admin ON books.lib_id = admin.id;"

        self.cr.execute(q)
        res = self.cr.fetchall()
        for row in self.booksTable.get_children():  # to delete repeating row
            self.booksTable.delete(row)
        for i in range(len(res)):
            self.booksTable.insert('', i, values=res[i])


    def searchbooks(self):
        data = self.searchEntry.get()

        q = f"SELECT id, name, description, status, author_name, total_copies, isbn, lib_id ,category FROM books WHERE name LIKE '%{data}%'   OR description LIKE '%{data}%'   OR isbn LIKE '%{data}%'"

        self.cr.execute(q)
        res = self.cr.fetchall()
        for row in self.booksTable.get_children():  # to delete repeating row
            self.booksTable.delete(row)
        for i in range(len(res)):
            self.booksTable.insert('', i, values=res[i])


    def refreshdata(self):
        self.searchEntry.delete(0, 'end')
        self.getBooksInfo()

    def get_student_id(self):
        q=f"select * from students"
        self.cr.execute(q)
        result=self.cr.fetchall()
        list=[]
        for i in result:
            list.append(i[0])
        return list



#obj = issue_book()