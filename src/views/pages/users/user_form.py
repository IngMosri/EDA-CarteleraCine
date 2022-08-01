from tkinter import *
import tkinter.ttk as TTK

from models.users import ListUser, User
from scripts.filterOptions import FilterOptions
from scripts.listData import ListData
import views.pages.users.user_list as UserList

class UserFormView:
    def __init__(self, master, list: ListData, user: User = None):
        self.master = master
        self.list = list
        self.userEdit = user

        self.user = StringVar()
        self.user.set('')
        self.password = StringVar()
        self.password.set('')
        self.status = StringVar()
        self.status.set('Activo')

        if (self.userEdit != None):
            self.user.set(self.userEdit.user_name)
            self.password.set(self.userEdit.password)
            self.status.set(('Activo' if self.userEdit.is_active else 'Inactivo'))

        # create Users main container
        self.frameUsers = Frame(self.master, bg='#ffffff')
        self.frameUsers.pack(fill='x', side='top', anchor='w', padx=30, pady=40)

        # create Title container
        self.frameTitle = Frame(self.frameUsers, bg='#ffffff')
        self.frameTitle.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        # create Title 
        title = Label(self.frameTitle, text='Agregar usuario', font=('arial', 20,'normal'), bg='#ffffff', fg='#4267b2')
        title.pack(padx=0, pady=10, side='left', anchor='n')

        # create form 
        frameForm= Frame(self.frameUsers, bg='#ffffff', highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        frameForm.pack(padx=20, pady=20, side='left', anchor='n')

        frameFields = Frame(frameForm, bg='#ffffff')
        frameFields.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        labelUser = Label(frameFields, text='Usuario:', font=('arial', 10,'normal'), bg='#ffffff', fg='#444444')
        labelUser.pack(side='top', anchor='w', padx=20, pady=5)
        self.entryUser = Entry(frameFields, width=70, relief='flat', textvariable=self.user, highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        self.entryUser.pack(fill='x', padx=20, pady=5, ipady=3)

        labelPassword = Label(frameFields, text='Contraseña:', font=('arial', 10,'normal'), bg='#ffffff', fg='#444444')
        labelPassword.pack(side='top', anchor='w', padx=20, pady=5)
        self.entryPassword = Entry(frameFields, show='*', width=70, relief='flat', textvariable=self.password, highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        self.entryPassword.pack(fill='x', padx=20, pady=5, ipady=3)

        labelStatus = Label(frameFields, text='Estatus:', font=('arial', 10,'normal'), bg='#ffffff', fg='#444444')
        labelStatus.pack(side='top', anchor='w', padx=20, pady=5)
        self.comboBoxStatus = TTK.Combobox(frameFields, width=30, textvariable=self.status)
        self.comboBoxStatus['values'] = [
            'Activo', 
            'Inactivo'
        ]
        self.comboBoxStatus.pack(side='top', anchor='w', padx=20, pady=5, ipady=3)

        # create Error container
        self.frameErrorContainer = Frame(frameFields, bg='#ffffff')
        self.frameErrorContainer.pack(fill='x', side='top', anchor='w', padx=10, pady=10)
        self.frameError = Frame(self.frameErrorContainer, bg='#ffffff')
        self.frameError.pack(fill='x', side='top', anchor='w', padx=10)

        # create frame for buttons
        frameButtons = Frame(frameForm, bg='#ffffff')
        frameButtons.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        # create button cancel
        frameCancel= Frame(frameButtons, bg='#ffffff', highlightthickness=2, highlightbackground='#11285b', highlightcolor='#11285b')
        frameCancel.pack(padx=25, pady=10, side='left', anchor='n')
        buttonCancel = Button(frameCancel, font=('arial', 12,'normal'), text='Cancelar', bg='#ffffff', relief='flat', activebackground='#ffffff', fg='#11285b', command=lambda: self.goBack())
        buttonCancel.pack()

        # create button add user
        frameCreate= Frame(frameButtons, bg='#ffffff', highlightthickness=2, highlightbackground='#ffffff', highlightcolor='#ffffff')
        frameCreate.pack(padx=25, pady=10, side='right', anchor='n')
        buttonCreate = Button(frameCreate, font=('arial', 12,'normal'), text='Guardar', bg='#11285b', relief='flat', activebackground='#11285b', fg='#ffffff', command=lambda: self.save())
        buttonCreate.pack()
        

   
    def save(self):
        error = False

        error = True if self.user.get() == '' else error
        error = True if self.password.get() == '' else error

        if (error == False):
            filters = [ FilterOptions('user_name', (None if self.userEdit is None else self.user.get())) ]

            resultUser: ListUser = self.list.users.getByFilter(filters)
            
            if (resultUser.list == None or (True if self.userEdit is None else (resultUser.list.data.user_id == self.userEdit.user_id))):
                if (self.userEdit != None):
                    user = User(self.userEdit.user_id, self.user.get(), self.password.get(), (1 if self.status.get() == 'Activo' else 0))
                    self.list.users.update(self.userEdit.pos, user)
                    self.goBack()
                else:
                    user = User(None, self.user.get(), self.password.get(), (1 if self.status.get() == 'Activo' else 0))
                    self.list.users.insert(user, True)
                    self.goBack()
            else:
                self.showError('El usuario ' + self.user.get() + ' ya está siendo ocupado, por favor ingrese otro nombre de usuario')
        else:
            self.showError('Por favor llene todos los campos correctamente')

           
    def showError(self, text):
        self.frameError.pack_forget()
        # create Error field container
        self.frameError = Frame(self.frameErrorContainer, bg='#ffe2e2', highlightthickness=2, highlightbackground='#f64e4e', highlightcolor='#f64e4e')
        self.frameError.pack(fill='x', side='top', padx=10)
        lavelError = Label(self.frameError, text=text, font=('arial', 10,'normal'), bg='#ffe2e2', fg='#f64e4e')
        lavelError.pack(side='top', padx=20, pady=5)

    def goBack(self):
        self.frameUsers.pack_forget()
        UserList.UserListView(self.master, self.list)