import pandas as pd
import os

# Загрузка двух CSV-файлов: до и после
before_path = "metrics/traffic_metrics_before1.csv"
after_path = "metrics/traffic_metrics_before20.csv" #МЕНЯЕМ НА +1

phase1 = 45  # сюда можно подставлять текущие фазы (светофор 1)
phase2 = 45  # и светофор 2

# Загрузка метрик
df_before = pd.read_csv(before_path)
df_after = pd.read_csv(after_path)

# Список метрик для сравнения
metrics = ["VEHS", "QUEUEDELAY", "SPEEDAVGARITH", "QLEN", "QLENMAX"]

# Группировка по OBJECT_ID
before_grouped = df_before.groupby("OBJECT_ID")[metrics].mean()
after_grouped = df_after.groupby("OBJECT_ID")[metrics].mean()

# Сравнение
comparison = after_grouped - before_grouped
comparison_percent = ((after_grouped - before_grouped) / before_grouped) * 100

summary = pd.concat([before_grouped, after_grouped, comparison, comparison_percent], axis=1, keys=["Before", "After", "Diff", "%Change"])

# Вывод результатов
pd.set_option("display.float_format", "{:.2f}".format)
print("\n🔍 Сравнение эффективности фаз ДО и ПОСЛЕ:")
print(summary)

# Сохранение сравнения в CSV #МЕНЯЕМ НА +1
summary_path = "data/phase_comparison_summary20.csv" #МЕНЯЕМ НА +1
os.makedirs("data", exist_ok=True)
summary.to_csv(summary_path)
print(f"\n📁 Сравнение сохранено в '{summary_path}'")

# --- Добавим запись в phase_log.csv ---
avg_metrics_before = df_before[metrics].mean()
avg_metrics_after = df_after[metrics].mean()
delta_metrics = avg_metrics_after - avg_metrics_before

# Формируем общую оценку (можно придумать весовую функцию позже)
evaluation = {
    "phase1": phase1,
    "phase2": phase2,
    "VEHICLES_before": avg_metrics_before["VEHS"],
    "QUEUEDELAY_before": avg_metrics_before["QUEUEDELAY"],
    "SPEEDAVGARITHM_before": avg_metrics_before["SPEEDAVGARITH"],
    "QLEN_before": avg_metrics_before["QLEN"],
    "QLENMAX_before": avg_metrics_before["QLENMAX"],
    "VEHICLES_after": avg_metrics_after["VEHS"],
    "QUEUEDELAY_after": avg_metrics_after["QUEUEDELAY"],
    "SPEEDAVGARITHM_after": avg_metrics_after["SPEEDAVGARITH"],
    "QLEN_after": avg_metrics_after["QLEN"],
    "QLENMAX_after": avg_metrics_after["QLENMAX"],
    "delta_QUEUEDELAY": delta_metrics["QUEUEDELAY"],
    "delta_SPEEDAVGARITHM": delta_metrics["SPEEDAVGARITH"],
    "delta_QLEN": delta_metrics["QLEN"],
    "delta_QLENMAX": delta_metrics["QLENMAX"]
}

log_path = "phase_res/phase_log.csv"
try:
    existing_log = pd.read_csv(log_path)
    updated_log = pd.concat([existing_log, pd.DataFrame([evaluation])], ignore_index=True)
except FileNotFoundError:
    updated_log = pd.DataFrame([evaluation])

updated_log.to_csv(log_path, index=False)
print(f"📊 Запись добавлена в журнал опыта: '{log_path}'")
