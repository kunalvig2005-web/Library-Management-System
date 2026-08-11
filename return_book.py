from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
from connection import *
from datetime import *

class return_book():
    def __init__(self, student_id):
        self.student_id = student_id
        self.background = "#D9CBA0"
        self.maincolor = "#4B3D2D"
        self.seccolor = 'white'
        self.textcolor = 'BLACK'
        self.buttoncolor = '#D9CBA0'
        self.labelfont = ('Times New Roman', 20, 'bold')
        self.conn = getConnection()
        self.cr = self.conn.cursor()
        self.font = ('Times New Roman', 14, 'bold')

        self.root = Toplevel()  # Use Toplevel if called from student dashboard
        self.root.state('zoomed')
        self.root.title(f'STUDENT DASHBOARD || RETURN BOOKS || ID: {self.student_id}')
        self.root.configure(background=self.background)

        self.mainlabel = Label(self.root, text="MY ISSUED BOOKS", font=('Times New Roman', 30, 'bold'), bg=self.background, fg=self.maincolor)
        self.mainlabel.pack(pady=20, side=TOP)

        self.searchFrame = Frame(self.root, bg=self.seccolor, padx=20, pady=20, bd=5, relief=SOLID)
        self.searchFrame.pack(pady=10)

        self.searchLabel = Label(self.searchFrame, text="Search", font=('Arial', 20, 'bold'), bg=self.seccolor, fg=self.textcolor)
        self.searchLabel.grid(row=0, column=0, pady=10, padx=10)
        self.searchEntry = Entry(self.searchFrame, width=30, font=self.font, highlightthickness=2, highlightbackground='black')
        self.searchEntry.grid(row=0, column=1, pady=10, padx=10)

        self.searchBtn = Button(self.searchFrame, width=10, text="Search", font=self.font, command=self.searchIssuedBooks, relief=SOLID, bg=self.buttoncolor, fg=self.textcolor)
        self.searchBtn.grid(row=0, column=2, pady=10, padx=10)

        self.refreshBtn = Button(self.searchFrame, width=10, text="Refresh", font=self.font, command=self.loadIssuedBooks, relief=SOLID, bg=self.buttoncolor, fg=self.textcolor)
        self.refreshBtn.grid(row=0, column=3, pady=10, padx=10)

        self.issueTable = ttk.Treeview(self.root, columns=('id', 'book_id', 'student_id', 'issue_date', 'due_date', 'status'))
        for col in self.issueTable["columns"]:
            self.issueTable.heading(col, text=col.replace('_', ' ').title(), anchor=CENTER)
            self.issueTable.column(col, anchor=CENTER, width=100)
        self.issueTable['show'] = 'headings'
        self.issueTable.pack(expand=1, fill='both', padx=10, pady=10)

        self.issueTable.bind('<Double-1>', self.returnBookWindow)

        self.style = ttk.Style()
        self.style.configure('Treeview.Heading', font=self.font, foreground=self.maincolor)
        self.style.configure('Treeview', font=self.font, rowheight=40)

        self.loadIssuedBooks()

    def loadIssuedBooks(self):
        q = f"SELECT id, book_id, student_id, issue_date, due_date, status FROM issue WHERE status='issue' AND student_id='{self.student_id}'"
        self.cr.execute(q)
        res = self.cr.fetchall()
        for row in self.issueTable.get_children():
            self.issueTable.delete(row)
        for i in res:
            self.issueTable.insert('', END, values=i)

    def searchIssuedBooks(self):
        data = self.searchEntry.get()
        q = f"""SELECT id, book_id, student_id, issue_date, due_date, status 
                FROM issue 
                WHERE status='issue' AND student_id='{self.student_id}' 
                AND (book_id LIKE '%{data}%' OR id LIKE '%{data}%')"""
        self.cr.execute(q)
        res = self.cr.fetchall()
        for row in self.issueTable.get_children():
            self.issueTable.delete(row)
        for i in res:
            self.issueTable.insert('', END, values=i)

    def returnBookWindow(self, event):
        row = self.issueTable.selection()
        if not row:
            return
        data = self.issueTable.item(row[0])['values']

        self.returnWin = Toplevel(self.root)
        self.returnWin.geometry('500x500')
        self.returnWin.title('Return Book')
        self.returnWin.configure(bg=self.background)

        Label(self.returnWin, text="Return Book", font=('Courier New', 24, 'bold'), bg=self.background, fg=self.maincolor).pack(pady=20)

        form = Frame(self.returnWin, bg="#A67C4D", padx=20, pady=20, bd=5, relief=SOLID)
        form.pack(pady=10)

        labels = ["Issue ID", "Book ID", "Student ID", "Issue Date", "Due Date"]
        self.entries = []

        for i, label in enumerate(labels):
            Label(form, text=label, font=self.font, bg="#A67C4D", fg='white').grid(row=i, column=0, padx=10, pady=10)
            entry = Entry(form, font=self.font)
            entry.grid(row=i, column=1, padx=10, pady=10)
            entry.insert(0, data[i])
            entry.configure(state='readonly')
            self.entries.append(entry)

        self.issue_id = data[0]
        self.book_id = data[1]

        Button(self.returnWin, text="Return", font=self.labelfont, width=10, relief=RAISED, bg=self.maincolor, fg='white', command=self.returnBook).pack(pady=20)

    def returnBook(self):
        return_date = datetime.now().date()

        # Fetch due date from the entries (5th index)
        due_date_str = self.entries[4].get()
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()

        # Calculate fine
        fine = 0
        if return_date > due_date:
            days_late = (return_date - due_date).days
            fine = days_late * 50

        # Update issue record with status and return_date, and also store fine
        self.cr.execute(f"""
            UPDATE issue 
            SET status='returned', return_date='{return_date}', fine={fine}
            WHERE id='{self.issue_id}'
        """)

        # Update total copies of the book
        self.cr.execute(f"UPDATE books SET total_copies = total_copies + 1 WHERE id='{self.book_id}'")

        # Check if book should be marked available
        self.cr.execute(f"SELECT total_copies FROM books WHERE id='{self.book_id}'")
        total = self.cr.fetchone()[0]
        if total > 0:
            self.cr.execute(f"UPDATE books SET status='available' WHERE id='{self.book_id}'")

        self.conn.commit()

        # Show success message with fine info
        if fine > 0:
            msg.showinfo("Book Returned", f"Book returned successfully.\nFine: ₹{fine}", parent=self.returnWin)
        else:
            msg.showinfo("Book Returned", "Book returned successfully. No fine.", parent=self.returnWin)

        self.returnWin.destroy()
        self.loadIssuedBooks()
