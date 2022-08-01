from tkinter import * 
from PIL import ImageTk, Image
import tkinter.font as font
import tkinter.ttk as TTK

from scripts.listData import ListData
import views.login as Login
from views.pages.billboard.billboard_main import BillboardMainView
from views.pages.movies.movies_main import MoviesMainView
from views.pages.users.user_main import UserMainView

class HomeView:
    def __init__(self, master, list: ListData, userId=None):
        self.master = master
        self.list = list
        self.userId = userId

        # set default configurations of window
        self.master.title('Cartelera de cine' + ('' if self.userId == None else ' | Admin'))
        self.master.iconbitmap('./src/assets/cine_icon.ico')
        self.master.geometry('1100x850')
        self.master.config(bg='#ffffff')
        self.master.resizable(False, False)

        # create Home container
        self.frameHome = Frame(self.master)
        self.frameHome.pack(fill=BOTH, expand=True, padx=0, pady=0)
        self.frameHome.config(bg='#ffffff')

        # create topbar and set default configuration
        self.frameTopBar = Frame(self.frameHome)
        self.frameTopBar.pack(fill='x', side='top', anchor='w')
        self.frameTopBar.config(height='25px')
        self.frameTopBar.config(bg='#11285b')
 
        # create topbar elements container and set default configuration
        self.frameTopBarContainer = Frame(self.frameTopBar)
        self.frameTopBarContainer.pack(fill='x', side='top', anchor='w')
        self.frameTopBarContainer.config(height='25px')
        self.frameTopBarContainer.config(bg='#11285b')

        # create icon in topbar
        logoImage = Image.open('./src/assets/cine_logo.png')
        logoIcon = ImageTk.PhotoImage(logoImage.resize((120, 30), Image.ANTIALIAS))
        logoLabel = Label(self.frameTopBarContainer, image=logoIcon, bg='#11285b')
        logoLabel.image = logoIcon
        logoLabel.pack(padx=40, pady=10, side='left', anchor='n')

        if (self.userId is None):
            # create Login button
            fontBold = font.Font(weight="bold")
            self.btnLogin = Button(self.frameTopBarContainer, font=fontBold, bg='#e3b734', relief='flat', activebackground='#c7a02e', fg='#11285b', text='Iniciar sesión', command=lambda: self.login())
            self.btnLogin.pack(padx=40, pady=10, side='right', anchor='n')
            # self.btnLogin.grid_forget()
        else:
            # create Logout button
            fontBold = font.Font(weight="bold")
            self.btnLogout = Button(self.frameTopBarContainer, font=fontBold, bg='#e3b734', relief='flat', activebackground='#c7a02e', fg='#11285b', text='Logout', command=lambda: self.logout())
            self.btnLogout.pack(padx=40, pady=10, side='right', anchor='n')
            # self.btnLogout.grid_forget()


        # create topbar for filters and set default configuration
        self.frameMenu = Frame(self.frameHome)
        self.frameMenu.pack(fill='x', side='top', anchor='w')
        self.frameMenu.config(height='25px')
        self.frameMenu.config(bg='#222222')

        self.btnBillboard = Button(self.frameMenu, font=('arial', 12,'normal'), bg='#222222', relief='flat', activebackground='#222222', activeforeground='#e3b734', fg='#e3b734', text='Cartelera', command=lambda: self.selectMenu(1))
        self.btnBillboard.grid(row=0, column=0, padx=10, pady=10)

        self.btnMovies = Button(self.frameMenu, font=('arial', 12,'normal'), bg='#222222', relief='flat', activebackground='#222222',  activeforeground='#e3b734', fg='#ffffff', text='Peliculas', command=lambda: self.selectMenu(2))
        self.btnMovies.grid(row=0, column=1, padx=10, pady=10)

        if (self.userId != None):
            self.btnUsers = Button(self.frameMenu, font=('arial', 12,'normal'), bg='#222222', relief='flat', activebackground='#222222',  activeforeground='#e3b734', fg='#ffffff', text='Usuarios', command=lambda: self.selectMenu(3))
            self.btnUsers.grid(row=0, column=3, padx=10, pady=10)

        # create pages container
        self.framePages = Frame(self.frameHome, bg='#ffffff')
        self.framePages.pack(fill='x', side='top', anchor='w', padx=10, pady=10)

        # create footer and set default configuration
        self.frameFooter = Frame(self.frameHome)
        self.frameFooter.pack(fill='x', side='bottom', anchor='w')
        self.frameFooter.config(height='25px')
        self.frameFooter.config(bg='#222222')

        self.selectMenu(1)

    def login(self):
        self.frameHome.pack_forget()
        Login.LoginView(self.master, self.list)

    def logout(self):
        self.frameHome.pack_forget()
        HomeView(self.master, self.list)

    def selectMenu(self, option):
        if (option == 1):
            self.btnBillboard.config(fg='#e3b734')
            self.btnMovies.config(fg='#ffffff')
            if (self.userId != None):
                self.btnUsers.config(fg='#ffffff')

            # clear pages container
            self.framePages.pack_forget()
            self.framePages = Frame(self.frameHome, bg='#ffffff')
            self.framePages.pack(fill='both', expand=1, side='top', anchor='w', padx=0, pady=0)

            BillboardMainView(self.framePages, self.list, self.userId)
            
        if (option == 2):
            self.btnBillboard.config(fg='#ffffff')
            self.btnMovies.config(fg='#e3b734')
            if (self.userId != None):
                self.btnUsers.config(fg='#ffffff')

            # clear pages container
            self.framePages.pack_forget()
            self.framePages = Frame(self.frameHome, bg='#ffffff')
            self.framePages.pack(fill='both', expand=1, side='top', anchor='w', padx=0, pady=0)

            MoviesMainView(self.framePages, self.list, self.userId)

        if (option == 3):
            self.btnBillboard.config(fg='#ffffff')
            self.btnMovies.config(fg='#ffffff')
            if (self.userId != None):
                self.btnUsers.config(fg='#e3b734')

            # clear pages container
            self.framePages.pack_forget()
            self.framePages = Frame(self.frameHome, bg='#ffffff')
            self.framePages.pack(fill='both', expand=1, side='top', anchor='w', padx=0, pady=0)

            UserMainView(self.framePages, self.list)

