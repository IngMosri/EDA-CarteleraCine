from tkinter import *
from tkinter.ttk import Separator
import datetime

from models.users import *
from scripts.filterOptions import FilterOptions
from scripts.listData import ListData
import views.pages.users.user_form as UserForm

class UserListView:
    def __init__(self, master, list: ListData):
        self.master = master
        self.list = list

        # create Users main container
        self.frameUsers = Frame(self.master, bg='#ffffff')
        self.frameUsers.pack(fill='both', expand=1, side='top', anchor='w', padx=30, pady=30)

        # create Title container
        self.frameTitle = Frame(self.frameUsers, bg='#ffffff')
        self.frameTitle.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        # create Title 
        title = Label(self.frameTitle, text='Usuarios', font=('arial', 20,'normal'), bg='#ffffff', fg='#4267b2')
        title.pack(padx=0, pady=10, side='left', anchor='n')

        # create button add user
        frameCreate= Frame(self.frameTitle, bg='#ffffff', highlightthickness=2, highlightbackground='#11285b', highlightcolor='#11285b')
        frameCreate.pack(padx=25, pady=10, side='right', anchor='n')
        buttonCreate = Button(frameCreate, font=('arial', 12,'normal'), text='+ Agregar usuario', bg='#ffffff', relief='flat', activebackground='#ffffff', fg='#11285b', command=lambda: self.createUser())
        buttonCreate.pack()

        # create scrollable container
        frameBody = Frame(self.frameUsers, bg='#ffffff')
        frameBody.pack(fill='both', expand=1, padx=7, pady=7)

        self.containerTopLevel = Canvas(frameBody, bd=0, highlightthickness=0, relief='ridge', bg='#ffffff')
        self.containerTopLevel.pack(side='left', fill='both', expand=1, padx=7, pady=7)
        
        yScrollbar = Scrollbar(frameBody, orient='vertical', command=self.containerTopLevel.yview)
        yScrollbar.pack(side='right', fill='y')

        self.containerTopLevel.configure(yscrollcommand=yScrollbar.set)
        self.containerTopLevel.bind('<Configure>', lambda e: self.containerTopLevel.configure(scrollregion=self.containerTopLevel.bbox('all')))

        self.frameTopLevel = Frame(self.containerTopLevel, bg='#ffffff')
        self.frameTopLevel.bind('<Configure>', lambda e: self.containerTopLevel.configure(scrollregion=self.containerTopLevel.bbox('all')))

        self.containerTopLevel.create_window((0,0), window=self.frameTopLevel, anchor='nw')
        
        self.containerTopLevel.bind_all("<MouseWheel>", self.onMosueWheel)

        # create Table main container
        self.frameTable = Frame(self.frameTopLevel, bg='#ffffff')
        self.frameTable.pack(fill='x', side='top', anchor='w', padx=0, pady=20)

        self.getUsers()

    def onMosueWheel(self, event):
        self.containerTopLevel.yview_scroll(-1 * (event.delta // 120), "units")
    
    def getUsers(self):
        self.frameTable.pack_forget()

        # create Table main container
        self.frameTable = Frame(self.frameTopLevel, bg='#ffffff')
        self.frameTable.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        # create Table header
        Label(self.frameTable, text='ID', font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=CENTER, width=10).grid(row=0, column=0, padx=0, pady=0)
        Label(self.frameTable, text='Nombre de usuario', font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=CENTER, width=50).grid(row=0, column=1, padx=0, pady=0)
        Label(self.frameTable, text='Estatus', font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=CENTER, width=10).grid(row=0, column=2, padx=0, pady=0)
        Label(self.frameTable, text='Acciones', font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=CENTER, width=30).grid(row=0, column=3, padx=0, pady=0)
        Separator(self.frameTable, orient='horizontal').grid(row=1, column=0, columnspan=4, pady=5, sticky="ew")

        filters = [ FilterOptions('user_name', '', False) ]

        result: ListUser = self.list.users.getByFilter(filters)
        tempList = result.list
        count = 0

        while (tempList):
            self.drawRows(count, tempList.data)

            tempList = tempList.next
            count += 1

    def drawRows(self, index, row: User):
        indexRow = (((index + 1) * 2) + 1)
        indexSeparator = (((index + 1) * 2) + 2)

        Label(self.frameTable, text=row.user_id, font=('arial', 12,'normal'), bg='#ffffff', fg='#444444', justify=CENTER, width=10).grid(row=indexRow, column=0, padx=0, pady=0)
        Label(self.frameTable, text=row.user_name, font=('arial', 12,'normal'), bg='#ffffff', fg='#444444', justify=CENTER, width=50).grid(row=indexRow, column=1, padx=0, pady=0)
        Label(self.frameTable, text=('Activo' if row.is_active else 'Inactivo'), font=('arial', 12,'normal'), bg='#ffffff', fg=('green' if row.is_active else 'red'), justify=CENTER, width=10).grid(row=indexRow, column=2, padx=0, pady=0)
        frameActions = Frame(self.frameTable, bg='#ffffff', width=30)
        frameActions.grid(row=indexRow, column=3, padx=0, pady=0, sticky='ew')
        Separator(self.frameTable, orient='horizontal').grid(row=indexSeparator, column=0, columnspan=4, pady=5, sticky='ew')


        frameEdit = Frame(frameActions, bg='#ffffff', highlightthickness=2, highlightbackground='green', highlightcolor='green')
        frameEdit.grid(row=0, column=1, padx=5, pady=5)
        buttonEdit = Button(frameEdit, font=('arial', 12,'normal'), text='Editar', bg='#ffffff', relief='flat', activebackground='#ffffff', fg='green', command=lambda: self.editUser(row))
        buttonEdit.pack()

        frameDelete = Frame(frameActions, bg='#ffffff', highlightthickness=2, highlightbackground='red', highlightcolor='red')
        frameDelete.grid(row=0, column=2, padx=5, pady=5)
        buttonDelete = Button(frameDelete, font=('arial', 12,'normal'), text='Eliminar', bg='#ffffff', relief='flat', activebackground='#ffffff', fg='red', command=lambda: self.deleteUser(row))
        buttonDelete.pack()

        frameActions.grid_columnconfigure(0, weight=1)
        frameActions.grid_columnconfigure(3, weight=1)
        
    def createUser(self):
        self.frameUsers.pack_forget()
        UserForm.UserFormView(self.master, self.list)

    def editUser(self, user: User):
        self.frameUsers.pack_forget()
        UserForm.UserFormView(self.master, self.list, user)
        
    def deleteUser(self, user: User):
        self.list.users.delete(user.pos)

        self.getUsers()
