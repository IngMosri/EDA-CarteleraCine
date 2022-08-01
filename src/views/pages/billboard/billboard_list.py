from tkinter import *
from tkinter import ttk
from tkinter.ttk import Separator
import moment
from tkcalendar import Calendar, DateEntry

from models.movies import ListMovie
from models.screenMovie import ListScreenMovie, ScreenMovie
from scripts.binaryTree import TreeNode
from scripts.filterOptions import FilterOptions
from scripts.listData import ListData 
import views.pages.billboard.billboard_form as BilboardForm

class BillboardListView:
    def __init__(self, master, list: ListData, userId=None):
        self.master = master
        self.list = list
        self.userId = userId

        self.filterState = StringVar()
        self.filterState.set('')
        self.filterCity = StringVar()
        self.filterCity.set('')
        self.filterDate = StringVar()
        self.filterOrder = StringVar()
        self.filterOrder.set('')

        # create ScreenBillboard main container
        self.mainFrameBillboard = Frame(self.master, bg='#ffffff')
        self.mainFrameBillboard.pack(fill='both', expand=1, side='top', anchor='w', padx=0, pady=0)
        
        # create topbar for filters and set default configuration
        self.frameFilters = Frame(self.mainFrameBillboard)
        self.frameFilters.pack(fill='x', side='top', anchor='w')
        self.frameFilters.config(height='25px')
        self.frameFilters.config(bg='#333333')

        # create Filter state
        stateValues = []

        tempStateList = self.list.states.list

        while (tempStateList):
            stateValues.append(tempStateList.data.name)
            
            tempStateList = tempStateList.next

        titleState = Label(self.frameFilters, text='Seleccione un estado', font=('arial', 10,'normal'), bg='#333333', fg='#ffffff')
        titleState.grid(row=0, column=1, padx=10, pady=10)

        self.comboBoxState = ttk.Combobox(self.frameFilters, textvariable=self.filterState)
        self.comboBoxState['values'] = stateValues
        self.comboBoxState.grid(row=0, column=2, padx=10, pady=10, ipady=3)
        self.comboBoxState.current(0)

        # create Filter city
        titleCity = Label(self.frameFilters, text='Seleccione una ciudad', font=('arial', 10,'normal'), bg='#333333', fg='#ffffff')
        titleCity.grid(row=0, column=3, padx=10, pady=10)

        self.comboBoxCity = ttk.Combobox(self.frameFilters, textvariable=self.filterCity)
        self.comboBoxCity['values'] = []
        self.comboBoxCity.grid(row=0, column=4, padx=10, pady=10, ipady=3)
        # self.comboBoxCity.current(0)

        titleCalendar = Label(self.frameFilters, text='Fecha', font=('arial', 10,'normal'), bg='#333333', fg='#ffffff')
        titleCalendar.grid(row=0, column=5, padx=10, pady=10)
        self.calendar = DateEntry(self.frameFilters, date_pattern='yyyy-MM-dd', width= 16, background= "#ffffff", foreground= "white", bd=2, textvariable=self.filterDate)
        self.calendar.grid(row=0, column=6, padx=10, pady=10, ipady=3)

        # create Filter city
        titleOrder = Label(self.frameFilters, text='Orden', font=('arial', 10,'normal'), bg='#333333', fg='#ffffff')
        titleOrder.grid(row=0, column=7, padx=10, pady=10)

        self.comboBoxOrder = ttk.Combobox(self.frameFilters, textvariable=self.filterOrder)
        self.comboBoxOrder['values'] = [
            'Ascendente', 
            'Descendente'
        ]
        self.comboBoxOrder.grid(row=0, column=8, padx=10, pady=10, ipady=3)
        self.comboBoxOrder.current(0)

        # create ScreenBillboard main container
        self.frameBillboard = Frame(self.mainFrameBillboard, bg='#ffffff')
        self.frameBillboard.pack(fill='both', expand=1, side='top', anchor='w', padx=30, pady=30)

        # create Title container
        self.frameTitle = Frame(self.frameBillboard, bg='#ffffff')
        self.frameTitle.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        # create Title 
        title = Label(self.frameTitle, text='Cartelera', font=('arial', 20,'normal'), bg='#ffffff', fg='#4267b2')
        title.pack(padx=0, pady=10, side='left', anchor='n')


        if (self.userId != None):
            # create button add billboard
            frameCreate= Frame(self.frameTitle, bg='#ffffff', highlightthickness=2, highlightbackground='#11285b', highlightcolor='#11285b')
            frameCreate.pack(padx=25, pady=10, side='right', anchor='n')
            buttonCreate = Button(frameCreate, font=('arial', 12,'normal'), text='+ Agregar horario', bg='#ffffff', relief='flat', activebackground='#ffffff', fg='#11285b', command=lambda: self.createScreenMovie())
            buttonCreate.pack()

        # create scrollable container
        frameBody = Frame(self.frameBillboard, bg='#ffffff')
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

        self.filterState.trace("w", lambda name, index,mode, var=self.frameTable: self.onChangeState())
        self.filterCity.trace("w", lambda name, index,mode, var=self.frameTable: self.getBillboard())
        self.filterDate.trace("w", lambda name, index,mode, var=self.frameTable: self.getBillboard())
        self.filterOrder.trace("w", lambda name, index,mode, var=self.frameTable: self.getBillboard())

        self.onChangeState()


    def onChangeState(self):
        cityValues = []
        
        filtersState = [ FilterOptions('name', self.filterState.get()) ]
        states = self.list.states.getByFilter(filtersState)
        filtersCities = [ FilterOptions('state_id', states.list.data.state_id) ]
        cities = self.list.cities.getByFilter(filtersCities)
        tempStateList = cities.list

        while (tempStateList):
            cityValues.append(tempStateList.data.name)
            
            tempStateList = tempStateList.next
            
        self.comboBoxCity['values'] = cityValues
        self.comboBoxCity.current(0)

        self.getBillboard()


    def onMosueWheel(self, event):
        self.containerTopLevel.yview_scroll(-1 * (event.delta // 120), "units")
    
    def getBillboard(self):
        self.frameTable.pack_forget()

        # create Table main container
        self.frameTable = Frame(self.frameTopLevel, bg='#ffffff')
        self.frameTable.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        # create Table header
        Label(self.frameTable, text='Pelicula', font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=LEFT, width=40, anchor="w").grid(row=0, column=0, padx=0, pady=0, sticky='w')
        Label(self.frameTable, text='Sala', font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=LEFT, width=10).grid(row=0, column=1, padx=0, pady=0, sticky='w')
        Label(self.frameTable, text='Hora', font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=LEFT, width=10).grid(row=0, column=2, padx=0, pady=0, sticky='w')
        Label(self.frameTable, text='Fecha', font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=LEFT, width=10).grid(row=0, column=3, padx=0, pady=0, sticky='w')
        Label(self.frameTable, text=('' if self.userId is None else 'Acciones'), font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=CENTER, width=30).grid(row=0, column=4, padx=0, pady=0)
        Separator(self.frameTable, orient='horizontal').grid(row=1, column=0, columnspan=5, pady=5, sticky="ew")


        filtersCities = [ FilterOptions('name', self.filterCity.get()) ]
        cities = self.list.cities.getByFilter(filtersCities)

        filters = [ 
            FilterOptions('city_id', cities.list.data.city_id),
            FilterOptions('movie_time', self.filterDate.get(), False) 
        ]

        result: ListScreenMovie = self.list.screenMovies.getByFilter(filters)
        tempList = result.list
        count = 0

        treeData = TreeNode()

        while (tempList):
            treeData.insert('movie_time', tempList.data)

            tempList = tempList.next
            count += 1

        orderedData = treeData.inorder([], (True if self.filterOrder.get() == 'Ascendente' else False))

        for index, row in enumerate(orderedData):
            self.drawRows(index, row)
            
    def drawRows(self, index, row: ScreenMovie):
        filtersBillboard = [ FilterOptions('movie_id', row.movie_id) ]
        resultBillboard: ListMovie = self.list.movies.getByFilter(filtersBillboard)

        indexRow = (((index + 1) * 2) + 1)
        indexSeparator = (((index + 1) * 2) + 2)

        Label(self.frameTable, text=resultBillboard.list.data.name, font=('arial', 12,'normal'), bg='#ffffff', fg='#444444', justify=CENTER, width=40, anchor="w").grid(row=indexRow, column=0, padx=0, pady=0, sticky='w')
        Label(self.frameTable, text=str(int(row.screen_number)), font=('arial', 12,'normal'), bg='#ffffff', fg='#444444', justify=CENTER, width=10).grid(row=indexRow, column=1, padx=0, pady=0)
        Label(self.frameTable, text=moment.date(row.movie_time).format("hh:mm A"), font=('arial', 12,'normal'), bg='#ffffff', fg='#444444', justify=CENTER, width=10).grid(row=indexRow, column=2, padx=0, pady=0)
        Label(self.frameTable, text=moment.date(row.movie_time).format("YYYY-MM-DD"),  font=('arial', 12,'normal'), bg='#ffffff', fg='#444444', justify=CENTER, width=10).grid(row=indexRow, column=3, padx=0, pady=0)
        frameActions = Frame(self.frameTable, bg='#ffffff', width=30)
        frameActions.grid(row=indexRow, column=4, padx=0, pady=0, sticky='ew')
        Separator(self.frameTable, orient='horizontal').grid(row=indexSeparator, column=0, columnspan=5, pady=5, sticky='ew')

        if (self.userId != None):
            frameDelete = Frame(frameActions, bg='#ffffff', highlightthickness=2, highlightbackground='red', highlightcolor='red')
            frameDelete.grid(row=0, column=2, padx=5, pady=5)
            buttonDelete = Button(frameDelete, font=('arial', 12,'normal'), text='Eliminar', bg='#ffffff', relief='flat', activebackground='#ffffff', fg='red', command=lambda: self.deleteScreenMovie(row))
            buttonDelete.pack()

        frameActions.grid_columnconfigure(0, weight=1)
        frameActions.grid_columnconfigure(3, weight=1)
        
    def createScreenMovie(self):
        self.frameFilters.pack_forget()
        self.mainFrameBillboard.pack_forget()
        BilboardForm.BillboardFormView(self.master, self.list, self.userId)
        
    def deleteScreenMovie(self, screenMovie: ScreenMovie):
        self.list.screenMovies.delete(screenMovie.pos)

        self.getBillboard()
