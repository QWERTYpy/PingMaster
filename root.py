import tkinter as tk
from main_frame import MainFrame
from main_menu import MainMenu
from info_frame import InfoFrame
from ping3 import ping
import threading
import time
import datetime


def ping_object():
    # Опрос устройств
    while True:
        time.sleep(5)
        for _ in dict_object.keys():
            # Составляем IP адрес устройства
            ping_result = ping("10.64." + dict_object[_].ip_adr)
            ping_result_bool = True  # Пинг прошёл
            if ping_result is None or type(ping_result) is not float:
                ping_result_bool = False
            if ping_result_bool:
                map.main_canvas.itemconfig(_, fill="green")
                if not dict_object[_].ping_status:
                    #text_ping.text_right_info.insert(tk.INSERT, f"{dict_object[_].ip_adr}-ON\n", 'cool')
                    dict_object[_].ping_status = True
            else:
                map.main_canvas.itemconfig(_, fill="red")
                if dict_object[_].ping_status:
                    #text_ping.text_right_info.insert(tk.INSERT, f"{dict_object[_].ip_adr}-OFF\n", 'warning')
                    dict_object[_].ping_status = False
                    dict_object[_].ping_off = time.time()
            ping_info()

        # print("Ping")

def ping_info():
    text_ping.text_right_info.configure(state='normal')
    text_ping.text_right_info.delete(1.0, tk.END)
    for __ in dict_object.keys():
        if not dict_object[__].ping_status:
            text_ping.text_right_info.insert(tk.INSERT, f"{dict_object[__].ip_adr}-{datetime.timedelta(seconds=int(time.time()-dict_object[__].ping_off))}\n", 'warning')
    text_ping.text_right_info.configure(state='disabled')

dict_object = {}
del_object = {}
# dict_object['a']=1
root = tk.Tk()
root.title(("Ping Master - v.1.0"))
root.geometry("1210x608+100+100")  # Создаем окно
root.resizable(False, False)  # Запрещаем изменять размер окна
root.configure(background='#ffffff')  # Устанавливаем цвет фона

map = MainFrame(root, 1000, 560, dict_object, del_object)
info = InfoFrame('info', root, map, dict_object, 1200, 20)
obj_info = InfoFrame('obj', root, map, dict_object, 180, 180)
text_ping = InfoFrame('ping', root, map, dict_object, 180, 400, obj_info)
MainMenu(root, map, info, dict_object, del_object)
threading.Thread(target=ping_object).start()
root.mainloop()  # Запускаем отображение
# print(dict_object)