# Создание объектов
import os.path
import tkinter as tk
from PIL import Image, ImageTk
# from device import Device
import saveload as sl
from description import Descr

class MainMenu:
    def __init__(self, root, map, info, dict_object, del_object):
        self.info = info
        self.root = root
        self.main_canvas = map.main_canvas
        self.dict_object = dict_object
        self.del_oblect = del_object
        # Создаем меню
        self.main_menu = tk.Menu(root)
        root.config(menu=self.main_menu)
        self.main_menu.add_command(label="Сохранить", command=self.save_object)
        self.main_menu.add_command(label="Удалить", command=self.del_object)
        self.main_menu.add_command(label="Редактировать", command=self.edit_object)



    def save_object(self):
        # Сохраняем объекты
        sl.save_ini(self.dict_object)
        self.info.title_left_down_text.set("Сохранено")

    def del_object(self):
        # Удаляем объекты с канвы
        for _ in self.del_oblect.keys():
            self.dict_object.pop(_)
            self.main_canvas.delete(self.del_oblect[_])
            self.main_canvas.delete(_)
        self.del_oblect.clear()
        self.info.title_left_down_text.set("Удалено")

    def edit_object(self):
        # Редактирование описания объектов
        for obj in self.del_oblect.keys():
            # self.main_canvas.itemconfig(obj, fill="green")
            descr = Descr(self.root, ip_adr=self.dict_object[obj].ip_adr, descr=self.dict_object[obj].descr)
            _, x, y = self.root.geometry().split('+')
            descr.geometry(f"200x180+{int(x) + 100}+{int(y)+100}")
            # print(self.dict_object[obj].ip_adr)
            # print(obj)
            descr.grab_set()
            descr.wait_window()
            # # print(descr.button)
            # Если в форме была нажата кнопка сохранить
            if descr.button:
                self.dict_object[obj].ip_adr = descr.ip_adr
                self.dict_object[obj].descr = descr.descr
                self.main_canvas.itemconfigure(self.dict_object[obj].label, text=descr.ip_adr)
                self.info.title_left_down_text.set("Описание изменено")
