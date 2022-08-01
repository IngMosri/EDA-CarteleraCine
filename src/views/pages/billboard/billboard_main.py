from tkinter import *
from scripts.listData import ListData 

import views.pages.billboard.billboard_list as BillboardView

class BillboardMainView:
    def __init__(self, master, list: ListData, userId=None):
        self.master = master
        self.list = list
        self.userId = userId

        # create Users container
        self.frameContainer = Frame(self.master, bg='#ffffff')
        self.frameContainer.pack(fill='both', expand=1, side='top', anchor='w', padx=0, pady=0)

        BillboardView.BillboardListView(self.frameContainer, self.list, self.userId)