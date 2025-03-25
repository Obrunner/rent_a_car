import sqlite3
import os
import threading
from concurrent.futures import ThreadPoolExecutor


lock = threading.Lock()

class DatabaseConnector():
    DATABASE_NAME = 'example.db'

    def __init__(self):
        self._conn = sqlite3.connect('instance/' + DatabaseConnector.DATABASE_NAME, check_same_thread=False)
        self._cursor = self._conn.cursor()
        self._setupTables()

    def __del__(self):
        self._conn.close()

    def _setupTables(self):
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
        ''')
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS cars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                km INTEGER NOT NULL
            );
        ''')
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS rental_agreements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                km_allowance INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                car_id INTEGER NOT NULL,
                is_open INTEGER NOT NULL,
                FOREIGN KEY(customer_id) REFERENCES customers(id),
                FOREIGN KEY(car_id) REFERENCES cars(id)
            );
        ''')

    def _thread_safe_executeSELECT(self, query):
        with lock:
            self._cursor.execute(query)
            return self._cursor.fetchall()


    def executeSELECT(self, sql_statement):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(self._thread_safe_executeSELECT, sql_statement)
            result = future.result()
            return result
        
    def _thread_safe_executeChanges(self, sql_statement):
        with lock:
            self._cursor.execute(sql_statement)
            self._conn.commit()
    
    def executeChanges(self, sql_statement):
        with ThreadPoolExecutor() as executor:
            future = executor.submit(self._thread_safe_executeChanges, sql_statement)
            future.result()