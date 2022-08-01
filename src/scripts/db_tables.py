import sqlite3

# Define connection and cursor
conn = sqlite3.connect('cinema.db')
cursor = conn.cursor()

# Users Table
cursor.execute(""" CREATE TABLE IF NOT EXISTS
    user(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        password TEXT NOT NULL,
        is_active INTEGER DEFAULT 1 NOT NULL,
        create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

# States Table
cursor.execute(""" CREATE TABLE IF NOT EXISTS
    state(
        state_id INTEGER PRIMARY KEY AUTOINCREMENT,
        state_code TEXT NOT NULL,
        name TEXT NOT NULL,
        is_active INTEGER DEFAULT 1 NOT NULL,
        create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

# Cities Table
cursor.execute(""" CREATE TABLE IF NOT EXISTS
    city(
        city_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city_code TEXT NOT NULL,
        name TEXT NOT NULL,
        is_active INTEGER DEFAULT 1 NOT NULL,
        create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        state_id INTEGER,
        FOREIGN KEY(state_id) REFERENCES state(state_id)
    )""")

# Screen Table / Tabla para las salas del cine
cursor.execute(""" CREATE TABLE IF NOT EXISTS
    screen(
        screen_id INTEGER PRIMARY KEY AUTOINCREMENT,
        screen_number INTEGER NOT NULL,
        city_id INTEGER,
        is_active INTEGER DEFAULT 1 NOT NULL,
        create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(city_id) REFERENCES city(city_id)
    )""")

# Table for relationship between movies and screens. So we can delete a movie from a specific city/screen
# without deleting it from another city/screen
cursor.execute(""" CREATE TABLE IF NOT EXISTS
    screen_movie(
        screen_id INTEGER,
        movie_id INTEGER,
        movie_time TIME NOT NULL,
        is_active INTEGER DEFAULT 1 NOT NULL,
        create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(screen_id) REFERENCES screen(screen_id),
        FOREIGN KEY(movie_id) REFERENCES movie(movie_id)
    )""")

# Movies Table
cursor.execute(""" CREATE TABLE IF NOT EXISTS
    movie(
        movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        director TEXT,
        producer TEXT,
        rating TEXT,
        length FLOAT NOT NULL,
        is_active INTEGER DEFAULT 1 NOT NULL,
        create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        genre_id INTEGER,
        FOREIGN KEY(genre_id) REFERENCES genre(genre_id)
    )""")

# Genres Table
cursor.execute(""" CREATE TABLE IF NOT EXISTS
    genre(
        genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        is_active INTEGER DEFAULT 1 NOT NULL,
        create_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        update_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")

# cursor.execute('drop table city')

# cursor.execute("SELECT user_id FROM user WHERE user_name = 'abc' ")
# print(cursor.fetchall())
# query = cursor.fetchone()[0]
# print(query)

# region Users
# ================ USERS DEFAULT DATA================
# cursor.execute("INSERT INTO user(user_name, password)"
#                "VALUES('john.doe', '123')")
# endregion
# region States
# ================ STATES DEFAULT DATA================
# cursor.execute("INSERT INTO city(city_code, name)"
#                "VALUES('J11', 'Guadalajara')")
# cursor.execute("INSERT INTO city(city_code, name)"
#                "VALUES('N11', 'Nuevo Leon')")
# cursor.execute("INSERT INTO city(city_code, name)"
#                "VALUES('E11', 'Estado de Mexico')")
# cursor.execute("INSERT INTO city(city_code, name)"
#                "VALUES('C11', 'Chihuahua')")
# cursor.execute("INSERT INTO city(city_code, name)"
#                "VALUES('S11', 'Sinaloa')")
# endregion
# region Cities
# ================ CITIES DEFAULT DATA================

# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('A', 'Guadalajara', 1)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('B', 'Zapopan', 1)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('C', 'Tlaquepaque', 1)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('D', 'Tonala', 1)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('E', 'Zapotlanejo', 1)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('F', 'Tlajomulco', 1)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('G', 'Ayotlan', 1)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('H', 'Tequila', 1)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('I', 'Ocotlan', 1)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('J', 'Puerto Vallarta', 1)")

# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('A', 'Guadalupe', 2)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('B', 'Abasolo', 2)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('C', 'Apodaca', 2)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('D', 'Cienega de Flores', 2)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('E', 'General Zaragoza', 2)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('F', 'Iturbide', 2)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('G', 'Juarez', 2)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('H', 'Monterrey', 2)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('I', 'Salinas Victoria', 2)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('J', 'General Zuazua', 2)")

# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('A', 'Cuautitlan Izcalli', 3)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('B', 'Chalco', 3)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('C', 'Aculco', 3)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('D', 'Atizapan', 3)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('E', 'Chapultepec', 3)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('F', 'Ecatepec de Morelos', 3)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('G', 'Naucalpan de Juarez', 3)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('H', 'Morelos', 3)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('I', 'Texcoco', 3)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('J', 'Toluca', 3)")

# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('A', 'Ignacio de Zaragoza', 4)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('B', 'Allende', 4)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('C', 'Valle de Zaragoza', 4)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('D', 'Rosario', 4)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('E', 'Nonoava', 4)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('F', 'Matamoros', 4)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('G', 'Guadalupe y Calvo', 4)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('H', 'Coronado', 4)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('I', 'Delicias', 4)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('J', 'Galeana', 4)")

# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('A', 'Guasave', 5)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('B', 'Navolato', 5)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('C', 'Cosala', 5)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('D', 'Angostura', 5)")
# cursor.execute("INSERT INTO city(city_code, name, state_id)"
#                "VALUES('E', 'Mocorito', 5)")

# endregion

# cursor.execute("Delete from city")
# cursor.execute("select * from city WHERE state_id=5")
print(cursor.fetchall())

conn.commit()
conn.close()
