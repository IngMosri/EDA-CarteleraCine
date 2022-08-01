from tkinter import * 
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter.ttk import Separator

from models.movies import ListMovie, Movie
from models.screenMovie import ScreenMovie
from scripts.filterOptions import FilterOptions
from scripts.listData import ListData
from scripts.quickSort import quickSort 
import views.pages.movies.movies_form as MovieForm


class MoviesListView:
    def __init__(self, master, list: ListData, userId=None):
        self.master = master
        self.list = list
        self.userId = userId

        self.filterName = StringVar()
        self.filterName.set('')

        self.filterRate = StringVar()
        self.filterRate.set('')
        self.filterGenre = StringVar()
        self.filterGenre.set('')
        self.filterOrder = StringVar()
        self.filterOrder.set('')


        # create Movies main container
        self.mainFrameMovies = Frame(self.master, bg='#ffffff')
        self.mainFrameMovies.pack(fill='both', expand=1, side='top', anchor='w', padx=0, pady=0)
        
        # create topbar for filters and set default configuration
        self.frameFilters = Frame(self.mainFrameMovies)
        self.frameFilters.pack(fill='x', side='top', anchor='w')
        self.frameFilters.config(height='25px')
        self.frameFilters.config(bg='#333333')

        # create Filter Name
        titleName = Label(self.frameFilters, text='Filtrar por nombre', font=('arial', 10,'normal'), bg='#333333', fg='#ffffff')
        titleName.grid(row=0, column=0, padx=10, pady=10)

        self.entryName = Entry(self.frameFilters, relief='flat', textvariable=self.filterName, highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        self.entryName.grid(row=0, column=1, padx=10, pady=10, ipady=3)

        # create Filter Rate
        titleRate = Label(self.frameFilters, text='Filtrar por clasificación', font=('arial', 10,'normal'), bg='#333333', fg='#ffffff')
        titleRate.grid(row=0, column=2, padx=10, pady=10)

        self.comboBoxRate = ttk.Combobox(self.frameFilters, width=7, textvariable=self.filterRate)
        self.comboBoxRate['values'] = [
            '', 
            'AA',
            'A',
            'B',
            'B15',
            'C',
            'D'
        ]
        
        self.comboBoxRate.grid(row=0, column=3, padx=10, pady=10, ipady=3)
        self.comboBoxRate.current(0)

        # create Filter Rate
        genreValues = ['']

        tempList = self.list.genres.list

        while (tempList):
            genreValues.append(tempList.data.name)
            
            tempList = tempList.next

        titleGenre = Label(self.frameFilters, text='Filtrar por genero', font=('arial', 10,'normal'), bg='#333333', fg='#ffffff')
        titleGenre.grid(row=0, column=4, padx=10, pady=10)

        self.comboBoxGenre = ttk.Combobox(self.frameFilters, width=15, textvariable=self.filterGenre)
        self.comboBoxGenre['values'] = genreValues
        self.comboBoxGenre.grid(row=0, column=5, padx=10, pady=10, ipady=3)
        self.comboBoxGenre.current(0)

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

        # create Movies main container
        self.frameMovies = Frame(self.mainFrameMovies, bg='#ffffff', width=70)
        self.frameMovies.pack(fill='both', expand=1, side='top', anchor='w', padx=30, pady=30)

        # create Title container
        self.frameTitle = Frame(self.frameMovies, bg='#ffffff')
        self.frameTitle.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        # create Title 
        title = Label(self.frameTitle, text='Peliculas', font=('arial', 20,'normal'), bg='#ffffff', fg='#4267b2')
        title.pack(padx=0, pady=10, side='left', anchor='n')


        if (self.userId != None):
            # create button add user
            frameCreate= Frame(self.frameTitle, bg='#ffffff', highlightthickness=2, highlightbackground='#11285b', highlightcolor='#11285b')
            frameCreate.pack(padx=25, pady=10, side='right', anchor='n')
            buttonCreate = Button(frameCreate, font=('arial', 12,'normal'), text='+ Agregar pelicula', bg='#ffffff', relief='flat', activebackground='#ffffff', fg='#11285b', command=lambda: self.createMovie())
            buttonCreate.pack()

        # create scrollable container
        frameBody = Frame(self.frameMovies, bg='#ffffff')
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

        self.filterName.trace("w", lambda name, index,mode, var=self.frameTable: self.getMovies())
        self.filterRate.trace("w", lambda name, index,mode, var=self.filterRate: self.getMovies())
        self.filterGenre.trace("w", lambda name, index,mode, var=self.filterGenre: self.getMovies())
        self.filterOrder.trace("w", lambda name, index,mode, var=self.frameTable: self.getMovies())

        self.getMovies()


    def onMosueWheel(self, event):
        self.containerTopLevel.yview_scroll(-1 * (event.delta // 120), "units")
    
    def getMovies(self):
        self.frameTable.pack_forget()

        # create Table main container
        self.frameTable = Frame(self.frameTopLevel, bg='#ffffff')
        self.frameTable.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        # create Table header
        Label(self.frameTable, text='', font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=LEFT, width=70).grid(row=0, column=0, padx=0, pady=0, sticky='w')
        Label(self.frameTable, text=('' if self.userId == None else 'Acciones'), font=('arial', 12,'bold'), bg='#ffffff', fg='#4267b2', justify=CENTER, width=30).grid(row=0, column=1, padx=0, pady=0)
        Separator(self.frameTable, orient='horizontal').grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        filters = [ FilterOptions('name', self.filterName.get(), False) ]

        if (self.filterRate.get() != ''):
            filters.append(FilterOptions('rating', self.filterRate.get()))

        if (self.filterGenre.get() != ''):
            filterGenres = [ FilterOptions('name', self.filterGenre.get()) ]
            genre = self.list.genres.getByFilter(filterGenres)

            filters.append(FilterOptions('genre_id', genre.list.data.genre_id))

        result: ListMovie = self.list.movies.getByFilter(filters)
        tempList = result.list

        arrayToOrder = []

        while (tempList):
            arrayToOrder.append(tempList.data)

            tempList = tempList.next

        quickSort(arrayToOrder, 'name', 0, len(arrayToOrder) - 1, (True if self.filterOrder.get() == 'Ascendente' else False))

        for index, row in enumerate(arrayToOrder):
            self.drawRows(index, row)

    def drawRows(self, index, row: Movie):
        indexRow = (((index + 1) * 2) + 1)
        indexSeparator = (((index + 1) * 2) + 2)

        filters = [ FilterOptions('genre_id', row.genre_id) ]
        genre = self.list.genres.getByFilter(filters)

        frameCellMovies = Frame(self.frameTable, bg='#ffffff', width=30)
        frameCellMovies.grid(row=indexRow, column=0, padx=0, pady=0, sticky='ew')
        frameActions = Frame(self.frameTable, bg='#ffffff', width=30)
        frameActions.grid(row=indexRow, column=1, padx=0, pady=0, sticky='ew')
        Separator(self.frameTable, orient='horizontal').grid(row=indexSeparator, column=0, columnspan=2, pady=5, sticky='ew')

        # create movies information
        movieImage = Image.open(row.image_path)
        moviePoster = ImageTk.PhotoImage(movieImage.resize((85, 130), Image.ANTIALIAS))
        logoPoster = Label(frameCellMovies, image=moviePoster, bg='#11285b')
        logoPoster.image = moviePoster
        logoPoster.grid(row=0, column=0, rowspan=4, padx=40, pady=10)

        # create Title Movie 
        movieTitle = Label(frameCellMovies, text=row.name, font=('arial', 15,'normal'), bg='#ffffff', fg='#777777')
        movieTitle.grid(row=0, column=1, columnspan=4, padx=5, pady=2, sticky='w')

        # create Title Director
        movieDirector = Label(frameCellMovies, text='Director: ' + row.director, font=('arial', 12,'normal'), bg='#ffffff', fg='#aaaaaa')
        movieDirector.grid(row=1, column=1, columnspan=4, padx=5, pady=2, sticky='w')

        # create Title Producer
        movieProducer = Label(frameCellMovies, text='Productor: ' + row.producer, font=('arial', 12,'normal'), bg='#ffffff', fg='#aaaaaa')
        movieProducer.grid(row=2, column=1, columnspan=4, padx=5, pady=2, sticky='w')

        frameBadge = Frame(frameCellMovies, bg='#ffffff', width=30)
        frameBadge.grid(row=3, column=1, columnspan=4, padx=5, pady=2, sticky='w')

        # create Title Rate
        movieRate = Label(frameBadge, text=row.rating, font=('arial', 12,'normal'), bg='#777777', fg='#ffffff')
        movieRate.grid(row=0, column=0, padx=5, pady=2, sticky='w')

        # create Title Length
        movieLength = Label(frameBadge, text=str(int(row.length)) + 'min', font=('arial', 12,'normal'), bg='#222222', fg='#ffffff')
        movieLength.grid(row=0, column=1, padx=5, pady=2, sticky='w')

        # create Title Genre
        movieGenre = Label(frameBadge, text=genre.list.data.name, font=('arial', 12,'normal'), bg='#0b5ba1', fg='#ffffff')
        movieGenre.grid(row=0, column=2, padx=5, pady=2, sticky='w')

        if (self.userId != None):
            frameEdit = Frame(frameActions, bg='#ffffff', highlightthickness=2, highlightbackground='green', highlightcolor='green')
            frameEdit.grid(row=0, column=1, padx=5, pady=5)
            buttonEdit = Button(frameEdit, font=('arial', 12,'normal'), text='Editar', bg='#ffffff', relief='flat', activebackground='#ffffff', fg='green', command=lambda: self.editMovie(row))
            buttonEdit.pack()

            frameDelete = Frame(frameActions, bg='#ffffff', highlightthickness=2, highlightbackground='red', highlightcolor='red')
            frameDelete.grid(row=0, column=2, padx=5, pady=5)
            buttonDelete = Button(frameDelete, font=('arial', 12,'normal'), text='Eliminar', bg='#ffffff', relief='flat', activebackground='#ffffff', fg='red', command=lambda: self.deleteMovie(row))
            buttonDelete.pack()

        frameActions.grid_columnconfigure(0, weight=1)
        frameActions.grid_columnconfigure(3, weight=1)
        
    def createMovie(self):
        self.mainFrameMovies.pack_forget()
        MovieForm.MoviesFormView(self.master, self.userId, self.list)

    def editMovie(self, movie: Movie):
        self.mainFrameMovies.pack_forget()
        MovieForm.MoviesFormView(self.master, self.userId, self.list, movie)
        
    def deleteMovie(self, movie: Movie):
        self.list.movies.delete(movie.pos)

        filters = [ FilterOptions('movie_id', movie.movie_id) ]
        screenMovies = self.list.screenMovies.getByFilter(filters)

        tempList = screenMovies.list

        while (tempList):
            self.list.screenMovies.delete(tempList.data.pos)
            tempList = tempList.next

        self.getMovies()
