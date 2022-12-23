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
        self.delta_x = delta_x
        self.ping_status = ""
        # Создание нового объекта и назначение ему обработчиков
        self.root = root
        self.del_object = del_object
        self.x = round(set_position_x / delta_x, 0)
        self.y = round(set_position_y / delta_x, 0)
        self.label_info = tk.Label(self.root, text="")
        # self.delta_x = delta_x
        self.oval = self.root.create_oval((self.x - 1) * delta_x, (self.y - 1) * delta_x, (self.x + 1) * delta_x,
                                                 (self.y + 1) * delta_x, fill='red')
        self.root.tag_bind(self.oval, "<Button-1>",
                                  lambda event, element=self.oval: self.button_b1(event, element))

        self.root.tag_bind(self.oval, "<Enter>",
                           lambda event, element=self.oval: self.enter(event, element))

        self.root.tag_bind(self.oval, "<Leave>",
                           lambda event, element=self.oval: self.leave(event, element))

        self.root.tag_bind(self.oval, "<B1-Motion>",
                           lambda event, element=self.oval: self.b1_motion(event, element))

        self.root.tag_bind(self.oval, " <ButtonRelease-1>",
                           lambda event, element=self.oval: self.buttonrelease_1(event, element))
        # self.root.tag_bind(self.oval, "<Button-3>",
        #                           lambda event, element=self.oval: self.right_button_click(event, element))

    def buttonrelease_1(self, event, element):
        # Когда левая кнопка отпущена
        if self.delta_x > 3:
            self.x = round(self.root.canvasx(event.x) / self.delta_x, 0)
            self.y = round(self.root.canvasy(event.y) / self.delta_x, 0)
        # print(self.x,self._x,self.y,self._y)

    def b1_motion(self,event, element):
        # Когда левая кнопка нажата и происходит перемещение
        # self.main_canvas.canvasx(self.position_cursor_old_x)
        if self.delta_x > 3:
            if element in self.del_object:
                self.root.delete(self.del_object[element])
                self.del_object.pop(element)
            _x = self.root.canvasx(event.x)
            _y = self.root.canvasy(event.y)
            self.root.coords(self.oval, _x - self.delta_x, _y - self.delta_x, _x + self.delta_x,
                             _y + self.delta_x)
            self.root.coords(self.label, _x + self.delta_x, _y)
            # self.root.tag_raise(self.label)
            print(event.x, event.y)

    def enter(self, event, element):
        # Когда курсор входит в зону объекта
        # self.root.after(3000, self.enter_sleep(event, element))
        self.label_info.config(text=self.ip_adr + "\n" + self.descr)
        self.label_info.place(x=event.x + 5, y=event.y + 5)
        # print(event.x, event.y)



    def leave(self, event, element):
        # Когда курсор покидает объект
        self.label_info.place_forget()
        # print(event.x,event.y)

    def button_b1(self, event, element):
        # Когда нажата левая кнопка
        # print(element)
        # self.main_canvas.delete(element-2)
        # print(self.main_canvas.find_all()) #показывает все ID
        # print(self.root.coords(self.oval))
        # print(self.root.coords(element))
        if element in self.del_object:
            self.root.delete(self.del_object[element])
            self.del_object.pop(element)
        else:
            if len(self.del_object):
                _, _value = self.del_object.popitem()
                self.root.delete(_value)
                # self.del_object.pop(*self.del_object.keys())
            self.rect = self.root.create_rectangle(self.root.coords(element))
            self.del_object[element] = self.rect
            # print(self.rect)
        print(self.del_object)

    def resize(self, delta_x):
        # Действия при масштабировании
        self.delta_x = delta_x
        self.tmp_x = self.x * delta_x
        self.tmp_y = self.y * delta_x
        self.root.coords(self.oval, self.tmp_x - delta_x, self.tmp_y - delta_x, self.tmp_x + delta_x, self.tmp_y + delta_x)
        if self.rect:
            self.root.coords(self.rect, self.tmp_x - delta_x, self.tmp_y - delta_x, self.tmp_x + delta_x,
                             self.tmp_y + delta_x)
        self.root.coords(self.label, self.tmp_x+delta_x,self.tmp_y)

