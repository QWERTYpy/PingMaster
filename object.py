# Создание объектов

import tkinter as tk
import time


class Object:
    def __init__(self, root, set_position_x, set_position_y, delta_x, del_object):
        self.ip_adr = ""  # IP адрес
        self.descr = ""  # Описание
        self.rect = ""  # Метка прямоугольника
        self.label = ""  # Метка надписи
        self.delta_x = delta_x  # Кратность
        self.ping_status = False  # True & False
        self.ping_off = time.time()  # Date and Time
        # Создание нового объекта и назначение ему обработчиков
        self.root = root
        self.del_object = del_object
        self.x = round(set_position_x / delta_x, 0)
        self.y = round(set_position_y / delta_x, 0)
        self.label_info = tk.Label(self.root, text="")
        # Создаем объект на канве
        self.oval = self.root.create_oval((self.x - 1) * delta_x, (self.y - 1) * delta_x, (self.x + 1) * delta_x,
                                                 (self.y + 1) * delta_x, fill='red')
        # Привязываем к объекту действия
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

    def buttonrelease_1(self, event, element):
        # Когда левая кнопка отпущена
        if self.delta_x > 3:
            self.x = round(self.root.canvasx(event.x) / self.delta_x, 0)
            self.y = round(self.root.canvasy(event.y) / self.delta_x, 0)

    def b1_motion(self, event, element):
        # Когда левая кнопка нажата и происходит перемещение
        # Если масштаб больше 4 то отображаем
        if self.delta_x > 3:
            if element in self.del_object:
                self.root.delete(self.del_object[element])
                self.del_object.pop(element)
            # Получаем координаты окна и переводим их в координаты канвы
            _x = self.root.canvasx(event.x)
            _y = self.root.canvasy(event.y)
            # Перемещаем объект
            self.root.coords(self.oval, _x - self.delta_x, _y - self.delta_x, _x + self.delta_x,
                             _y + self.delta_x)
            # Перемещаем метку
            self.root.coords(self.label, _x + self.delta_x, _y)

    def enter(self, event, element):
        # Когда курсор входит в зону объекта
        self.label_info.config(text=self.ip_adr + "\n" + self.descr)
        self.label_info.place(x=event.x + 5, y=event.y + 5)



    def leave(self, event, element):
        # Когда курсор покидает объект
        self.label_info.place_forget()  # Удаляем


    def button_b1(self, event, element):
        # Когда нажата левая кнопка
        if element in self.del_object:
            # Если элемент есть в удаляемых, то удаляем прямоугольник выделения
            self.root.delete(self.del_object[element])
            # Освобождаем список
            self.del_object.pop(element)
        else:
            # Если словарь не пустой (вдруг)
            if len(self.del_object):
                _, _value = self.del_object.popitem()
                # Удаляем прямоугольник выделения
                self.root.delete(_value)
            # Выделяем объект прямоугольником
            self.rect = self.root.create_rectangle(self.root.coords(element))
            # Связываем элемент с прямоугольником
            self.del_object[element] = self.rect

    def resize(self, delta_x):
        # Действия при масштабировании
        self.delta_x = delta_x
        self.tmp_x = self.x * delta_x
        self.tmp_y = self.y * delta_x
        # Изменяем позицию объекта
        self.root.coords(self.oval, self.tmp_x - delta_x, self.tmp_y - delta_x, self.tmp_x + delta_x, self.tmp_y + delta_x)
        if self.rect:
            # Если объект выделен, то изменяем позицию и прямоугольника
            self.root.coords(self.rect, self.tmp_x - delta_x, self.tmp_y - delta_x, self.tmp_x + delta_x,
                             self.tmp_y + delta_x)
        # Изменяем позицию метки
        self.root.coords(self.label, self.tmp_x+delta_x,self.tmp_y)
