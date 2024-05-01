from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def connect_to_db():
    try:
        # Використання URI для підключення, що включає ім'я користувача та пароль
        uri = "mongodb://root:5344166@localhost:27017/"
        client = MongoClient(uri)
        db = client['cats_db']
        return db['cats']
    except ConnectionFailure:
        print("Сервер MongoDB не доступний")
        return None

# Додавання котів для тестування
def add_cats(collection):
    try:
        collection.insert_many([
            {"name": "barsik", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]},
            {"name": "murzik", "age": 5, "features": ["має пухнастий хвіст", "ловить мишей"]}
        ])
        print("Коти додані для тесту.")
    except Exception as e:
        print("Помилка при додаванні котів:", e)

# Читання: пошук кота за іменем
def find_cat_by_name(collection, name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("Кіт з іменем", name, "не знайдений.")
    except Exception as e:
        print("Помилка при пошуку кота:", e)

# Оновлення: оновити вік кота
def update_cat_age(collection, name, age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": age}})
        if result.modified_count:
            print("Вік кота оновлено.")
        else:
            print("Оновлення не виконано.")
    except Exception as e:
        print("Помилка оновлення віку кота:", e)

# Видалення: видалити кота за іменем
def delete_cat_by_name(collection, name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print("Кіт видалений.")
        else:
            print("Кіт з іменем", name, "не знайдений для видалення.")
    except Exception as e:
        print("Помилка видалення кота:", e)

# Виконання
if __name__ == "__main__":
    cats_collection = connect_to_db()
    if cats_collection is not None:
        add_cats(cats_collection)
        find_cat_by_name(cats_collection, "barsik")
        update_cat_age(cats_collection, "barsik", 4)
        delete_cat_by_name(cats_collection, "barsik")
