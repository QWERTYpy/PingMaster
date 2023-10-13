import sys
import tkinter as tk
from main_frame import MainFrame
from main_menu import MainMenu
from info_frame import InfoFrame
from object import ObjectDict
import saveload as sl
import history as hs


# Создаем Объект содержажащий все данные
objectDict = ObjectDict()
def on_closing():
    sl.save_ini(objectDict.dict_object)
    root.destroy()  # Закрыть окно

hs.folder_exist()  # Проверяем существует ли папка для логов
root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
root.title("Ping Master - v.1.4")
root.geometry("1250x608+100+100")  # Создаем окно
root.resizable(False, False)  # Запрещаем изменять размер окна
root.configure(background='#ffffff')  # Устанавливаем цвет фона

mapFrame = MainFrame(root, 1000, 560, objectDict)
info = InfoFrame('info', root, mapFrame, objectDict, 1200, 20)  # Инфополе внизу слева
stat = InfoFrame('stat', root, mapFrame, objectDict, 1200, 20)  # Статистика внизу
obj_info = InfoFrame('obj', root, mapFrame, objectDict, 220, 180)  # Информация справа
text_ping = InfoFrame('ping', root, mapFrame, objectDict, 220, 400, obj_info, info, stat)  # Информация о пинге
mm = MainMenu(root, mapFrame, info, objectDict)
root.mainloop()  # Запускаем отображение
sys.exit()
