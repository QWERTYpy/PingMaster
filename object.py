# Создание объектов
import os.path
import tkinter as tk
from PIL import Image, ImageTk
# from device import Device

class Object:
    def __init__(self, root, set_position_x, set_position_y, delta_x):
        self.ip_adr = ""
        self.descr = ""
        # Создание нового объекта и назначение ему обработчиков
        self.root = root
        self.x = round(set_position_x / delta_x, 0)
        self.y = round(set_position_y / delta_x, 0)

        # self.delta_x = delta_x
        self.oval = self.root.create_oval((self.x - 1) * delta_x, (self.y - 1) * delta_x, (self.x + 1) * delta_x,
                                                 (self.y + 1) * delta_x, fill='red')
        self.root.tag_bind(self.oval, "<Button-1>",
                                  lambda event, element=self.oval: self.name_obj(event, element))
        # self.root.tag_bind(self.oval, "<Button-3>",
        #                           lambda event, element=self.oval: self.right_button_click(event, element))

    def name_obj(self, event, element):
        # print(element)
        # self.main_canvas.delete(element-2)
        # print(self.main_canvas.find_all()) #показывает все ID
        print(self.root.coords(self.oval))

    def resize(self, delta_x):

        self.tmp_x = self.x * delta_x
        self.tmp_y = self.y * delta_x
        self.root.coords(self.oval, self.tmp_x - delta_x, self.tmp_y - delta_x, self.tmp_x + delta_x, self.tmp_y + delta_x)

