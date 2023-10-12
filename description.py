import tkinter as tk
from tkinter import ttk
# Всплывающее меню при создании или редактировании информации о объекте
class Descr(tk.Toplevel):
    def __init__(self, parent, ip_adr="", descr="", work=False):
        super().__init__(parent)
        self.button = None
        self.ip_adr = ip_adr
        self.descr = descr
        self.work_status = work
        self.label_dsc = tk.Label(self, text="Добавьте описание:")
        self.label_dsc.place(x=0, y=0)
        self.label_ip = tk.Label(self, text="IP адрес:")
        self.label_ip.place(x=0, y=20)
        self.entry_ip = tk.Entry(self, width=20)
        self.entry_ip.insert(0, self.ip_adr)
        self.entry_ip.place(x=70, y=20)
        self.label_txt = tk.Label(self, text="Описание:")
        self.label_txt.place(x=0, y=40)
        self.txt = tk.Text(self, width=23, height=4)
        self.txt.insert(1.0, self.descr)
        self.txt.place(x=4,y=60)
        # self.chk_enabled = tk.IntVar()
        # self.chk_enabled.set(0)
        self.enabled_on = "Включено"
        self.enabled_off = "Отключено"
        self.chk_enabled = tk.StringVar(value=(self.enabled_off,self.enabled_on)[self.work_status])
        self.chk = ttk.Checkbutton(self, textvariable=self.chk_enabled, variable=self.chk_enabled, offvalue=self.enabled_off, onvalue=self.enabled_on)
        self.chk.place(x=4,y=135)
        self.button_ok = tk.Button(self, text="Сохранить", width=10, command=self.button_save)
        self.button_ok.place(x=10, y=160)
        self.button_ok = tk.Button(self, text="Отмена", width=10, command=self.button_cansel)
        self.button_ok.place(x=100, y=160)

    def button_save(self):
        # Кнопка - сохранить
        self.button = True
        self.ip_adr = self.entry_ip.get()
        self.descr = self.txt.get(1.0, "end")
        self.work_status = (True, False)[self.chk_enabled.get() == self.enabled_off]
        self.destroy()

    def button_cansel(self):
        # Кнопка - отменить
        self.button = False
        self.destroy()


