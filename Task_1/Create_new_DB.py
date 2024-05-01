import psycopg2
from psycopg2 import sql

# Параметри підключення до бази даних
DB_NAME = "DB2"
DB_USER = "god_it"
DB_PASSWORD = "5344166"
DB_HOST = "localhost"
DB_PORT = "5432"  # Порт за замовчуванням для PostgreSQL

# Запит для створення таблиці користувачів
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE
);
"""

# Запит для створення таблиці статусів
CREATE_STATUS_TABLE = """
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);
"""

# Запит для створення таблиці завдань
CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100),
    description TEXT,
    status_id INTEGER REFERENCES status(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
"""

def create_database():
    """Створення бази даних та таблиць."""
    try:
        # Підключення до бази даних 'postgres' з відключенням транзакцій
        conn = psycopg2.connect(dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB_NAME)))
        cursor.close()
        print("База даних створена")
    except Exception as e:
        print("Сталася помилка при створенні бази даних:", e)
        if conn:
            conn.close()
        return

    try:
        # Підключення до новоствореної бази даних 'DB2'
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(CREATE_USERS_TABLE)
        cursor.execute(CREATE_STATUS_TABLE)
        cursor.execute(CREATE_TASKS_TABLE)
        cursor.close()
        print("Таблиці успішно створені")
    except Exception as e:
        print("Сталася помилка при створенні таблиць:", e)
    finally:
        if conn:
            conn.close()

# Виклик функції для створення бази даних та таблиць
create_database()
