# Создание объектов
import os.path
import tkinter as tk
from PIL import Image, ImageTk
# from device import Device

class Object:
    def __init__(self, root, set_position_x, set_position_y, delta_x, del_object):
        self.ip_adr = ""
        self.descr = ""
        self.rect = ""
        self.label = ""
        # Создание нового объекта и назначение ему обработчиков
        self.root = root
        self.del_object = del_object
        self.x = round(set_position_x / delta_x, 0)
        self.y = round(set_position_y / delta_x, 0)
        self.label_info = tk.Label(self.root, text="111")
        # self.delta_x = delta_x
        self.oval = self.root.create_oval((self.x - 1) * delta_x, (self.y - 1) * delta_x, (self.x + 1) * delta_x,
                                                 (self.y + 1) * delta_x, fill='red')
        self.root.tag_bind(self.oval, "<Button-1>",
                                  lambda event, element=self.oval: self.name_obj(event, element))

        self.root.tag_bind(self.oval, "<Enter>",
                           lambda event, element=self.oval: self.enter(event, element))

        self.root.tag_bind(self.oval, "<Leave>",
                           lambda event, element=self.oval: self.leave(event, element))
        # self.root.tag_bind(self.oval, "<Button-3>",
        #                           lambda event, element=self.oval: self.right_button_click(event, element))


    def enter(self, event, element):
        self.root.after(3000, self.enter_sleep(event, element))
        print(event.x, event.y)

    def enter_sleep(self, event, element):
        self.label_info.config(text=self.ip_adr+"\n"+self.descr)
        self.label_info.place(x=event.x+5, y=event.y+5)
        # print(event.x,event.y)

    def leave(self, event, element):
        self.label_info.place_forget()
        # print(event.x,event.y)

    def name_obj(self, event, element):
        # print(element)
        # self.main_canvas.delete(element-2)
        # print(self.main_canvas.find_all()) #показывает все ID
        # print(self.root.coords(self.oval))
        # print(self.root.coords(element))
        if element in self.del_object:
            self.root.delete(self.del_object[element])
            self.del_object.pop(element)
        else:
            self.rect = self.root.create_rectangle(self.root.coords(element))
            self.del_object[element] = self.rect
            # print(self.rect)
        print(self.del_object)

    def resize(self, delta_x):

        self.tmp_x = self.x * delta_x
        self.tmp_y = self.y * delta_x
        self.root.coords(self.oval, self.tmp_x - delta_x, self.tmp_y - delta_x, self.tmp_x + delta_x, self.tmp_y + delta_x)
        if self.rect:
            self.root.coords(self.rect, self.tmp_x - delta_x, self.tmp_y - delta_x, self.tmp_x + delta_x,
                             self.tmp_y + delta_x)
        self.root.coords(self.label, self.tmp_x+delta_x,self.tmp_y)

