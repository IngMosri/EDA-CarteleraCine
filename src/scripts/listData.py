import time

from scripts.binaryTree import TreeNode
from models.users import *
from models.states import *
from models.cities import *
from models.genres import *
from models.movies import *
from models.screenMovie import *

class ListData():
    def __init__(self):
        self.userModel = UsersModel()
        self.users = ListUser()
        self.stateModel = StatesModel()
        self.states = ListState()
        self.cityModel = CitiesModel()
        self.cities = ListCity()
        self.genreModel = GenresModel()
        self.genres = ListGenre()
        self.movieModel = MoviesModel()
        self.movies = ListMovie()
        self.screenMovieModel = ScreenMoviesModel()
        self.screenMovies = ListScreenMovie()

    def getDatabaseData(self):
        # get Users data and put into a list
        users = self.userModel.getAll()
        state = self.stateModel.getAll()
        city = self.cityModel.getAll()
        genre = self.genreModel.getAll()
        movie = self.movieModel.getAll()
        screenMovie = self.screenMovieModel.getAll()

        for row in users:
            self.users.insert(row)
        for row in state:
            self.states.insert(row)
        for row in city:
            self.cities.insert(row)
        for row in genre:
            self.genres.insert(row)
        for row in movie:
            self.movies.insert(row)
        for row in screenMovie:
            self.screenMovies.insert(row)

    def backUpData(self):
        # get Users list and backup into database
        self.userModel.deleteAll()
        usersList = self.users.list

        if (usersList != None):
            while (1 == 1):
                self.userModel.create(usersList.data)

                if (usersList.next is None):
                    break
                else:
                    usersList = usersList.next

        # get Movies list and backup into database
        self.movieModel.deleteAll()
        moviesList = self.movies.list

        if (moviesList != None):
            while (1 == 1):
                self.movieModel.create(moviesList.data)

                if (moviesList.next is None):
                    break
                else:
                    moviesList = moviesList.next

        
        # get Screen Movies list and backup into database
        self.screenMovieModel.deleteAll()
        screenMoviesList = self.screenMovies.list

        if (screenMoviesList != None):
            while (1 == 1):
                self.screenMovieModel.create(screenMoviesList.data)

                if (screenMoviesList.next is None):
                    break
                else:
                    screenMoviesList = screenMoviesList.next

listData = ListData()
listData.getDatabaseData()

treeStates = TreeNode()

# # filteredData = listData.users.getByFilter('user_name', 'john.doe')

# # time.sleep(5)

# tempList = listData.cities.list

# while(True):
#     treeStates.insert('name', tempList.data)

#     if (tempList.next is None):
#         break
#     else:
#         tempList = tempList.next

# orderedStatesASC = treeStates.inorder([])

# print('\n\n********** Lista orden ASC **********')
# for row in orderedStatesASC:
#     print(f'{row.city_id} - {row.name}')

# orderedStatesDESC = treeStates.inorder([], False)

# print('\n\n********** Lista orden DESC **********')
# for row in orderedStatesDESC:
#     print(f'{row.city_id} - {row.name}')
# listData.backUpData()
