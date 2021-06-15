import sqlite3

Create_table = """CREATE TABLE IF NOT EXISTS bookmarks
(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
url TEXT NOT NULL,
NOT NULL requires a column
notes TEXT,
date_added TEXT NOT NULL
);"""


class DatabaseManager:
    def __init__(self, database_filename):
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement, values=None):
        with self.connection:
            cursor=self.connection.cursor()
            cursor.execute(statement, values or [])
            return cursor

    def create_table(self, table_name, columns):
        columns_with_types=[
            with their data types and constraints
            f'{column_name} {data_type}'
            for column_name, data_type in columns.items()
        ]
        self._execute(
            f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({', '.join(columns_with_types)});
            '''
            )
    
    def add(self, table_name, data):
        placeholder = ', '.join('?' * len( data ))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())

        self._execute(
            f'''
            INSERT INTO {table_name}
            ({ column_names })
            VALUES ({placeholder});
            ''',
            column_values
        )

