from tkinter import *
import books_category
import return_book
import view_category
import change_student_password
import return_book
import only_view_books

class student:
    def __init__(self,student_info):
        self.student_info=student_info
        print(self.student_info)

        self.root = Tk()
        self.root.state('zoomed')
        self.root.title("Student dashboard")
        self.mainmenu = Menu(self.root)
        self.root.configure(menu=self.mainmenu)

        self.mainmenu.add_command(label="View Category", command=view_category.category_view)
        self.mainmenu.add_command(label="View Books", command=only_view_books.Main)

        self.logout = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="Student Account ", menu=self.logout)
        self.logout.add_cascade(label="Change Password",
                                command=lambda: change_student_password.login(self.student_info[0][2]))
        self.logout.add_cascade(label="Logout", command=self.root.destroy)

        self.mainmenu.add_cascade(label="Return Books",command=lambda:return_book.return_book(self.student_info[0][0]))

        self.root.mainloop()

#ob=student()
