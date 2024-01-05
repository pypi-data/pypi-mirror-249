## CloverDB - Database

# CloverDB - Простая обертка для работы с SQLite в Python

CloverDB - это простой класс для работы с базой данных SQLite в приложениях Python. Ниже представлено описание каждой функции класса и примеры использования.

# Установка библиотеки

```sh
pip install cloverdb
```

## Использование

1. **`__init__(self, db_name='cloverdb.db')`**
    - Инициализация объекта CloverDB с указанием имени базы данных (по умолчанию 'cloverdb.db').

2. **`connect(self, db_name=None)`**
    - Метод подключения к базе данных.
    - Принимает опциональный параметр `db_name`, указывающий на имя базы данных.
    - Пример использования:
        ```python
        clover_db = CloverDB()
        connection = clover_db.connect('custom_db.db')
        ```

3. **`select(self, select, from_table, where=None)`**
    - Метод для выполнения запроса SELECT к базе данных.
    - Принимает параметры `select` (колонки для выбора), `from_table` (название таблицы) и опциональный параметр `where` (условие WHERE в виде словаря).
    - Возвращает результат запроса.
    - Пример использования:
        ```python
        result = clover_db.select(select='userid', from_table='giveusers', where={'column_name': 'value'})
        print(result)
        ```

4. **`create_table(self, table_name, columns)`**
    - Метод для создания таблицы в базе данных.
    - Принимает параметры `table_name` (название таблицы) и `columns` (словарь с описанием столбцов и их типов).
    - Пример использования:
        ```python
        clover_db.create_table(table_name='users', columns={'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT'})
        ```

5. **`insert(self, table_name, values)`**
    - Метод для вставки данных в таблицу.
    - Принимает параметры `table_name` (название таблицы) и `values` (словарь с данными для вставки).
    - Пример использования:
        ```python
        clover_db.insert(table_name='example_table', values={'id': 1, 'name': 'John Doe'})
        ```

6. **`update(self, table_name, set_values, where=None)`**
    - Метод для обновления данных в таблице.
    - Принимает параметры `table_name` (название таблицы), `set_values` (словарь с данными для обновления) и опциональный параметр `where` (условие WHERE в виде словаря).
    - Пример использования:
        ```python
        clover_db.update(table_name='example_table', set_values={'name': 'Jane Doe'}, where={'id': 1})
        ```

7. **`delete(self, table_name, where=None)`**
    - Метод для удаления данных из таблицы.
    - Принимает параметры `table_name` (название таблицы) и опциональный параметр `where` (условие WHERE в виде словаря).
    - Пример использования:
        ```python
        clover_db.delete(table_name='example_table', where={'id': 1})
        ```

8. **`execute_custom_query(self, custom_query)`**
    - Метод для выполнения произвольного SQL-запроса.
    - Принимает параметр `custom_query` (строка с SQL-запросом).
    - Возвращает результат выполнения запроса.
    - Пример использования:
        ```python
        result = clover_db.execute_custom_query("SELECT * FROM example_table WHERE age > 20")
        print(result)
        ```

9. **`close(self)`**
    - Метод закрытия соединения с базой данных.

## Пример использования:

```python
# Создаем объект CloverDB
import cloverdb

# Подключаемся к базе данных
connection = clover_db.connect('custom_db.db')
cursor = connection.cursor()

# Выполняем запрос SELECT
try:
    select_query = clover_db.select(select='userid', from_table='giveusers', where={'column_name': 'value'})
    print(select_query)
except CloverDBError as e:
    print(e)

# Создаем таблицу
try:
    create_table_query = clover_db.create_table(table_name='example_table', columns={'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT'})
    print(create_table_query)
except CloverDBError as e:
    print(e)

# Вставляем данные
try:
    insert_query = clover_db.insert(table_name='example_table', values={'id': 1, 'name': 'John Doe'})
    print(insert_query)
except CloverDBError as e:
    print(e)

# Обновляем данные
try:
    update_query = clover_db.update(table_name='example_table', set_values={'name': 'Jane Doe'}, where={'id': 1})
    print(update_query)
except CloverDBError as e:
    print(e)

# Удаляем данные
try:
    delete_query = clover_db.delete(table_name='example_table', where={'id': 1})
    print(delete_query)
except CloverDBError as e:
    print(e)

# Выполняем произвольный запрос
try:
    custom_query_result = clover_db.execute_custom_query("SELECT * FROM example_table WHERE age > 20")
    print(custom_query_result)
except CloverDBError as e:
    print(e)

# Закрываем соединение
clover_db.close()
```
