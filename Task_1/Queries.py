import psycopg2

# Параметри підключення до бази даних
DB_NAME = "DB2"
DB_USER = "god_it"
DB_PASSWORD = "5344166"
DB_HOST = "localhost"
DB_PORT = "5432"

# Функція для виконання SQL запитів
def execute_query(query, params=None):
    with psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description:
                return cursor.fetchall()  # Return the result for SELECT queries
            conn.commit()  # Commit the changes for INSERT, UPDATE, DELETE

# Запити
def get_tasks_by_user(user_id):
    return execute_query("SELECT * FROM tasks WHERE user_id = %s", (user_id,))

def get_tasks_by_status(status_name):
    return execute_query("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = %s)", (status_name,))

def update_task_status(task_id, new_status):
    execute_query("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s", (new_status, task_id))

def get_users_with_no_tasks():
    return execute_query("SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)")

def add_task_for_user(user_id, title, description):
    execute_query("INSERT INTO tasks (title, description, user_id) VALUES (%s, %s, %s)", (title, description, user_id))

def get_incomplete_tasks():
    return execute_query("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed')")

def delete_task(task_id):
    execute_query("DELETE FROM tasks WHERE id = %s", (task_id,))

def find_users_by_email(email_pattern):
    return execute_query("SELECT * FROM users WHERE email LIKE %s", (email_pattern,))

def update_user_name(user_id, new_name):
    execute_query("UPDATE users SET fullname = %s WHERE id = %s", (new_name, user_id))

def get_task_count_by_status():
    return execute_query("SELECT status.name, COUNT(tasks.id) FROM status LEFT JOIN tasks ON status.id = tasks.status_id GROUP BY status.name")

def get_tasks_for_domain_specific_users(domain):
    return execute_query("SELECT tasks.* FROM tasks JOIN users ON tasks.user_id = users.id WHERE users.email LIKE %s", ('%' + domain,))

def get_tasks_with_no_description():
    return execute_query("SELECT * FROM tasks WHERE description IS NULL OR description = ''")

def get_users_and_tasks_in_progress():
    return execute_query("SELECT users.fullname, tasks.title FROM users INNER JOIN tasks ON users.id = tasks.user_id WHERE tasks.status_id = (SELECT id FROM status WHERE name = 'in progress')")

def get_users_and_their_task_count():
    return execute_query("SELECT users.fullname, COUNT(tasks.id) FROM users LEFT JOIN tasks ON users.id = tasks.user_id GROUP BY users.fullname")

# Виконання конкретних запитів
if __name__ == '__main__':
    user_id = 1  # Приклад
    print("Завдання конкретного користувача:", get_tasks_by_user(user_id))
    print("Завдання за статусом 'new':", get_tasks_by_status('new'))
    update_task_status(1, 'in progress')  # Приклад: оновлення статусу завдання
    print("Користувачі без завдань:", get_users_with_no_tasks())
    add_task_for_user(user_id, "New Task", "This is a new task description")  # Додавання нового завдання
    print("Незавершені завдання:", get_incomplete_tasks())
    delete_task(2)  # Приклад: видалення завдання
    print("Користувачі з електронною поштою, що містить 'example.com':", find_users_by_email('%example.com'))
    update_user_name(user_id, "Updated Name")  # Приклад: оновлення імені користувача
    print("Кількість завдань за статусами:", get_task_count_by_status())
    print("Завдання для користувачів з доменом 'example.com':", get_tasks_for_domain_specific_users('example.com'))
    print("Завдання без опису:", get_tasks_with_no_description())
    print("Користувачі і їх завдання у статусі 'in progress':", get_users_and_tasks_in_progress())
    print("Користувачі та кількість їх завдань:", get_users_and_their_task_count())
