# Создание объектов
import os.path
import tkinter as tk
from PIL import Image, ImageTk
# from device import Device

class MainMenu:
    def __init__(self, root, info):
        self.info = info
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
        self.info.title_left_down_text.set("Сохранено")

    def del_object(self):
        self.info.title_left_down_text.set("Удалено")