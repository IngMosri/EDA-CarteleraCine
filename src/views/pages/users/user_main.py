from tkinter import *
from scripts.listData import ListData 

import views.pages.users.user_list as UserList

class UserMainView:
    def __init__(self, master, list: ListData):
        self.master = master
        self.list = list

        # create Users container
        self.frameContainer = Frame(self.master, bg='#ffffff')
        self.frameContainer.pack(fill='both', expand=1, side='top', anchor='w', padx=0, pady=0)

        UserList.UserListView(self.frameContainer, self.list)