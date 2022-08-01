import sqlite3

from scripts.filterOptions import FilterOptions

class State:
    def __init__(
        self,
        state_id=None,
        state_code=None,
        name=None,
        is_active=1
    ):
        self.state_id = state_id
        self.state_code = state_code
        self.name = name
        self.is_active = is_active

    def __getitem__(self, key):
        return getattr(self, key)

class NodeState:
    def __init__(self, data = None, prev = None, next = None):
        self.data: State = data
        self.prev: NodeState = prev
        self.next: NodeState = next

class ListState:
    def __init__(self):
        self.list: NodeState = None

    def getList(self):
        return self.list

    def getByFilter(self, filters):
        filteredData = ListState()

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
        
    def insert(self, data: State):
        def insertValue(tempList: NodeState):
            if (tempList is None):
                newList = NodeState(data)
                return newList
            if (tempList.next is None):
                newList = NodeState(data, tempList)
                tempList.next = newList
                return tempList
            else:
                tempList.next = insertValue(tempList.next)
                return tempList

        self.list = insertValue(self.list)

    def update(self, pos: int, data: State):
        def updateValue(tempList: NodeState, tempPos: int):
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
        def deleteValue(tempList: NodeState, tempPos: int):
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

class StatesModel:
    def __init__(self):
        self.table = 'state'
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
                    data.insert(i, State(row[0], row[1], row[2], row[3]))

                return data
            else:
                conn.close()
                return []
        except:
            conn.close()
            return []

    def create(self, user: State):
        # create DB connection
        conn = sqlite3.connect(self.database)
        cursor = conn.cursor()

        try:
            result = cursor.execute('INSERT INTO ' + self.table + ' (' + ('state_id, ' if user.state_id != None else '') + 'state_code, name, is_active) VALUES (' + (':state_id, ' if user.state_id != None else '') + ':state_code, :name, :is_active)',  {'state_id': user.state_id, 'state_code': user.state_code, 'name': user.name, 'is_active': user.is_active})
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