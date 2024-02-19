import sqlite3
from bot.DataBase.BaseClass import BaseDB



class OfferDB(BaseDB):
    __name_table = 'offer'


    def get_services_for_category(self, category_id: str )->list:
        """Возвращает услуги заданной категории"""
        db = None
        try: 

            data = self.sql.execute(f'SELECT name FROM {self.__name_table} WHERE category_id = "{category_id}"').fetchall()

            service_list = []
            for i in data:
                service_list.append(i[0])
            return service_list

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
        finally: 
            self.db.commit()
            if db: self.db.close()

    def get_info_service(self, name: str) ->tuple:
        """Возвращает информацию из бд о услуге [имя, описание, категория_id, файл]"""
        db = None
        try: 

            data = self.sql.execute(f'SELECT name, description, category_id, file_id FROM {self.__name_table} WHERE name = "{name}"').fetchall()

            return data[0]

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
            return False
        finally: 
            self.db.commit()
            if db: self.db.close()


    def add_service(self, category_id: str, name: str, description: str, photo: str = None)-> bool:
        """Добавляет услугу"""
        db = None
        try: 

            self.sql.execute(f'INSERT INTO {self.__name_table} (category_id, name, description, photo) VALUES ("{category_id}", "{name}", "{description}", "{photo}")')
            return True

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
            return False

        finally: 
            self.db.commit()
            if db: self.db.close()


    def delete_servise(self, name: str) ->bool:
        """Удаляет услугу"""
        db = None
        try: 

            self.sql.execute(f'DELETE FROM {self.__name_table} WHERE name = "{name}"')
            return True 
            

        except sqlite3.Error as ex:
            if db: self.db.rollback() 
            print (f'Упс что то пошло не так с базой данных - {ex}') 
            return False
        finally: 
            self.db.commit()
            if db: self.db.close()