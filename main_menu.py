# Верхнее меню
import tkinter as tk
import saveload as sl
from description import Descr
from window_history import History


class MainMenu:
    def __init__(self, root, map, info, dict_object, del_object):
        self.info = info  # Ссылка на инфофрейм
        self.root = root  # Ссылка на головное окно
        self.main_canvas = map.main_canvas  # Ссылка на канву
        self.map = map  # Ссылка на главный фрейм
        self.dict_object = dict_object  # Ссылка на словарь объектов
        self.del_oblect = del_object  # Ссылка на словарь удаляемых объектов
        # Создаем меню
        self.main_menu = tk.Menu(root)
        root.config(menu=self.main_menu)
        # Связываем пункты меню с событиями
        self.main_menu.add_command(label="Сохранить", command=self.save_object)
        self.main_menu.add_command(label="Удалить", command=self.del_object)
        self.main_menu.add_command(label="Редактировать", command=self.edit_object)
        self.main_menu.add_command(label="Обновить", command=self.reboot_object)
        self.main_menu.add_command(label="История", command=self.history_object)

    def history_object(self):
            descr = History(self.root)
            _, x, y = self.root.geometry().split('+')
            descr.geometry(f"400x500+{int(x) + 100}+{int(y) + 100}")
            descr.grab_set()
            descr.wait_window()


    def reboot_object(self):
        # Включаем флаг на перезагрузку
        self.map.reboot_ping = True

    def save_object(self):
        # Сохраняем объекты
        sl.save_ini(self.dict_object)
        # Выводим служебное сообщение внизу слева
        self.info.title_left_down_text.set("Сохранено")

    def del_object(self):
        # Удаляем объекты с канвы
        for _ in self.del_oblect.keys():

            self.main_canvas.delete(self.del_oblect[_])  # Удаляем прямоугольник выделения
            self.main_canvas.delete(self.dict_object[_].red_oval)  # Удаляем выделение
            self.main_canvas.delete(_)  # Удаляем объект
            self.dict_object.pop(_)  # Удаляем из словаря
        self.del_oblect.clear()  # Очищаем словарь
        # Выводим служебное сообщение внизу слева
        self.info.title_left_down_text.set("Удалено")

    def edit_object(self):
        # Редактирование описания объектов
        for obj in self.del_oblect.keys():
            descr = Descr(self.root, ip_adr=self.dict_object[obj].ip_adr, descr=self.dict_object[obj].descr)
            _, x, y = self.root.geometry().split('+')
            descr.geometry(f"200x180+{int(x) + 100}+{int(y)+100}")
            descr.grab_set()
            descr.wait_window()
            # Если в форме была нажата кнопка сохранить
            if descr.button:
                self.dict_object[obj].ip_adr = descr.ip_adr
                self.dict_object[obj].descr = descr.descr
                self.main_canvas.itemconfigure(self.dict_object[obj].label, text=descr.ip_adr)
                self.info.title_left_down_text.set("Описание изменено")
