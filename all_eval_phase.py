import pandas as pd
import numpy as np

# Загрузка журнала фаз
log = pd.read_csv("phase_res/phase_log.csv")

# Вычисляем оценку эффективности фаз
log["score"] = (
    -log["delta_QUEUEDELAY"]   # хотим уменьшить задержку
    + log["delta_SPEEDAVGARITHM"]  # хотим повысить скорость
    - log["delta_QLEN"]        # хотим уменьшить длину затора
    - log["delta_QLENMAX"]     # и его максимум
)

# Округлим для наглядности
log[["delta_QUEUEDELAY", "delta_SPEEDAVGARITHM", "delta_QLEN", "delta_QLENMAX", "score"]] = log[[
    "delta_QUEUEDELAY", "delta_SPEEDAVGARITHM", "delta_QLEN", "delta_QLENMAX", "score"
]].round(2)

# Сортировка по оценке (чем выше — тем лучше)
sorted_log = log.sort_values(by="score", ascending=False).reset_index(drop=True)

# Вывод топ-результатов
print("\n🏁 Топ фаз по эффективности:")
print(sorted_log[["phase1", "phase2", "delta_QUEUEDELAY", "delta_SPEEDAVGARITHM", "delta_QLEN", "delta_QLENMAX", "score"]])

# Сохранение отчёта
#sorted_log.to_csv("phase_res/evaluated_phases.csv", index=False)
#print("\n✅ Результаты сохранены в 'phase_res/evaluated_phases.csv'")
