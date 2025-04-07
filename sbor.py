import sqlite3
import pandas as pd

# Путь к твоему .db файлу от Vissim #МЕНЯЕМ НА +1
db_path = "C:/Users/andpm/Semestr8/VKR1/VKR.results/40.db" #МЕНЯЕМ НА +1

# Подключение к базе
conn = sqlite3.connect(db_path)

# Загрузка таблицы с точками сбора данных
query_data_collection = """
SELECT OBJECT_ID, VEHS, QUEUEDELAY, SPEEDAVGARITH
FROM DATACOLLECTIONMEASUREMENT_EvaluationTimeIntervalClass
"""

# Загрузка таблицы с длинами затора
query_queue_counter = """
SELECT OBJECT_ID, QLEN, QLENMAX
FROM QUEUECOUNTER_EvaluationTimeInterval
"""

# Чтение таблиц
df_data = pd.read_sql_query(query_data_collection, conn)
df_queue = pd.read_sql_query(query_queue_counter, conn)

conn.close()

# Объединяем таблицы по OBJECT_ID (если ID совпадают логически)
df_merged = pd.merge(df_data, df_queue, on="OBJECT_ID", how="outer")

# Сохраняем в CSV для ИИ #МЕНЯЕМ НА +1
df_merged.to_csv("metrics/traffic_metrics_before20.csv", index=False) #МЕНЯЕМ НА +1
print("✅ Данные успешно сохранены в 'traffic_metrics.csv'")
