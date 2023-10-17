# Создание объектов

import tkinter as tk


class ObjectDict:
    def __init__(self):
        self.dict_object = {}  # Создаем словарь для хранения созданных объектов
        self.dict_del_object = {}  # Создаем словарь для хранения объектов на удаление
        self.reboot_ping = False  # Создаем флаг для перезагрузки пинга


class Object:
    def __init__(self, main_canvas, ini_block, delta_x, objectDict: ObjectDict):
    # def __init__(self, root, set_position_x, set_position_y, delta_x, del_object):
        self.main_canvas = main_canvas
        self.ip_adr = ini_block[0]  # IP адрес
        self.descr = ini_block[3]  # Описание
        self.rect = ""  # Метка прямоугольника
        self.red_oval = ""  # Метка для выделения отсутствующих
        self.grey_oval = ""  # Метка для выделения отключенных
        self.delta_x = delta_x  # Кратность
        _set_position_x = int(float(ini_block[1]))
        _set_position_y = int(float(ini_block[2]))
        self.label = self.main_canvas.create_text(_set_position_x+delta_x, _set_position_y, anchor='w', text=ini_block[0])  # Метка надписи
        self.main_canvas.tag_lower(self.label)

        # Если кратность более 4, то отображаем метки
        if self.delta_x >= 4:
            self.main_canvas.tag_raise(self.label)
        self.ping_status = ini_block[4]  # True & False Отвечает ли на пинг
        self.work_status = ini_block[6]  # True & False Отключенная
        self.ping_off = ini_block[5]  # Date and Time
        # Создание нового объекта и назначение ему обработчиков
        self.objectDict = objectDict
        self.x = round(_set_position_x / delta_x, 0)
        self.y = round(_set_position_y / delta_x, 0)
        self.label_info = tk.Label(self.main_canvas, text="")  # Всплывающая метка
        # Создаем объект на канве
        self.oval = self.main_canvas.create_oval((self.x - 1) * delta_x, (self.y - 1) * delta_x, (self.x + 1) * delta_x,
                                                 (self.y + 1) * delta_x, fill='red')
        # Привязываем к объекту действия
        self.main_canvas.tag_bind(self.oval, "<Button-1>",
                                  lambda event, element=self.oval: self.button_b1(event, element))
        self.main_canvas.tag_bind(self.oval, "<Enter>",
                           lambda event, element=self.oval: self.enter(event, element))
        self.main_canvas.tag_bind(self.oval, "<Leave>",
                           lambda event, element=self.oval: self.leave(event, element))
        self.main_canvas.tag_bind(self.oval, "<B1-Motion>",
                           lambda event, element=self.oval: self.b1_motion(event, element))
        self.main_canvas.tag_bind(self.oval, " <ButtonRelease-1>",
                           lambda event, element=self.oval: self.buttonrelease_1(event, element))

    def buttonrelease_1(self, event, element):
        # Когда левая кнопка отпущена
        if self.delta_x > 3:
            self.x = round(self.main_canvas.canvasx(event.x) / self.delta_x, 0)
            self.y = round(self.main_canvas.canvasy(event.y) / self.delta_x, 0)

    def b1_motion(self, event, element):
        # Когда левая кнопка нажата и происходит перемещение
        # Если масштаб больше 4 то отображаем
        if self.delta_x > 3:
            if element in self.objectDict.dict_del_object:
                self.main_canvas.delete(self.objectDict.dict_del_object[element])
                self.objectDict.dict_del_object.pop(element)
            # Получаем координаты окна и переводим их в координаты канвы
            _x = self.main_canvas.canvasx(event.x)
            _y = self.main_canvas.canvasy(event.y)
            # Перемещаем объект
            self.main_canvas.coords(self.oval, _x - self.delta_x, _y - self.delta_x, _x + self.delta_x,
                             _y + self.delta_x)
            # Перемещаем метку
            self.main_canvas.coords(self.label, _x + self.delta_x, _y)
            # Перемещаем выделение если есть
            if self.red_oval:
                self.main_canvas.coords(self.red_oval, _x - 2*self.delta_x, _y - 2*self.delta_x, _x + 2*self.delta_x,
                             _y + 2*self.delta_x)

    def enter(self, event, element):
        # Когда курсор входит в зону объекта
        self.label_info.config(text=self.ip_adr + "\n" + self.descr)
        self.label_info.place(x=event.x + 5, y=event.y + 5)

    def leave(self, event, element):
        # Когда курсор покидает объект
        self.label_info.place_forget()  # Удаляем

    def button_b1(self, event, element):
        # Когда нажата левая кнопка
        if element in self.objectDict.dict_del_object:
            # Если элемент есть в удаляемых, то удаляем прямоугольник выделения
            self.main_canvas.delete(self.objectDict.dict_del_object[element])
            # Освобождаем список
            self.objectDict.dict_del_object.pop(element)
        else:
            # Если словарь не пустой (вдруг)
            if len(self.objectDict.dict_del_object):
                _, _value = self.objectDict.dict_del_object.popitem()
                # Удаляем прямоугольник выделения
                self.main_canvas.delete(_value)
            # Выделяем объект прямоугольником
            self.rect = self.main_canvas.create_rectangle(self.main_canvas.coords(element))
            # Связываем элемент с прямоугольником
            self.objectDict.dict_del_object[element] = self.rect

    def resize(self, delta_x):
        # Действия при масштабировании
        self.delta_x = delta_x
        self.tmp_x = self.x * delta_x
        self.tmp_y = self.y * delta_x
        # Изменяем позицию объекта
        self.main_canvas.coords(self.oval, self.tmp_x - delta_x, self.tmp_y - delta_x, self.tmp_x + delta_x, self.tmp_y + delta_x)
        if self.rect:
            # Если объект выделен, то изменяем позицию и прямоугольника
            self.main_canvas.coords(self.rect, self.tmp_x - delta_x, self.tmp_y - delta_x, self.tmp_x + delta_x,
                             self.tmp_y + delta_x)
        if self.red_oval:
            self.main_canvas.coords(self.red_oval, self.tmp_x - 2*delta_x, self.tmp_y - 2*delta_x, self.tmp_x + 2*delta_x,
                             self.tmp_y + 2*delta_x)
        if self.grey_oval:
            self.main_canvas.coords(self.grey_oval, self.tmp_x - 2 * delta_x, self.tmp_y - 2 * delta_x,
                                    self.tmp_x + 2 * delta_x, self.tmp_y + 2 * delta_x)
        # Изменяем позицию метки
        self.main_canvas.coords(self.label, self.tmp_x+delta_x,self.tmp_y)

    def setcolor_RG(self):
        # Установка цвета точек
        if self.ping_status:
            self.main_canvas.itemconfig(self.oval, fill="green")
            # Удаляем дополнительное очерчивание
            self.main_canvas.delete(self.red_oval)
            self.red_oval = ""
        else:
            self.main_canvas.itemconfig(self.oval, fill="red")
            tmp_x = self.x * self.delta_x
            tmp_y = self.y * self.delta_x
            delta_x = self.delta_x
            if not self.red_oval:
                self.red_oval = self.main_canvas.create_oval(tmp_x - 2 * delta_x, tmp_y - 2 * delta_x,
                                                                            tmp_x + 2 * delta_x, tmp_y + 2 * delta_x,
                                                                            outline='orange', width=3)

    def setcolor_grey(self):
        # Очерчевание серым отключенных устройств
        if not self.work_status:
            self.main_canvas.itemconfig(self.oval, fill="grey")
            tmp_x = self.x * self.delta_x
            tmp_y = self.y * self.delta_x
            delta_x = self.delta_x
            self.grey_oval = self.main_canvas.create_oval(tmp_x - 2 * delta_x, tmp_y - 2 * delta_x,
                                                         tmp_x + 2 * delta_x, tmp_y + 2 * delta_x,
                                                         outline='grey', width=3)
            if self.red_oval:
                self.main_canvas.delete(self.red_oval)
                self.red_oval = ""
        else:
            self.main_canvas.delete(self.grey_oval)
            self.grey_oval = ""

    def up_line(self):
        # Поднять над слоями
        if self.red_oval:
            self.main_canvas.tag_raise(self.red_oval)
        if self.grey_oval:
            self.main_canvas.tag_raise(self.grey_oval)
        # Отображаем метки только если масштаб 4 и больше
        if self.delta_x > 3:
            self.main_canvas.tag_raise(self.label)
        else:
            self.main_canvas.tag_lower(self.label)
