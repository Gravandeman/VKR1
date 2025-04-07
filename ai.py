import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# 📥 Загрузка логов фаз с расширенными метриками
log = pd.read_csv("phase_res/phase_log.csv")

# Используем все метрики ДО применения фаз как входные признаки
X = log[[
    "VEHICLES_before",
    "QUEUEDELAY_before",
    "SPEEDAVGARITHM_before",
    "QLEN_before",
    "QLENMAX_before"
]]

# Целевые значения — предложенные ранее фазы, которые дали результат
y = log[["phase1", "phase2"]]

# 🔄 Масштабирование входных данных
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 🚀 Разделение на обучающую и тестовую выборку
if len(X_scaled) < 2:
    print("⚠ Недостаточно данных для тестовой выборки. Обучение на всей выборке.")
    X_train, X_test = X_scaled, X_scaled
    y_train, y_test = y, y
else:
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42
    )

# 🧠 Построение нейросети
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dense(2)  # выход: две фазы (светофор 1 и 2)
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 🏋️ Обучение модели
if len(X_train) < 2:
    model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=1)
else:
    model.fit(X_train, y_train, epochs=100, batch_size=8, verbose=1)

# 💬 Оценка
loss, mae = model.evaluate(X_test, y_test)
print(f"Средняя абсолютная ошибка (MAE): {mae:.2f} секунд")

# 💡 Предсказание на основе последних входных метрик
last_input = log[[
    "VEHICLES_before",
    "QUEUEDELAY_before",
    "SPEEDAVGARITHM_before",
    "QLEN_before",
    "QLENMAX_before"
]].iloc[[-1]]

last_input_scaled = scaler.transform(last_input)
predicted_phases = model.predict(last_input_scaled)

print("\n🔮 Предсказанные оптимальные фазы:")
print(f"Светофор 1 (ID 1+2): {predicted_phases[0][0]:.1f} секунд")
print(f"Светофор 2 (ID 3+4): {predicted_phases[0][1]:.1f} секунд")