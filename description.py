import tkinter as tk
from tkinter import ttk
from object import Object, ObjectDict
# Всплывающее меню при создании или редактировании информации об объекте
class Descr(tk.Toplevel):
    def __init__(self, parent, delta_x, coord, element = None, objectDict: ObjectDict = None):
    # def __init__(self, parent, ip_adr="", descr="", work=False):
        super().__init__(parent)
        self.delta_x = delta_x
        # Создаем все поля
        self.main_canvas = parent
        self.label_dsc = tk.Label(self, text="Добавьте описание:")
        self.label_dsc.place(x=0, y=0)
        self.label_ip = tk.Label(self, text="IP адрес:")
        self.label_ip.place(x=0, y=20)
        self.entry_ip = tk.Entry(self, width=20)
        self.label_txt = tk.Label(self, text="Описание:")
        self.label_txt.place(x=0, y=40)
        self.txt = tk.Text(self, width=23, height=4)

        self.entry_ip.insert(0, "")
        self.entry_ip.place(x=70, y=20)
        self.txt.insert(1.0, "")
        self.txt.place(x=4, y=60)
        # self.work_status = self.objectDict.dict_object[element].work_status
        # Если нужно - заполняем
        self.position_x, self.position_y = coord
        self.objectDict = objectDict
        self.element = element
        if element:
            self.entry_ip.insert(0, self.objectDict.dict_object[element].ip_adr)
            # self.entry_ip.place(x=70, y=20)
            self.txt.insert(1.0, self.objectDict.dict_object[element].descr)
            # self.txt.place(x=4, y=60)
            self.work_status = self.objectDict.dict_object[element].work_status
        else:
            self.work_status = False

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
        ini_block = [self.entry_ip.get(),
                     self.position_x,
                     self.position_y,
                     self.txt.get(1.0,"end"),
                     False,
                     0,
                     (True, False)[self.chk_enabled.get() == self.enabled_off]]
        if self.element:
            self.objectDict.dict_object[self.element].ip_adr = ini_block[0]
            self.objectDict.dict_object[self.element].descr = ini_block[3]
            self.objectDict.dict_object[self.element].work_status = ini_block[6]
        else:
            new_device = Object(self.main_canvas, ini_block, self.delta_x, self.objectDict)
            self.objectDict.dict_object[new_device.oval] = new_device
        self.destroy()

    def button_cansel(self):
        # Кнопка - отменить
        self.destroy()


