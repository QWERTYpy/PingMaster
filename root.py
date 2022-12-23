import tkinter as tk
from main_frame import MainFrame
from main_menu import MainMenu
from info_frame import InfoFrame
from ping3 import ping
import threading
import time

def ping_object():
    while True:
        time.sleep(5)
        for _ in dict_object.keys():
            ping_result = ping("10.64."+dict_object[_].ip_adr)
            ping_result_bool = True  # Пинг прошёл
            if ping_result is None or type(ping_result) is not float:
                ping_result_bool = False
            if ping_result_bool:
                map.main_canvas.itemconfig(_, fill="green")
                text_ping.text_right_info.insert(tk.INSERT, f"{dict_object[_].ip_adr}-ON\n", 'cool')
            else:
                map.main_canvas.itemconfig(_, fill="red")
                text_ping.text_right_info.insert(tk.INSERT, f"{dict_object[_].ip_adr}-OFF\n", 'warning')
        # print("Ping")


dict_object = {}
del_object = {}
# dict_object['a']=1
root = tk.Tk()
root.title(("Ping Master - v.1.0"))
root.geometry("1210x608+100+100")  # Создаем окно
root.resizable(False, False)  # Запрещаем изменять размер окна
root.configure(background='#ffffff')  # Устанавливаем цвет фона

map = MainFrame(root, 1000, 560, dict_object, del_object)
info = InfoFrame('info', root, 1200, 20)
text_ping = InfoFrame('ping', root, 180, 400)
MainMenu(root, map, info, dict_object, del_object)
threading.Thread(target=ping_object).start()
root.mainloop()  # Запускаем отображение
# print(dict_object)