from tkinter import *
import tkinter.ttk as TTK
from tkinter.filedialog import askopenfilename
from shutil import copyfile
import string
import random

from models.movies import ListMovie, Movie
from scripts.filterOptions import FilterOptions
from scripts.listData import ListData
import views.pages.movies.movies_list as MoviesList

class MoviesFormView:
    def __init__(self, master, userId, list: ListData, movie: Movie = None):
        self.master = master
        self.list = list
        self.userId = userId
        self.movieEdit = movie

        self.name = StringVar()
        self.name.set('')
        self.image_path = ''
        self.director = StringVar()
        self.director.set('')
        self.genre_id = ''
        self.genre = StringVar()
        self.genre.set('')
        self.producer = StringVar()
        self.producer.set('')
        self.rating = StringVar()
        self.rating.set('')
        self.length = StringVar()
        self.length.set('')

        if (self.movieEdit != None):
            filters = [ FilterOptions('genre_id', self.movieEdit.genre_id) ]
            genre = self.list.genres.getByFilter(filters)

            self.name.set(self.movieEdit.name)
            self.image_path = self.movieEdit.image_path
            self.director.set(self.movieEdit.director)
            self.genre_id = self.movieEdit.genre_id
            self.genre.set(genre.list.data.name)
            self.producer.set(self.movieEdit.producer)
            self.rating.set(self.movieEdit.rating)
            self.length.set(int(self.movieEdit.length))

            
        self.vcmd = self.master.register(self.validateNumber)

        # create Movie main container
        self.frameMovies = Frame(self.master, bg='#ffffff')
        self.frameMovies.pack(fill='x', side='top', anchor='w', padx=30, pady=20)

        # create Title container
        self.frameTitle = Frame(self.frameMovies, bg='#ffffff')
        self.frameTitle.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        # create Title 
        title = Label(self.frameTitle, text='Agregar pelicula', font=('arial', 20,'normal'), bg='#ffffff', fg='#4267b2')
        title.pack(padx=0, pady=10, side='left', anchor='n')

        # create form 
        frameForm= Frame(self.frameMovies, bg='#ffffff', highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        frameForm.pack(padx=20, pady=20, side='left', anchor='n')

        frameFields = Frame(frameForm, bg='#ffffff')
        frameFields.pack(fill='x', side='top', anchor='w', padx=0, pady=10)

        labelName = Label(frameFields, text='Nombre:', font=('arial', 10,'normal'), bg='#ffffff', fg='#444444')
        labelName.pack(side='top', anchor='w', padx=20, pady=5)
        self.entryName = Entry(frameFields, width=70, relief='flat', textvariable=self.name, highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        self.entryName.pack(fill='x', padx=20, pady=5, ipady=3)

        # create Image fields
        frameImage = Frame(frameFields, bg='#ffffff')
        frameImage.pack(fill='x', side='top', anchor='w', padx=15, pady=5)

        frameAddImage= Frame(frameImage, bg='#ffffff', highlightthickness=2, highlightbackground='#ffffff', highlightcolor='#ffffff')
        frameAddImage.pack(padx=5, pady=0, side='left', anchor='n')
        buttonAddImage = Button(frameAddImage, font=('arial', 12,'normal'), text='Agregar imagen', bg='#11285b', relief='flat', activebackground='#11285b', fg='#ffffff', command=lambda: self.changeImage())
        buttonAddImage.pack()

        self.labelImage = Label(frameImage, text=self.image_path, font=('arial', 10,'normal'), bg='#ffffff', fg='#444444')
        self.labelImage.pack(side='left', anchor='n', padx=5, pady=10)

        labelDirector = Label(frameFields, text='Director:', font=('arial', 10,'normal'), bg='#ffffff', fg='#444444')
        labelDirector.pack(side='top', anchor='w', padx=20, pady=5)
        self.entryDirector = Entry(frameFields, width=70, relief='flat', textvariable=self.director, highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        self.entryDirector.pack(fill='x', padx=20, pady=5, ipady=3)

        labelProducer = Label(frameFields, text='Productor:', font=('arial', 10,'normal'), bg='#ffffff', fg='#444444')
        labelProducer.pack(side='top', anchor='w', padx=20, pady=5)
        self.entryProducer = Entry(frameFields, width=70, relief='flat', textvariable=self.producer, highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        self.entryProducer.pack(fill='x', padx=20, pady=5, ipady=3)

        # create Fields Rate  
        frameGenreRate = Frame(frameFields, bg='#ffffff')
        frameGenreRate.pack(fill='x', side='top', anchor='w', padx=0, pady=0)

        titleRate = Label(frameGenreRate, text='Clasificación', justify=LEFT, font=('arial', 10,'normal'), bg='#ffffff', fg='#444444', width=25, anchor="w")
        titleRate.grid(row=0, column=0, padx=20, pady=5, sticky='w')

        titleGenre = Label(frameGenreRate, text='Genero', justify=LEFT, font=('arial', 10,'normal'), bg='#ffffff', fg='#444444', width=25, anchor="w")
        titleGenre.grid(row=0, column=1, padx=20, pady=5, sticky='w')

        self.comboBoxRate = TTK.Combobox(frameGenreRate, textvariable=self.rating, width=25)
        self.comboBoxRate['values'] = [
            '', 
            'AA',
            'A',
            'B',
            'B15',
            'C',
            'D'
        ]
        
        self.comboBoxRate.grid(row=1, column=0, padx=20, pady=5, sticky='we', ipady=3)

        # create Field Genre
        genreValues = ['']

        tempList = self.list.genres.list

        while (tempList):
            genreValues.append(tempList.data.name)
            
            tempList = tempList.next

        self.comboBoxGenre = TTK.Combobox(frameGenreRate, width=25, textvariable=self.genre)
        self.comboBoxGenre['values'] = genreValues
        self.comboBoxGenre.grid(row=1, column=1, padx=20, pady=5, sticky='we', ipady=3)

        # create Field Length
        labelLength = Label(frameGenreRate, text='Duración:', font=('arial', 10,'normal'), bg='#ffffff', fg='#444444', width=25, anchor="w")
        labelLength.grid(row=2, column=0, padx=20, pady=5, sticky='w')
        self.entryLength = Entry(frameGenreRate, width=25, relief='flat', textvariable=self.length, highlightthickness=1, highlightbackground='#aaaaaa', highlightcolor='#aaaaaa')
        self.entryLength.config(validate='all', validatecommand=(self.vcmd, '%P'))
        self.entryLength.grid(row=3, column=0, padx=20, pady=5, sticky='we', ipady=3)

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

        error = True if self.name.get() == '' else error
        error = True if self.image_path == '' else error
        error = True if self.director.get() == '' else error
        error = True if self.producer.get() == '' else error
        error = True if self.rating.get() == '' else error
        error = True if self.genre.get() == '' else error
        error = True if self.length.get() == '' else error

        if (error == False):
            filtersGenre = [ FilterOptions('name', self.genre.get()) ]
            genre = self.list.genres.getByFilter(filtersGenre)

            filtersMovie = [ FilterOptions('name', (None if self.movieEdit is None else self.name.get())) ]

            resultMovie: ListMovie= self.list.movies.getByFilter(filtersMovie)
            
            if (resultMovie.list == None or (True if self.movieEdit is None else (resultMovie.list.data.movie_id == self.movieEdit.movie_id))):
                if (self.movieEdit != None):
                    movie = Movie(
                        self.movieEdit.movie_id,
                        self.name.get(),
                        self.image_path,
                        self.director.get(),
                        genre.list.data.genre_id,
                        self.producer.get(),
                        self.rating.get(),
                        self.length.get()
                    )

                    self.list.movies.update(self.movieEdit.pos, movie)
                    self.goBack()
                else:
                    movie = Movie(
                        None,
                        self.name.get(),
                        self.image_path,
                        self.director.get(),
                        genre.list.data.genre_id,
                        self.producer.get(),
                        self.rating.get(),
                        self.length.get()
                    )

                    self.list.movies.insert(movie, True)
                    self.goBack()
            else:
                self.showError('La pelicula ' + self.name.get() + ' ya está registrado, por favor ingrese otro nombre')
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
        self.frameMovies.pack_forget()
        MoviesList.MoviesListView(self.master, self.list, self.userId)

    def validateNumber(self, value):
        if str.isdigit(value) or value == '':
            return True
        else:
            return False

    def generateId(self, size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def changeImage(self):
        Tk().withdraw()
        filename = askopenfilename()
        newFileName = './src/assets/billboard_images/' + self.generateId(10) + '.jpg'

        copyfile(filename, newFileName)

        self.image_path = newFileName
        self.labelImage.config(text=self.image_path)
