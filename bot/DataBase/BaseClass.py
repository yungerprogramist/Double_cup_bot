import sqlite3



class BaseDB:

    def __init__(self) -> None:
        db = sqlite3.connect('project.db') 
        self.sql = db.cursor()
        self.db = db 
        


    def create_user_db(self):

        self.sql.execute('''CREATE TABLE IF NOT EXISTS "users" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "username"  TEXT UNIQUE,
            "chat_id" INTEGER UNIQUE
        )''')
        self.db.commit()
        self.sql.close()


    def create_categories_db(self):

        self.sql.execute('''CREATE TABLE IF NOT EXISTS "categories" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "category" TEXT
        )''')
        self.db.commit()
        self.sql.close()


    def create_offer_db(self):

        self.sql.execute('''CREATE TABLE IF NOT EXISTS "offer" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "category_id" TEXT, 
            "name" TEXT UNIQUE,
            "description" TEXT,
            "photo" TEXT
        )''')
        self.db.commit()
        self.sql.close()


    def create_messages_db(self):

        self.sql.execute('''CREATE TABLE IF NOT EXISTS "messages" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "name" TEXT,
            "text" TEXT,
            "photo" TEXT
        )''')
        self.db.commit()
        self.sql.close()

