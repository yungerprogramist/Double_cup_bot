import sqlite3
from bot.DataBase.BaseClass import BaseDB



class MessagesDB(BaseDB):
    __name_table = 'messages'



    def get_message(self, name: str)-> list:
        """Возвращает сообщение [text, photo])"""
        db = None
        try: 

            data = self.sql.execute(f'SELECT text, photo FROM {self.__name_table} WHERE name="{name}"').fetchall()

            chanel_list = []
            for i in data:
                chanel_list.append(i[0])
            return chanel_list

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
        finally: 
            self.db.commit()
            if db: self.db.close()


    def get_message_list(self):
        """Возвращает список сообщений ([name, text],[...], ...)"""
        db = None
        try: 

            data = self.sql.execute(f'SELECT name, text FROM {self.__name_table}').fetchall()

            chanel_list = []
            for i in data:
                chanel_list.append(i)
            return chanel_list

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
        finally: 
            self.db.commit()
            if db: self.db.close()


    def get_message_for_name(self, name) -> list:
        """Возвращает сообщение [text, photo]"""
        db = None
        try: 

            data = self.sql.execute(f'SELECT text, photo FROM {self.__name_table} WHERE name = {name}').fetchall()

            chanel_list = []
            for i in data:
                chanel_list.append(i)
            return chanel_list[0]

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
        finally: 
            self.db.commit()
            if db: self.db.close()

    
    def change_text_message(self, name, text):
        """изменяет текст сообщения"""
        db = None
        try: 

            self.sql.execute(f'UPDATE {self.__name_table} SET text = "{text}" WHERE name ="{name}"')

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
        finally: 
            self.db.commit()
            if db: self.db.close()
    

    def change_photo_message(self, name, photo):
        """изменяет текст сообщения"""
        db = None
        try: 

            self.sql.execute(f'UPDATE {self.__name_table} SET photo = "{photo}" WHERE name ="{name}"')

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
        finally: 
            self.db.commit()
            if db: self.db.close()


    