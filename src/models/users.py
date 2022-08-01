import sqlite3

from scripts.filterOptions import FilterOptions

class User:
    def __init__(
        self,
        user_id=None,
        user_name=None,
        password=None,
        is_active=1
    ):
        self.pos = None
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.is_active = is_active

    def __getitem__(self, key):
        return getattr(self, key)

class NodeUser:
    def __init__(self, data = None, prev = None, next = None):
        self.data: User = data
        self.prev: NodeUser = prev
        self.next: NodeUser = next

class ListUser:
    def __init__(self):
        self.list: NodeUser = None

    def getList(self):
        return self.list

    def getByFilter(self, filters):
        filteredData = ListUser()

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

    def insert(self, data: User, autoInc = False):
        def insertValue(tempList: NodeUser):
            if (tempList is None):
                if (autoInc):
                    data.user_id = 1
                newList = NodeUser(data)
                return newList
            if (tempList.next is None):
                if (autoInc):
                    data.user_id = tempList.data.user_id + 1
                newList = NodeUser(data, tempList)
                tempList.next = newList
                return tempList
            else:
                tempList.next = insertValue(tempList.next)
                return tempList

        self.list = insertValue(self.list)

    def update(self, pos: int, data: User):
        def updateValue(tempList: NodeUser, tempPos: int, pos: int, data: User):
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
        def deleteValue(tempList: NodeUser, tempPos: int):
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

class UsersModel:
    def __init__(self):
        self.table = 'user'
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
                    data.insert(i, User(row[0], row[1], row[2], row[3]))

                return data
            else:
                conn.close()
                return []
        except:
            conn.close()
            return []

    def create(self, user: User):
        # create DB connection
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            result = cursor.execute('INSERT INTO ' + self.table + ' (' + ('user_id, ' if user.user_id != None else '') + 'user_name, password, is_active) VALUES (' + (':user_id, ' if user.user_id != None else '') + ':user_name, :password, :is_active)',  {'user_id': user.user_id, 'user_name': user.user_name, 'password': user.password, 'is_active': user.is_active})
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