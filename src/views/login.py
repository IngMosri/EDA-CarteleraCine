from tkinter import * 
from PIL import ImageTk, Image
import tkinter.font as font
from scripts.filterOptions import FilterOptions
from scripts.listData import ListData

import views.home as Home
from models.users import *

class LoginView:
    def __init__(self, master, list: ListData):
        self.master = master
        self.list = list

        self.user = StringVar()
        self.user.set('')

        self.password = StringVar()
        self.password.set('')

        # set default configurations of window
        self.master.title('Cartelera de cine | Login')
        self.master.iconbitmap('./src/assets/cine_icon.ico')
        self.master.geometry('400x500')
        self.master.config(bg='#11285b')
        self.master.resizable(False, False)

        # create Login container
        self.frameLogin = Frame(self.master)
        self.frameLogin.pack(fill='x', side='top', anchor=CENTER, pady=10, padx=20)
        self.frameLogin.config(bg='#11285b')
        
        # create Back button
        fontBold = font.Font(weight="normal")
        self.btnBack = Button(self.frameLogin, font=fontBold, bg='#11285b', relief='flat', activeforeground='#dddddd', activebackground='#11285b', fg='#ffffff', text='← Regresar', command=lambda: self.back())
        self.btnBack.pack(padx=10, pady=10, side='top', anchor='w')

        # create icon in topbar
        logoImage = Image.open('./src/assets/cine_logo.png')
        logoIcon = ImageTk.PhotoImage(logoImage.resize((240, 60), Image.ANTIALIAS))
        logoLabel = Label(self.frameLogin, image=logoIcon, bg='#11285b')
        logoLabel.image = logoIcon
        logoLabel.pack(padx=10, pady=10)

        # create Login container
        self.frameLoginContainer = Frame(self.frameLogin)
        self.frameLoginContainer.pack(fill='x', side='top', anchor=CENTER, padx=10)
        self.frameLoginContainer.config(bg='#4267b2')

        # create title Login
        titleLogin = Label(self.frameLoginContainer, text='LOGIN', font=('arial', 20,'normal'), bg='#4267b2', fg='#ffffff')
        titleLogin.pack(padx=10, pady=10, side='top')
        
        # create Field container
        frameFields = Frame(self.frameLogin)
        frameFields.pack(fill='x', side='top', anchor='w', padx=10)
        frameFields.config(bg='#4267b2')

        # create Field user
        labelUser = Label(frameFields, text='Usuario:', font=('arial', 10,'normal'), bg='#4267b2', fg='#ffffff')
        labelUser.pack(side='top', anchor='w', padx=20, pady=5)
        self.entryUser = Entry(frameFields, width=50, relief='flat', textvariable=self.user)
        self.entryUser.pack(fill='x', padx=20, pady=5, ipady=3)

        # create Field password
        labelPassword = Label(frameFields, text='Contraseña:', font=('arial', 10,'normal'), bg='#4267b2', fg='#ffffff')
        labelPassword.pack(side='top', anchor='w', padx=20, pady=5)
        self.entryPassword = Entry(frameFields, show='*', width=50, relief='flat', textvariable=self.password)
        self.entryPassword.pack(fill='x', padx=20, pady=5, ipady=3)

        # create Error container
        self.frameErrorContainer = Frame(frameFields, bg='#4267b2')
        self.frameErrorContainer.pack(fill='x', side='top', anchor='w', padx=10, pady=10)
        self.frameError = Frame(self.frameErrorContainer, bg='#4267b2')
        self.frameError.pack(fill='x', side='top', anchor='w', padx=10)

        # create Login button
        fontBold = font.Font(weight="bold")
        self.btnLogin = Button(frameFields, font=fontBold, bg='#e3b734', relief='flat', activebackground='#c7a02e', fg='#11285b', text='Iniciar sesión', command=lambda: self.login())
        self.btnLogin.pack(padx=10, pady=10, side='top')

    def login(self):
        user = self.user.get()
        password = self.password.get()

        if (user != '' and password != ''):
            filters = [
                FilterOptions('user_name', user),
                FilterOptions('password', password),
                FilterOptions('is_active', 1)
            ]

            result: ListUser = self.list.users.getByFilter(filters)

            if (result.list != None):
                userId = result.list.data.user_id

                self.frameLogin.pack_forget()
                Home.HomeView(self.master, self.list, userId)
            else:
                self.showError('Las credenciales son incorrectas')
        else:
            self.showError('Por favor llene todos los campos')

    def showError(self, text):
        self.frameError.pack_forget()
        # create Error field container
        self.frameError = Frame(self.frameErrorContainer, bg='#ffe2e2', highlightthickness=2, highlightbackground='#f64e4e', highlightcolor='#f64e4e')
        self.frameError.pack(fill='x', side='top', padx=10)
        lavelError = Label(self.frameError, text=text, font=('arial', 10,'normal'), bg='#ffe2e2', fg='#f64e4e')
        lavelError.pack(side='top', padx=20, pady=5)

    def back(self):
        self.frameLogin.pack_forget()
        Home.HomeView(self.master, self.list)