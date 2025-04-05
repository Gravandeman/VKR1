import sqlite3
import pandas as pd

# Путь к .db файлу
db_path = "C:/Users/andpm/Semestr8/VKR1/VKR.results/5.db"

# Подключаемся к базе данных
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Получаем список всех таблиц в базе
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Таблицы в базе данных:")
for table in tables:
    print(table[0])
