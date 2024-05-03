from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Налаштування підключення до MongoDB
client = MongoClient("mongodb://root:5344166@localhost:27017/")
db = client['cats_db']
cats = db['cats']

def add_cats():
    """Додає котів до колекції для тесту."""
    try:
        cats.insert_many([
            {"name": "barsik", "age": 3, "features": ["ходить в капці", "дає себе гладити", "рудий"]},
            {"name": "murzik", "age": 5, "features": ["має пухнастий хвіст", "ловить мишей"]}
        ])
        print("Коти додані для тесту.")
    except PyMongoError as e:
        print("Помилка при додаванні котів:", e)

def print_all_cats():
    """Виводить всі записи з колекції cats."""
    try:
        all_cats = cats.find()
        for cat in all_cats:
            print(cat)
    except PyMongoError as e:
        print("Error accessing database:", e)

def input_with_prompt(prompt):
    """Запитує у користувача ввід з заданим повідомленням і перевіряє чи ввід не пустий."""
    user_input = input(prompt)
    while user_input.strip() == "":
        print("Input cannot be empty. Please try again.")
        user_input = input(prompt)
    return user_input

def find_cat_by_name():
    """Дозволяє користувачу ввести ім'я кота та виводить інформацію про цього кота."""
    name = input_with_prompt("Enter the name of the cat: ")
    try:
        cat = cats.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print("No cat found with the name", name)
    except PyMongoError as e:
        print("Error accessing database:", e)

def update_cat_age():
    """Дозволяє користувачеві оновити вік кота за ім'ям."""
    name = input_with_prompt("Enter the name of the cat to update: ")
    age = input_with_prompt("Enter the new age: ")
    try:
        result = cats.update_one({"name": name}, {"$set": {"age": int(age)}})
        if result.modified_count:
            print("Cat age updated.")
        else:
            print("No cat updated.")
    except PyMongoError as e:
        print("Error updating database:", e)

def add_feature_to_cat():
    """Дозволяє додати нову характеристику до списку features кота за ім'ям."""
    name = input_with_prompt("Enter the name of the cat to update: ")
    feature = input_with_prompt("Enter the new feature to add: ")
    try:
        result = cats.update_one({"name": name}, {"$addToSet": {"features": feature}})
        if result.modified_count:
            print("Feature added to cat.")
        else:
            print("No feature added.")
    except PyMongoError as e:
        print("Error updating database:", e)

def delete_cat_by_name():
    """Видаляє запис з колекції за ім'ям тварини."""
    name = input_with_prompt("Enter the name of the cat to delete: ")
    try:
        result = cats.delete_one({"name": name})
        if result.deleted_count:
            print("Cat deleted.")
        else:
            print("No cat found to delete.")
    except PyMongoError as e:
        print("Error deleting from database:", e)

def delete_all_cats():
    """Видаляє всі записи з колекції."""
    try:
        result = cats.delete_many({})
        print(f"Deleted {result.deleted_count} cats.")
    except PyMongoError as e:
        print("Error deleting from database:", e)

def main():
    """Основна функція, яка запускає меню для керування базою даних котів."""
    while True:
        print("\nCAT DATABASE OPERATIONS:")
        print("1 - Add Cats for Testing")
        print("2 - Print All Cats")
        print("3 - Find Cat by Name")
        print("4 - Update Cat Age")
        print("5 - Add Feature to Cat")
        print("6 - Delete Cat by Name")
        print("7 - Delete All Cats")
        print("0 - Exit")
        choice = input("Choose an operation: ")

        if choice == "1":
            add_cats()
        elif choice == "2":
            print_all_cats()
        elif choice == "3":
            find_cat_by_name()
        elif choice == "4":
            update_cat_age()
        elif choice == "5":
            add_feature_to_cat()
        elif choice == "6":
            delete_cat_by_name()
        elif choice == "7":
            delete_all_cats()
        elif choice == "0":
            print("Exiting the program.")
            break
        else:
            print("Invalid input, please choose a valid operation.")

if __name__ == "__main__":
    main()
