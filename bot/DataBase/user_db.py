import sqlite3
from bot.DataBase.BaseClass import BaseDB



class UserDB(BaseDB):
    __name_table = 'users'


    def start_db(self, username: str, chat_id: int) ->None:
        """Заполняет информацию о пользователе, который нажал start,  в бд"""
        db = None
        try: 

            if not (self.sql.execute(f'SELECT EXISTS(SELECT * FROM {self.__name_table} WHERE username ="{username}")').fetchone()[0]): #проверка на наличие пользователя в бд
                self.sql.execute(f'INSERT INTO {self.__name_table} (username, chat_id) VALUES ("{username}", "{chat_id}")')

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
        finally: 
            self.db.commit()
            if db: self.db.close()

    
