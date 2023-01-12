import sys
import tkinter as tk
from main_frame import MainFrame
from main_menu import MainMenu
from info_frame import InfoFrame
from ping3 import ping
import threading
import time
import datetime

dict_object = {}
del_object = {}
# dict_object['a']=1
root = tk.Tk()
root.title(("Ping Master - v.1.0"))
root.geometry("1210x608+100+100")  # Создаем окно
root.resizable(False, False)  # Запрещаем изменять размер окна
root.configure(background='#ffffff')  # Устанавливаем цвет фона

map = MainFrame(root, 1000, 560, dict_object, del_object)
info = InfoFrame('info', root, map, dict_object, 1200, 20)  # Инфополе внизу слева
stat = InfoFrame('stat', root, map, dict_object, 1200, 20)  # Статистика внизу
obj_info = InfoFrame('obj', root, map, dict_object, 180, 180) # Информация справа
text_ping = InfoFrame('ping', root, map, dict_object, 180, 400, obj_info, info, stat)
mm = MainMenu(root, map, info, dict_object, del_object)
# threading.Thread(target=ping_object).start()
# threading.Thread(target=watchdog_timer).start()
root.mainloop()  # Запускаем отображение
sys.exit()
# print(dict_object)