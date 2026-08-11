from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as msg
import add_admin
import add_books
import view_admin
import books_category
import update_category
import view_books
import change_admin_password
import add_students
import view_students
import issue_book
from PIL import Image,ImageTk

class main_menu:
    def __init__(self,admininfo):
        self.admininfo=admininfo
        print(self.admininfo)

        self.root=Toplevel()
        self.root.state('zoomed')
        self.root.title("Admin dashboard")
        self.mainmenu=Menu(self.root)
        self.root.configure(menu=self.mainmenu)

        self.adminmenu=Menu(self.mainmenu,tearoff=0)
        self.mainmenu.add_cascade(label="Manage Library Admin",menu=self.adminmenu)
        self.adminmenu.add_command(label="Add Admin",command=add_admin.Main)
        self.adminmenu.add_command(label="View Admin",command=view_admin.Main)

        self.s_menu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="Manage Students", menu=self.s_menu)
        self.s_menu.add_command(label="Add students", command=add_students.students)
        self.s_menu.add_command(label="View Students", command=view_students.Main)

        self.b_menu = Menu(self.mainmenu, tearoff=0)
        self.mainmenu.add_cascade(label="Manage Books", menu=self.b_menu)
        self.b_menu.add_command(label="Add Books", command=add_books.add_books)
        self.b_menu.add_command(label="View Books", command=view_books.Main)

        self.categorymenu=Menu(self.mainmenu,tearoff=0)
        self.mainmenu.add_cascade(label="Manage Category",menu=self.categorymenu)
        self.categorymenu.add_command(label="Add Category",command=books_category.category)
        self.categorymenu.add_command(label="View Category",command=update_category.category_view)

        self.mainmenu.add_cascade(label="Issue Books",command=issue_book.issue_book)

        self.logout=Menu(self.mainmenu,tearoff=0)
        self.mainmenu.add_cascade(label="Library Account ",menu=self.logout)
        self.logout.add_cascade(label="Change Password",command=lambda:change_admin_password.login(self.admininfo[0][2]))
        self.logout.add_cascade(label="Logout", command=self.root.destroy)

        self.image=Image.open("lib1.jpg")
        self.width=self.root.winfo_screenwidth()
        self.height=self.root.winfo_screenheight()
        self.img=self.image.resize((self.width,self.height))
        bg=ImageTk.PhotoImage(self.img)

        c=Canvas(self.root,width=self.width,height=self.height,highlightbackground="black",highlightthickness=2)
        c.pack(fill='both',expand=True)
        c.create_image(0,0,image=bg,anchor=NW)

        c.create_text(680,40,font=('',48,'bold'))

        self.root.mainloop()
#ob=main_menu()
