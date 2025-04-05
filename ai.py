import win32com.client

# Подключаемся к запущенной сессии Vissim
Vissim = win32com.client.Dispatch("Vissim.Vissim")

# Загружаем проект (укажи свой путь)
Vissim.LoadNet("C:/Users/andpm/Semestr8/VKR1/VKR.inpx")

# Запускаем симуляцию
Vissim.Simulation.RunContinuous()



# Получаем список контроллеров светофоров
signal_controllers = Vissim.Net.SignalControllers.GetAll()

for controller in signal_controllers:
    id = controller.AttValue("No")  # ID светофора
    phase_time = controller.AttValue("ProgTime")  # Время текущей фазы

    print(f"Светофор {id}: Текущая фаза {phase_time} секунд")
