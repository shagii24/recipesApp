import sqlite3
from sqlite3 import Error
import traceback

class dbConnection():
    def __init__(self,path):
        self.path = path
    def connect(self):
        connection = None
        try:
            connection = sqlite3.connect(self.path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection
    def execute_read_query(self,query):
        cursor = self.connect().cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
    
    def execute_read_query_json(self,query):
        cursor = self.connect().cursor()
        result = None
        try:
            cursor.execute(query)
            result = [dict((cursor.description[i][0], value) \
               for i, value in enumerate(row)) for row in cursor.fetchall()]
            cursor.close()
  
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_query(self, query):
        connection = self.connect()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
            cursor.close()
        except Error as e:
            print(f"The error '{e}' occurred")

