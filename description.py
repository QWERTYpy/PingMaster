import tkinter as tk
from tkinter import ttk
from object import Object, ObjectDict
import tkinter.messagebox as mb
import re
# Всплывающее меню при создании или редактировании информации об объекте


def is_valid(newval):  # Проверка ввода ключа
    return re.match("^[0-9]{0,3}[.][0-9]{0,3}$", newval) is not None


class Descr(tk.Toplevel):
    def __init__(self, parent, delta_x, coord, element=None, objectDict: ObjectDict = None):
        super().__init__(parent)
        self.delta_x = delta_x
        # Создаем все поля
        self.main_canvas = parent
        self.label_dsc = tk.Label(self, text="Добавьте описание:")
        self.label_dsc.place(x=0, y=0)
        self.label_ip = tk.Label(self, text="IP адрес:")
        self.label_ip.place(x=0, y=20)

        check = (self.register(is_valid), "%P")
        self.entry_ip = tk.Entry(self, width=20, validate="key", validatecommand=check)
        self.label_txt = tk.Label(self, text="Описание:")
        self.label_txt.place(x=0, y=40)
        self.txt = tk.Text(self, width=23, height=4)
        self.entry_ip.insert(0, "")
        self.entry_ip.place(x=70, y=20)
        self.txt.insert(1.0, "")
        self.txt.place(x=4, y=60)
        # Если нужно - заполняем
        self.position_x, self.position_y = coord
        self.objectDict = objectDict
        self.element = element
        if element:  #  Если передан указатель на Объект то берем данные из него
            self.entry_ip.insert(0, self.objectDict.dict_object[element].ip_adr)
            self.txt.insert(1.0, self.objectDict.dict_object[element].descr)
            self.work_status = self.objectDict.dict_object[element].work_status
        else:  # Если нет, то создается новый Объект
            self.work_status = False
            self.entry_ip.insert(0, '.')
        # Создаем чекбокс для контроля вкл-выкл Объекта
        self.enabled_on = "Включено"
        self.enabled_off = "Отключено"
        self.chk_enabled = tk.StringVar(value=(self.enabled_off,self.enabled_on)[self.work_status])
        self.chk = ttk.Checkbutton(self, textvariable=self.chk_enabled, variable=self.chk_enabled, offvalue=self.enabled_off, onvalue=self.enabled_on)
        self.chk.place(x=4, y=135)
        self.button_ok = tk.Button(self, text="Сохранить", width=10, command=self.button_save)
        self.button_ok.place(x=10, y=160)
        self.button_ok = tk.Button(self, text="Отмена", width=10, command=self.button_cansel)
        self.button_ok.place(x=100, y=160)

    def button_save(self):
        # Кнопка - сохранить
        _new_ip = self.entry_ip.get()
        for __ in self.objectDict.dict_object.keys():

            if not re.fullmatch("^[0-9]{3}.[0-9]{1,3}$", _new_ip):
                mb.showwarning("Внимание!", "Не корректный IP адрес")
                return
            if self.objectDict.dict_object[__].ip_adr == _new_ip:
                if self.element and self.objectDict.dict_object[self.element].ip_adr == _new_ip:
                    continue
                mb.showwarning("Внимание!", "Устройство с таким IP существует")
                return

        ini_block = [self.entry_ip.get(),
                     self.position_x,
                     self.position_y,
                     self.txt.get(1.0,"end"),
                     False,
                     0,
                     (True, False)[self.chk_enabled.get() == self.enabled_off]]
        if self.element:  # Если был передан номер элемента, то редактируем его
            self.objectDict.dict_object[self.element].ip_adr = ini_block[0]
            self.objectDict.dict_object[self.element].descr = ini_block[3]
            self.objectDict.dict_object[self.element].work_status = ini_block[6]
            self.main_canvas.itemconfigure(self.objectDict.dict_object[self.element].label, text=ini_block[0])
        else:  # Если нет, то создаем новый Объект
            new_device = Object(self.main_canvas, ini_block, self.delta_x, self.objectDict)
            self.objectDict.dict_object[new_device.oval] = new_device

        self.destroy()

    def button_cansel(self):
        # Кнопка - отменить
        self.destroy()


