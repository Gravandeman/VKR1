import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# 📥 Пути к метрикам
before_path = "metrics/traffic_metrics_before1.csv"
after_path = "metrics/traffic_metrics_before8.csv"

# ✅ Загрузка данных
before = pd.read_csv(before_path)
after = pd.read_csv(after_path)

# 📊 Метрики для сравнения
metrics = ["VEHS", "QUEUEDELAY", "SPEEDAVGARITH", "QLEN", "QLENMAX"]

# 🌐 Группировка по OBJECT_ID
before_grouped = before.groupby("OBJECT_ID")[metrics].mean()
after_grouped = after.groupby("OBJECT_ID")[metrics].mean()

# ➕ Разница
diff = after_grouped - before_grouped
percent = (diff / before_grouped) * 100

# 📈 Общий отчёт
summary = pd.concat([before_grouped, after_grouped, diff, percent], axis=1, keys=["Before", "After", "Delta", "%Change"])
summary = summary.round(2)

# 📤 Сохранение
os.makedirs("data", exist_ok=True)
#summary.to_csv("data/final_phase_comparison.csv")
print("\n✅ Отчёт сохранён в 'data/final_phase_comparison.csv'")

# 📊 Построение диаграммы изменений по каждой метрике
diff.reset_index(inplace=True)
plt.figure(figsize=(12, 6))
diff_melted = diff.melt(id_vars="OBJECT_ID", var_name="Metric", value_name="Change")
sns.barplot(data=diff_melted, x="Metric", y="Change", hue="OBJECT_ID")
plt.title("Изменение метрик ДО и ПОСЛЕ применения новых фаз")
plt.ylabel("Разница (After - Before)")
plt.xticks(rotation=45)
plt.tight_layout()
#plt.savefig("data/phase_metrics_difference.png")
plt.show()

print("📊 График изменений сохранён в 'data/phase_metrics_difference.png'")

# 📘 Текстовый анализ изменений
print("\n📘 Анализ изменений по метрикам:")
for metric in metrics:
    delta = diff[metric].mean()
    direction = "уменьшилась" if delta < 0 else "увеличилась"
    print(f"Среднее значение метрики '{metric}' {direction} на {abs(delta):.2f} единиц")

    if metric == "QUEUEDELAY" and delta < 0:
        print("➡️  Задержка в заторе снизилась — это означает улучшение пропускной способности.")
    elif metric == "QUEUEDELAY" and delta > 0:
        print("⚠️  Задержка в заторе увеличилась — возможны пробки.")
    elif metric == "SPEEDAVGARITHM" and delta > 0:
        print("➡️  Средняя скорость выросла — движение стало быстрее.")
    elif metric == "SPEEDAVGARITHM" and delta < 0:
        print("⚠️  Средняя скорость снизилась — возможны заторы или снижение эффективности.")
    elif metric in ["QLEN", "QLENMAX"] and delta < 0:
        print(f"➡️  {metric} уменьшилась — заторы стали короче.")
    elif metric in ["QLEN", "QLENMAX"] and delta > 0:
        print(f"⚠️  {metric} увеличилась — возможное накопление транспорта.")