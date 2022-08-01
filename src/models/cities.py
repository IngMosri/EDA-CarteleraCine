import sqlite3

from scripts.filterOptions import FilterOptions

class City:
    def __init__(
        self,
        city_id=None,
        city_code=None,
        name=None,
        state_id=None,
        is_active=1
    ):
        self.city_id = city_id
        self.city_code = city_code
        self.name = name
        self.state_id = state_id
        self.is_active = is_active

    def __getitem__(self, key):
        return getattr(self, key)

class NodeCity:
    def __init__(self, data = None, prev = None, next = None):
        self.data: City = data
        self.prev: NodeCity = prev
        self.next: NodeCity = next

class ListCity:
    def __init__(self):
        self.list: NodeCity = None

    def getList(self):
        return self.list

    def getByFilter(self, filters):
        filteredData = ListCity()

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

    def insert(self, data: City):
        def insertValue(tempList: NodeCity):
            if (tempList is None):
                newList = NodeCity(data)
                return newList
            if (tempList.next is None):
                newList = NodeCity(data, tempList)
                tempList.next = newList
                return tempList
            else:
                tempList.next = insertValue(tempList.next)
                return tempList

        self.list = insertValue(self.list)

    def update(self, pos: int, data: City):
        def updateValue(tempList: NodeCity, tempPos: int):
            if (tempList is None):
                return tempList
            else:
                if (tempPos == pos):
                    tempList.data = data
                    return tempList
                else:
                    tempList.next = updateValue(tempList.next, tempPos + 1)
                    return tempList

    def delete(self, pos: int):
        def deleteValue(tempList: NodeCity, tempPos: int):
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

class CitiesModel:
    def __init__(self):
        self.table = 'city'
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
                    data.insert(i, City(row[0], row[1], row[2], row[3], row[4]))

                return data
            else:
                conn.close()
                return []
        except:
            conn.close()
            return []

    def create(self, user: City):
        # create DB connection
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            result = cursor.execute('INSERT INTO ' + self.table + ' (' + ('city_id, ' if user.city_id != None else '') + 'city_code, name, state_id, is_active) VALUES (' + (':city_id, ' if user.city_id != None else '') + ':city_code, :name, :state_id, :is_active)',  {'city_id': user.city_id, 'city_code': user.city_code, 'name': user.name, 'state_id': user.state_id, 'is_active': user.is_active})
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