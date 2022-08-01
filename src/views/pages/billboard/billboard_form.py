from tkinter import *
import tkinter.ttk as TTK
from tktimepicker import SpinTimePickerModern, SpinTimePickerOld
from tkcalendar import Calendar, DateEntry
from tkinter import ttk
from tktimepicker import constants
import moment
from models.screenMovie import ScreenMovie

from models.users import ListUser, User
from scripts.filterOptions import FilterOptions
from scripts.listData import ListData
import views.pages.billboard.billboard_list as BillboardList

class BillboardFormView:
    def __init__(self, master, list: ListData, userId):
        self.master = master
        self.list = list
        self.userId = userId

        self.movie = StringVar()
        self.movie.set('')
        self.screen = StringVar()
        self.screen.set('')
        self.state = StringVar()
        self.state.set('')
        self.city = StringVar()
        self.city.set('')
        self.date = StringVar()
        self.hour = StringVar()
        self.hour.set('')
        self.minute = StringVar()
        self.minute.set('')

        self.vcmd = self.master.register(self.validateNumber)

        # create Users main container
        self.frameUsers = Frame(self.master, bg='#ffffff')
        self.frameUsers.pack(fill='x', side='top', anchor='w', padx=30, pady=40)

        # create Title container
        self.frameTitle = Frame(self.frameUsers, bg='#ffffff')
        self.frameTitle.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        # create Title 
        title = Label(self.frameTitle, text='Agregar horario', font=('arial', 20,'normal'), bg='#ffffff', fg='#4267b2')
        title.pack(padx=0, pady=10, side='left', anchor='n')

        # create form 
        frameForm= Frame(self.frameUsers, bg='#ffffff', highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        frameForm.pack(padx=20, pady=20, side='left', anchor='n')

        frameFields = Frame(frameForm, bg='#ffffff')
        frameFields.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        titleMovie = Label(frameFields, text='Pelicula', font=('arial', 10,'normal'), justify=LEFT, bg='#ffffff', fg='#444444', width=25, anchor="w")
        titleMovie.grid(row=0, column=0, columnspan=2, padx=20, pady=5, sticky='w')
        titleScreen = Label(frameFields, text='Sala', font=('arial', 10,'normal'), justify=LEFT, bg='#ffffff', fg='#444444', width=25, anchor="w")
        titleScreen.grid(row=0, column=2, columnspan=2, padx=20, pady=5, sticky='w')

        moviesValues = []

        tempMovieList = self.list.movies.list

        while (tempMovieList):
            moviesValues.append(tempMovieList.data.name)
            
            tempMovieList = tempMovieList.next

        self.comboBoxMovie = TTK.Combobox(frameFields, textvariable=self.movie, width=30)
        self.comboBoxMovie['values'] = moviesValues
        
        self.comboBoxMovie.grid(row=1, column=0, columnspan=2, padx=20, pady=5, ipady=3)

        self.entryScreen = Entry(frameFields, width=30, relief='flat', textvariable=self.screen, highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        self.entryScreen.config(validate='all', validatecommand=(self.vcmd, '%P'))
        self.entryScreen.grid(row=1, column=2, columnspan=2, padx=20, pady=5, sticky='we', ipady=3)


        titleState = Label(frameFields, text='Estado', font=('arial', 10,'normal'), justify=LEFT, bg='#ffffff', fg='#444444', width=25, anchor="w")
        titleState.grid(row=2, column=0, columnspan=2, padx=20, pady=5, sticky='w')
        titleCity = Label(frameFields, text='Ciudad', font=('arial', 10,'normal'), justify=LEFT, bg='#ffffff', fg='#444444', width=25, anchor="w")
        titleCity.grid(row=2, column=2, columnspan=2, padx=20, pady=5, sticky='w')

        #Create Combobox state
        stateValues = []

        tempStateList = self.list.states.list

        while (tempStateList):
            stateValues.append(tempStateList.data.name)
            
            tempStateList = tempStateList.next

        self.comboBoxState = ttk.Combobox(frameFields, textvariable=self.state, width=30)
        self.comboBoxState['values'] = stateValues
        self.comboBoxState.grid(row=3, column=0, columnspan=2, padx=20, pady=5, ipady=3)
        self.comboBoxState.current(0)

        # create Filter city

        self.comboBoxCity = ttk.Combobox(frameFields, textvariable=self.city, width=30)
        self.comboBoxCity['values'] = []
        self.comboBoxCity.grid(row=3, column=2, columnspan=2, padx=20, pady=5, ipady=3)

        #create Time and date picker
        titleState = Label(frameFields, text='Fecha', font=('arial', 10,'normal'), justify=LEFT, bg='#ffffff', fg='#444444', width=25, anchor="w")
        titleState.grid(row=4, column=0, columnspan=2, padx=20, pady=5, sticky='w')
        titleCity = Label(frameFields, text='Hora', font=('arial', 10,'normal'), justify=LEFT, bg='#ffffff', fg='#444444', width=5, anchor="w")
        titleCity.grid(row=4, column=2, padx=20, pady=5, sticky='w')
        titleCity = Label(frameFields, text='Minuto', font=('arial', 10,'normal'), justify=LEFT, bg='#ffffff', fg='#444444', width=5, anchor="w")
        titleCity.grid(row=4, column=3, padx=20, pady=5, sticky='w')

        self.datePick = DateEntry(frameFields, date_pattern='yyyy-MM-dd', width= 30, background= "#ffffff", foreground= "white", bd=2, textvariable=self.date)
        self.datePick.grid(row=5, column=0, columnspan=2, padx=20, pady=5, ipady=3)

        self.comboBoxHour = TTK.Combobox(frameFields, textvariable=self.hour, width=9)
        self.comboBoxHour['values'] = [
            '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
            '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
            '20', '21', '22', '23'
        ]
        
        self.comboBoxHour.grid(row=5, column=2, padx=20, pady=5, ipady=3)
        self.comboBoxHour.current(0)

        self.comboBoxMinutes = TTK.Combobox(frameFields, textvariable=self.minute, width=9)
        self.comboBoxMinutes['values'] = [
            '00', '01', '02', '03', '04', '05', '06', '07', '08', '09',
            '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
            '20', '21', '22', '23', '24', '25', '26', '27', '28', '29',
            '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
            '40', '41', '42', '43', '44', '45', '46', '47', '48', '49',
            '50', '51', '52', '53', '54', '55', '56', '57', '58', '59',
        ]
        
        self.comboBoxMinutes.grid(row=5, column=3, padx=20, pady=5, ipady=3)
        self.comboBoxMinutes.current(0)

        # create Error container
        self.frameErrorContainer = Frame(frameFields, bg='#ffffff')
        self.frameErrorContainer.grid(row=6, column=0, columnspan=4, padx=10, pady=10)
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

        self.state.trace("w", lambda name, index,mode, var=frameFields: self.onChangeState())

        self.onChangeState()
    
    def onChangeState(self):
        cityValues = []
        
        filtersState = [ FilterOptions('name', self.state.get()) ]
        states = self.list.states.getByFilter(filtersState)
        filtersCities = [ FilterOptions('state_id', states.list.data.state_id) ]
        cities = self.list.cities.getByFilter(filtersCities)
        tempStateList = cities.list

        while (tempStateList):
            cityValues.append(tempStateList.data.name)
            
            tempStateList = tempStateList.next
            
        self.comboBoxCity['values'] = cityValues
        self.comboBoxCity.current(0)
   
    def validateNumber(self, value):
        if str.isdigit(value) or value == '':
            return True
        else:
            return False

    def save(self):
        error = False

        error = True if self.screen.get() == '' else error
        error = True if self.movie.get() == '' else error
        error = True if self.city.get() == '' else error
        error = True if self.date.get() == '' else error
        error = True if self.hour.get() == '' else error
        error = True if self.minute.get() == '' else error

        if (error == False):
            movieTime = self.date.get() + ' ' + self.hour.get() + ':' + self.minute.get()
            
            filtersMovie = [ FilterOptions('name', self.movie.get()) ]
            movie = self.list.movies.getByFilter(filtersMovie)

            filtersCity = [ FilterOptions('name', self.city.get()) ]
            city = self.list.cities.getByFilter(filtersCity)

            # check if movies are less to 10
            filtersScreen = [ 
                FilterOptions('movie_id', movie.list.data.movie_id),
                FilterOptions('city_id', city.list.data.city_id)
            ]

            screen = self.list.screenMovies.getByFilter(filtersScreen)
            screenCount = screen.getCount()

            filtersScreen2 = [ 
                FilterOptions('screen_number', int(self.screen.get())),
                FilterOptions('city_id', city.list.data.city_id)
            ]

            screen2 = self.list.screenMovies.getByFilter(filtersScreen2)
            tempScreen = screen2.list
            validateHours = []

            while(tempScreen):
                filtersTempMovie = [ FilterOptions('movie_id', tempScreen.data.movie_id) ]
                movieTemp = self.list.movies.getByFilter(filtersTempMovie)
                
                dateFrom = moment.date(tempScreen.data.movie_time)
                dateTo = moment.date(tempScreen.data.movie_time).add(minutes=(int(movieTemp.list.data.length) + 30))
                movieTimeMom = moment.date(movieTime)

                validateHours.append(movieTimeMom >= dateFrom and movieTimeMom <= dateTo)
                
                tempScreen = tempScreen.next

            if (screenCount < 10):
                if (True not in validateHours):
                    screenMovie = ScreenMovie(
                        None,
                        self.screen.get(),
                        movie.list.data.movie_id,
                        city.list.data.city_id,
                        movieTime
                    )
                    self.list.screenMovies.insert(screenMovie, True)
                    self.goBack()
                else:
                    self.showError('El horario que intenta ingresar ya está siendo ocupado, por favor \ncambie de horario o sala')
            else:
                self.showError('Ya existen ' + str(screenCount) + ' horarios registrados para \nla pelicula ' + self.movie.get() + ' \nen la ciudad ' + self.city.get() + ' y no se puede \nagregar más registros, por fabor selecióne otra pelicula o ciudad')
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
        BillboardList.BillboardListView(self.master, self.list, self.userId)