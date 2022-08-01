import sqlite3

from scripts.filterOptions import FilterOptions


class Movie:
    def __init__(
        self,
        movie_id=None,
        name=None,
        image_path=None,
        director=None,
        genre_id=None,
        producer=None,
        rating=None,
        length=None,
        is_active=1
    ):
        self.pos = None
        self.movie_id = movie_id
        self.name = name
        self.image_path = image_path
        self.director = director
        self.genre_id = genre_id
        self.producer = producer
        self.rating = rating
        self.length = length
        self.is_active = is_active

    def __getitem__(self, key):
        return getattr(self, key)


class NodeMovie:
    def __init__(self, data=None, prev=None, next=None):
        self.data: Movie = data
        self.prev: NodeMovie = prev
        self.next: NodeMovie = next


class ListMovie:
    def __init__(self):
        self.list: NodeMovie = None

    def getList(self):
        return self.list

    def getByFilter(self, filters):
        filteredData = ListMovie()

        tempList = self.list
        count = 0

        while(True):
            validations = []

            for filter in filters:
                if (filter.exact == True):
                    validations.append(filter.value == tempList.data[filter.key])
                else:
                    validations.append(filter.value.lower() in tempList.data[filter.key].lower())

            if (False not in validations):
                tempList.data.pos = count
                filteredData.insert(tempList.data)

            if (tempList == None or tempList.next is None):
                break
            else:
                count += 1
                tempList = tempList.next

        return filteredData

    def insert(self, data: Movie, autoInc = False):
        def insertValue(tempList: NodeMovie):
            if (tempList is None):
                if (autoInc):
                    data.movie_id = 1
                newList = NodeMovie(data)
                return newList
            if (tempList.next is None):
                if (autoInc):
                    data.movie_id = tempList.data.movie_id + 1
                newList = NodeMovie(data, tempList)
                tempList.next = newList
                return tempList
            else:
                tempList.next = insertValue(tempList.next)
                return tempList

        self.list = insertValue(self.list)

    def update(self, pos: int, data: Movie):
        def updateValue(tempList: NodeMovie, tempPos: int, pos: int, data: Movie):
            if (tempList is None):
                return tempList
            else:
                if (tempPos == pos):
                    tempList.data = data
                    return tempList
                else:
                    tempList.next = updateValue(tempList.next, tempPos + 1, pos, data)
                    return tempList
        
        self.list = updateValue(self.list, 0, pos, data)

    def delete(self, pos: int):
        def deleteValue(tempList: NodeMovie, tempPos: int):
            if (tempList is None):
                return tempList
            else:
                if (tempPos == pos):
                    if (tempList.prev == None):
                        newList = tempList.next
                        newList.prev = None

                        return newList
                    else:
                        newList = tempList.next
                        newList.prev = tempList.prev

                        return newList
                elif (tempPos + 1 == pos and tempList.next.next == None):
                    tempList.next = None

                    return tempList
                else:
                    tempList.next = deleteValue(tempList.next, tempPos + 1)
                    return tempList

        self.list = deleteValue(self.list, 0)


class MoviesModel:
    def __init__(self):
        self.table = 'movie'
        self.database = 'cinema.db'

    def getAll(self):
        # create DB connection
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            result = cursor.execute(f'SELECT * FROM ' + self.table).fetchall()

            if (result):
                conn.close()
                data = []

                for i, row in enumerate(result):
                    data.insert(i, Movie(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))

                return data
            else:
                conn.close()
                return []
        except:
            conn.close()
            return []

    def create(self, user: Movie):
        # create DB connection
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            result = cursor.execute('INSERT INTO ' + self.table + ' (' + ('movie_id, ' if user.movie_id != None else '') + 'name, image_path, director, genre_id, producer, rating, length, is_active) VALUES (' + (':movie_id, ' if user.movie_id != None else '') + ':name, :image_path, :director, :genre_id, :producer, :rating, :length, :is_active)',  {'movie_id': user.movie_id, 'name': user.name, 'image_path': user.image_path, 'director': user.director, 'genre_id': user.genre_id, 'producer': user.producer, 'rating': user.rating, 'length': user.length, 'is_active': user.is_active})
            conn.commit()

            if (result):
                return True
            else:
                conn.close()
                return None
        except:
            conn.close()
            return None

    def deleteAll(self):
        # create DB connection
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            result = cursor.execute('DELETE FROM ' + self.table + ' WHERE 1 = 1')
            conn.commit()

            if (result):
                return True
            else:
                conn.close()
                return None
        except:
            conn.close()
            return None
