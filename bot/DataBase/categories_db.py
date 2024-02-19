import sqlite3
from bot.DataBase.BaseClass import BaseDB



class CategoriesDB(BaseDB):
    __name_table = 'categories'



    def get_categories_list(self):
        """Возвращает список категорий"""
        db = None
        try: 

            data = self.sql.execute(f'SELECT category FROM {self.__name_table}').fetchall()

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


    def get_id_category(self, category: str) ->int:
        """Возвращает id категории"""
        db = None
        try: 

            data = self.sql.execute(f'SELECT id FROM {self.__name_table} WHERE category = "{category}"').fetchone()
            return int(data[0])

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
        finally: 
            self.db.commit()
            if db: self.db.close()


    def add_category(self, name:str) -> bool:
        """Добавляет категорию"""
        db = None
        try: 

            self.sql.execute(f'INSERT INTO {self.__name_table} (category) VALUES ("{name}")')
            return True

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
            return False
        finally: 
            self.db.commit()
            if db: self.db.close()
    

    def dell_category(self, name: str)-> bool:
        """Добавляет категорию"""
        db = None
        try: 

            self.sql.execute(f'DELETE FROM {self.__name_table} WHERE category = "{name}"')
            return True

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
            return False
        finally: 
            self.db.commit()
            if db: self.db.close()
    
