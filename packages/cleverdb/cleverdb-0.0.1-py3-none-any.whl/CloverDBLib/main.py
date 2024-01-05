import sqlite3
import json

class CloverDBError(sqlite3.OperationalError):
    pass

class CloverDB:
    def __init__(self, db_name='cloverdb.db'):
        """
        Инициализация объекта CloverDB.

        Параметры:
        - db_name (строка): Имя базы данных. По умолчанию 'cloverdb.db'.
        """
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def connect(self, db_name=None):
        """
        Установление соединения с базой данных.

        Параметры:
        - db_name (строка): Имя базы данных. Если не указано, используется db_name из конструктора.

        Возвращает:
        - connection (объект): Объект соединения с базой данных.
        """
        if db_name is None:
            db_name = self.db_name

        try:
            self.connection = sqlite3.connect(db_name)
            self.cursor = self.connection.cursor()
            print("Connected to the database.")
            return self.connection
        except sqlite3.OperationalError as e:
            raise CloverDBError(f"Error connecting to the database: {e}")

    def select(self, select, from_table, where=None):
        """
        Выполнение SELECT-запроса к базе данных.

        Параметры:
        - select (строка): Столбцы, которые следует выбрать.
        - from_table (строка): Имя таблицы, из которой следует выбрать данные.
        - where (словарь): Условия WHERE в виде словаря.

        Возвращает:
        - result (список): Список словарей с результатами запроса.
        """
        query = f"SELECT {select} FROM {from_table}"
        if where:
            where_condition = ' AND '.join([f"{column} = '{value}'" for column, value in where.items()])
            query += f" WHERE {where_condition}"
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except sqlite3.OperationalError as e:
            raise CloverDBError(f"Error executing SELECT query: {e}")

    def create_table(self, table_name, columns):
        """
        Создание таблицы в базе данных.

        Параметры:
        - table_name (строка): Имя таблицы.
        - columns (словарь): Словарь с определением столбцов и их типов.

        Возвращает:
        - query (строка): SQL-запрос для создания таблицы.
        """
        column_definitions = ', '.join([f"{name} {datatype}" for name, datatype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            raise CloverDBError(f"Error executing CREATE TABLE query: {e}")

    def insert(self, table_name, values):
        """
        Вставка новой записи в таблицу.

        Параметры:
        - table_name (строка): Имя таблицы.
        - values (словарь): Словарь с данными для вставки.

        Возвращает:
        - query (строка): SQL-запрос для вставки данных.
        """
        column_names = ', '.join(values.keys())
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        try:
            self.cursor.execute(query, tuple(values.values()))
            self.connection.commit()
        except sqlite3.OperationalError as e:
            raise CloverDBError(f"Error executing INSERT query: {e}")

    def update(self, table_name, set_values, where=None):
        """
        Обновление данных в таблице.

        Параметры:
        - table_name (строка): Имя таблицы.
        - set_values (словарь): Словарь с новыми значениями для обновления.
        - where (словарь): Условия WHERE в виде словаря.

        Возвращает:
        - query (строка): SQL-запрос для обновления данных.
        """
        set_clause = ', '.join([f"{column} = ?" for column in set_values.keys()])
        where_condition = ''
        if where:
            where_condition = ' WHERE ' + ' AND '.join([f"{column} = '{value}'" for column, value in where.items()])
        query = f"UPDATE {table_name} SET {set_clause}{where_condition}"
        try:
            self.cursor.execute(query, tuple(set_values.values()))
            self.connection.commit()
        except sqlite3.OperationalError as e:
            raise CloverDBError(f"Error executing UPDATE query: {e}")

    def delete(self, table_name, where=None):
        """
        Удаление данных из таблицы.

        Параметры:
        - table_name (строка): Имя таблицы.
        - where (словарь): Условия WHERE в виде словаря.

        Возвращает:
        - query (строка): SQL-запрос для удаления данных.
        """
        where_condition = ''
        if where:
            where_condition = ' WHERE ' + ' AND '.join([f"{column} = '{value}'" for column, value in where.items()])
        query = f"DELETE FROM {table_name}{where_condition}"
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            raise CloverDBError(f"Error executing DELETE query: {e}")

    def execute_custom_query(self, params):
        """
        Выполнение произвольного SQL-запроса с использованием параметров в виде словаря.

        Параметры:
        - params (словарь): Словарь с параметрами запроса.

        Возвращает:
        - result (список): Список словарей с результатами запроса.
        """
        table_name = params['table']
        where_conditions = params.get('where', {})
        
        where_condition = ''
        if where_conditions:
            where_condition = ' WHERE ' + ' AND '.join([f"{column} {operator} {json.dumps(value)}" for column, condition in where_conditions.items() for operator, value in condition.items()])
        
        query = f"SELECT * FROM {table_name}{where_condition}"

        try:
            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            result = [dict(zip(columns, row)) for row in self.cursor.fetchall()]
            return result
        except sqlite3.OperationalError as e:
            raise CloverDBError(f"Error executing custom query: {e}")

    def close(self):
        """
        Закрытие соединения с базой данных.
        """
        if self.connection:
            self.connection.close()
            print("Connection closed.")
