import psycopg2
from faker import Faker

# Параметри підключення до бази даних
DB_NAME = "DB2"
DB_USER = "god_it"
DB_PASSWORD = "5344166"
DB_HOST = "localhost"
DB_PORT = "5432"  # Порт за замовчуванням для PostgreSQL

def seed_database():
    """Наповнення таблиць даними."""
    fake = Faker()

    try:
        # Підключення до бази даних
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Вставка фіктивних даних у таблиці
        for _ in range(10):
            fullname = fake.name()
            email = fake.email()
            cursor.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

        for status in ['new', 'in progress', 'completed']:
            cursor.execute("INSERT INTO status (name) VALUES (%s)", (status,))

        for _ in range(10):
            title = fake.sentence()
            description = fake.paragraph()
            status_id = fake.random_int(min=1, max=3)
            user_id = fake.random_int(min=1, max=10)
            cursor.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
                           (title, description, status_id, user_id))

        cursor.close()
        conn.close()
        print("Дані успішно вставлені в таблиці!")
    except Exception as e:
        print("Сталася помилка при вставці даних в таблиці:", e)

# Виклик функції для наповнення таблиць даними
seed_database()
