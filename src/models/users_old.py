import sqlite3

class User:
    def __init__(
        self,
        user_id=None,
        user_name=None,
        password=None,
        is_active=None,
        create_at=None,
        update_at=None,
    ):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        self.is_active = is_active
        self.create_at = create_at
        self.update_at = update_at


class UsersModel:
    def __init__(self):
        self.table = 'user'

    def getOneByUserPass(self, user, password):
        # create DB connection
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()

        try:
            result = cursor.execute('SELECT * FROM ' + self.table + ' WHERE is_active = 1 AND user_name = :user_name AND password = :password', {'user_name': user, 'password': password}).fetchone()

            if (result):
                conn.close()
                return User(result[0], result[1], result[2], result[3], result[4], result[5])
            else:
                conn.close()
                return None
        except:
            conn.close()
            return None

    def getOneByUser(self, user, userId):
        # create DB connection
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()

        try:
            result = cursor.execute('SELECT * FROM ' + self.table + ' WHERE is_active = 1 AND user_name = :user_name' + ('' if userId is None else ' AND user_id != :user_id' ), {'user_name': user, 'user_id': userId}).fetchone()

            if (result):
                conn.close()
                return User(result[0], result[1], result[2], result[3], result[4], result[5])
            else:
                conn.close()
                return None
        except:
            conn.close()
            return None

    def getAll(self):
        # create DB connection
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()

        try:
            result = cursor.execute('SELECT * FROM ' + self.table).fetchall()

            if (result):
                conn.close()
                data = []

                for i, row in enumerate(result):
                    data.insert(i, User(row[0], row[1], row[2], row[3], row[4], row[5]))

                return data
            else:
                conn.close()
                return None
        except:
            conn.close()
            return None

    def create(self, user: User):
        # create DB connection
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()

        try:
            result = cursor.execute('INSERT INTO ' + self.table + ' (user_name, password, is_active) VALUES (:user_name, :password, :is_active)',  {'user_name': user.user_name, 'password': user.password, 'is_active': user.is_active})
            conn.commit()
            
            if (result):
                return True
            else:
                conn.close()
                return None
        except:
            conn.close()
            return None
    
    def update(self, user: User):
        # create DB connection
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()

        try:
            result = cursor.execute('UPDATE ' + self.table + ' SET user_name = :user_name, password = :password, is_active = :is_active WHERE user_id = :user_id',  {'user_name': user.user_name, 'password': user.password, 'is_active': user.is_active, 'user_id': user.user_id})
            conn.commit()
            
            if (result):
                return True
            else:
                conn.close()
                return None
        except:
            conn.close()
            return None

    def delete(self, userId):
        # create DB connection
        conn = sqlite3.connect('cinema.db')
        cursor = conn.cursor()

        try:
            result = cursor.execute('DELETE FROM ' + self.table + ' WHERE user_id = :user_id',  {'user_id': userId})
            conn.commit()
            
            if (result):
                return True
            else:
                conn.close()
                return None
        except:
            conn.close()
            return None