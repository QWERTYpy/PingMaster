# Создание объектов
import os.path
import tkinter as tk
from PIL import Image, ImageTk
# from device import Device
import saveload as sl

class MainMenu:
    def __init__(self, root, map, info, dict_object, del_object):
        self.info = info
        self.main_canvas = map.main_canvas
        self.dict_object = dict_object
        self.del_oblect = del_object
        # Создаем меню
        self.main_menu = tk.Menu(root)
        root.config(menu=self.main_menu)
        self.main_menu.add_command(label="Сохранить", command=self.save_object)
        self.main_menu.add_command(label="Удалить", command=self.del_object)


    def save_object(self):
        # # if os.path.exists("ip_config.ini"):
        # config = configparser.ConfigParser()
        # for _ in self.dict_device.keys():
        #     # print(self.main_canvas.move(_, delta, delta))
        #     x, y = self.dict_device[_].coord

        # self.title_left_down_text.set("Сохранено")
        sl.save_ini(self.dict_object)
        self.info.title_left_down_text.set("Сохранено")

    def del_object(self):
        for _ in self.del_oblect.keys():
            self.main_canvas.delete(self.del_oblect[_])
            self.main_canvas.delete(_)

        self.info.title_left_down_text.set("Удалено")