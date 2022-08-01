from tkinter import * 
from tkinter import messagebox

from views.home import HomeView
from scripts.listData import ListData

listData = ListData()
listData.getDatabaseData()

rootUi = Tk()
app = HomeView(rootUi, listData)

def on_closing():
    if messagebox.askyesno("Salir", "¿Deseas cerrar el programa?"):
        listData.backUpData()
        rootUi.destroy()

rootUi.protocol("WM_DELETE_WINDOW", on_closing)
rootUi.mainloop()