import time
import tkinter as tk
from ping3 import ping
import datetime
import threading
import history as hs
from object import Object, ObjectDict


class InfoFrame(tk.Frame):
    def __init__(self, type_frame, root, mainframe, objectDict: ObjectDict, map_width, map_height,
                 obj_info=None, inform=None, stat=None):
        self.map = mainframe
        self.objectDict = objectDict
        self.main_canvas = mainframe.main_canvas
        self.dict_object: dict[int, Object] = objectDict.dict_object
        self.ms_time = 1800000  # Задержка пинга 30 минут
        self.ms_time_delta = 0  # Накопитель для обратного отсчета
        self.root = root
        super().__init__(root)
        if type_frame == 'info':  # Создаем информационное поле внизу слева
            self.load_info(map_width, map_height)
        if type_frame == 'stat':  # Создаем окно статистики
            self.load_stat(map_width, map_height)
        if type_frame == 'ping':  # Создаем поле для вывода пинга
            self.obj_info = obj_info
            self.info = inform
            self.stat = stat
            self.object_name = ""
            self.ping_info(map_width, map_height)
        if type_frame == 'obj':  # Создаем поле для вывода описания
            self.object_info(map_width, map_height)

    def load_info(self, map_width, map_height):
        """
        Создаем информационное поле для вывода служебной информации
        :param map_width: Ширина фрейма
        :param map_height: Высота фрейма
        :return:
        """
        # Создаем информационное поле внизу программы
        frame_map = tk.Frame(bg='gray90', bd=2)
        frame_map.place(x=0, y=585, width=map_width, height=map_height)
        # Добавляем информационное поле
        self.title_left_down_text = tk.StringVar()
        self.title_left_down_text.set("Привет")
        self.title_left_down = tk.Label(frame_map, anchor="w", height=1, width=50,
                                        textvariable=self.title_left_down_text)
        self.title_left_down.place(relx=0, rely=0)

    def load_stat(self, map_width, map_height):
        """
        Создаем информационное поле для вывода статистики по объектам
        :param map_width:
        :param map_height:
        :return:
        """
        # Создаем информационное поле внизу программы
        frame_map = tk.Frame(bg='gray90', bd=2)
        frame_map.place(x=350, y=585, width=map_width, height=map_height)
        # Добавляем информационное поле
        self.stat = tk.Text(frame_map, width=44, height=1)
        self.stat.tag_config('on', font=('Times New Roman', 10, 'bold'), foreground="green")
        self.stat.tag_config('off', font=('Times New Roman', 10, 'bold'), foreground="red")
        self.stat.tag_config('all', font=('Times New Roman', 10, 'bold'), foreground="black")
        self.stat.tag_config('break', font=('Times New Roman', 10, 'bold'), foreground="grey")
        self.stat.place(relx=0, rely=0)

    def object_info(self, map_width, map_height):
        """
        Поле для вывода описания объекта
        :param map_width:
        :param map_height:
        :return:
        """
        # Создаем информационное поле для вывода информации о объекте
        frame_map = tk.Frame(bg='gray90', bd=2)
        frame_map.place(x=1025, y=400, width=map_width, height=map_height)
        self.obj_info_text = tk.Text(frame_map, width=26, height=10)
        self.obj_info_text.tag_config('head', font=('Times New Roman', 12, 'bold'))
        self.obj_info_text.place(relx=0, rely=0)

    def ping_info(self, map_width, map_height):
        # Создаем информационное поле для вывода информации о пинге
        frame_map = tk.Frame(bg='gray90', bd=2)
        frame_map.place(x=1025, y=0, width=map_width, height=map_height)
        # Создаем скролл для прокрутки сообщений
        self.scroll = tk.Scrollbar(frame_map, orient=tk.VERTICAL)
        # Создаем текствое поле для ввода информации о пингах
        self.text_right_info = tk.Text(frame_map, width=24, height=24, yscrollcommand=self.scroll.set)
        # Создаем теги для цветового оформления текста
        self.text_right_info.tag_config('warning', background="yellow", foreground="red")
        self.text_right_info.tag_config('new_warning', background="red", foreground="yellow")
        # self.text_right_info.tag_config('break', background="grey", foreground="black")
        self.text_right_info.tag_config('cool', background="green", foreground="black")
        self.scroll.config(command=self.text_right_info.yview)
        self.scroll.place(in_=self.text_right_info, relx=1.0, relheight=1.0, bordermode="outside")
        self.text_right_info.place(relx=0, rely=0)
        self.text_right_info.bind("<Button-1>", self.button_b1)
        self.ping_status = False  # Переменная для защиты от повторного запуска пинга
        # Запускаем пинг устройств
        self.start_ping()
        # Запускаем таймер обратного отсчета
        self.ping_timer()

    def start_ping(self):
        if not self.ping_status:
            self.ping_status = True  # Включаем флаг, что запущен пинг устройств
            self.ping_thread = threading.Thread(target=self.ping_object)
            self.ping_thread.start()
        self.aft_ping = self.after(self.ms_time, self.start_ping)

    def ping_timer(self):
        """
        Обратный таймер до начала следующего пинга
        :return:
        """
        # print(self.objectDict.reboot_ping)
        # Проверка флага на принудительный запуск пинга
        if self.objectDict.reboot_ping:  # Если нажата клавиша Обновить
            if not self.ping_status:  # Если пинг сейчас не выполняется
                self.objectDict.reboot_ping = False  # Восстанавливаем флаг
                self.after_cancel(self.aft_ping)  # Отменяем отложенный запуск
                self.start_ping()  # Запускаем новую итерацию

        if not self.ping_status:  # Если не производится пинг, то выводим обратный отсчет
            print_time = self.ms_time / 1000 - self.ms_time_delta
            self.info.title_left_down_text.set(f"Осталось: {int(print_time)} c.")
            self.ms_time_delta += 1
        # Взводим таймер на 1 секунду
        self.after(999, self.ping_timer)

    def ping_object(self):
        # Опрос устройств
        self.info.title_left_down_text.set(f"Выполняется опрос устройств ...")
        len_dict_object = len(self.dict_object)
        _count_dict_object = 0
        # Обновляем статистику по объектам
        self.stat_info()
        for _ in self.dict_object.keys():

            if self.objectDict.reboot_ping:  # Если нажата клавиша Обновить, то прерываем опрос
                break
            if not self.dict_object[_].work_status:  # Если устройство отключено берем следующее
                if not self.dict_object[_].grey_oval:
                    self.dict_object[_].setcolor_grey()
                continue
            self.dict_object[_].setcolor_grey()
            _count_dict_object += 1
            # Составляем IP адрес устройства и пингуем его
            ping_result = ping("10.64." + self.dict_object[_].ip_adr)
            ping_result_bool = True  # Пинг прошёл
            if ping_result is None or type(ping_result) is not float:
                ping_result_bool = False
            if ping_result_bool:
                # Если пинг прошел, отображаем значек зеленым
                #self.map.main_canvas.itemconfig(_, fill="green")
                # Включаем флаг, что устройство на связи
                if not self.dict_object[_].ping_status:
                    self.dict_object[_].ping_status = True
                    hs.add_in_log(f"{self.dict_object[_].ip_adr} - ON - {time.time()}")
                #Выставляем цвет
                self.dict_object[_].setcolor_RG()
            else:
                # Если нет
                # Выключаем флаг, что устройство на связи, записываем время ухода
                if self.dict_object[_].ping_status:
                    self.dict_object[_].ping_status = False
                    self.dict_object[_].ping_off = time.time()
                    hs.add_in_log(f"{self.dict_object[_].ip_adr} - OFF - {self.dict_object[_].ping_off}")
                # Выставляем цвет
                self.dict_object[_].setcolor_RG()
            # Обновляем данные в таблице
            self.ping_object_info()
            # Обновляем данные в поле статистики
            self.stat_info()
            # Обновлаяем данные о количестве
            self.info.title_left_down_text.set(
                f"Выполняется опрос устройств ... {_count_dict_object} из {len_dict_object}")

        # Выключаем флаг, что идет опрос устройств
        self.ping_status = False
        self.ms_time_delta = 0

    def stat_info(self):
        self.stat.stat.delete(1.0, tk.END)
        self.stat.stat.insert(tk.INSERT, f"Всего: {len(self.dict_object)}  ", 'all')
        _on = 0
        _off = 0
        _break = 0
        for _ in self.dict_object.values():
            if _.work_status and _.ping_status:
                _on += 1
            elif _.work_status and not _.ping_status:
                _off += 1
            elif not _.work_status:
                _break += 1
        self.stat.stat.insert(tk.INSERT, f"На связи: {_on}  ", 'on')
        self.stat.stat.insert(tk.INSERT, f"Отсутсвуют: {_off}  ", 'off')
        self.stat.stat.insert(tk.INSERT, f"Отключены: {_break}  ", 'break')

    def ping_object_info(self):
        # Отображение статистики устройств
        self.text_right_info.configure(state='normal')
        self.text_right_info.delete(1.0, tk.END)

        _dict_ping_info = {}  # Создаем словарь для вывода данных
        for __ in self.dict_object.values():  # Создаем его отсутствующими устройвами
            if not __.ping_status and __.work_status:
                _dict_ping_info[__.ip_adr] = [__.ping_off, __.oval]
        # Сортируем в порядке возрастания времени отсуствия
        _dict_ping_info = sorted(_dict_ping_info.items(), key=lambda item: item[1][0], reverse=True)

        # Создаем цветовое оформление
        for __ in _dict_ping_info:
            time_out = datetime.timedelta(seconds=int(time.time() - __[1][0]))
            time_delta = datetime.timedelta(hours=2)
            # print(__[0])
            if time_out < time_delta:
                color_text = "new_warning"
                self.map.main_canvas.itemconfig(self.dict_object[__[1][1]].red_oval, outline="red")
            else:
                color_text = "warning"
                self.map.main_canvas.itemconfig(self.dict_object[__[1][1]].red_oval, outline="orange")

            _str_day = time_out.days
            _str_time = time.strftime("%H:%M:%S", time.gmtime(time_out.seconds))
            str_time_out = f"{_str_day:4} д. {_str_time[:-3]}"
            self.text_right_info.insert(tk.INSERT,
                                            f"{__[0]:7} - {str_time_out}\n",
                                            color_text)
        self.text_right_info.configure(state='disabled')
        # self.text_right_info.update()
        # self.main_canvas.update()

    def button_b1(self, event):
        # print(event.x, event.y)
        if len(self.text_right_info.get(1.0, tk.END)) - 1:
            # Получаем номер строки из координат курсора
            index, _ = event.widget.index("@%s,%s" % (event.x, event.y)).split('.')
            # Получаем строку и отделяем IP
            self.object_name, _ = self.text_right_info.get(f"{index}.0", f"{index}.{tk.END}").split('-')
            self.object_name = self.object_name.strip()
            # print(self.object_name)
            # Ищем объект в общем списке
            for _ in self.dict_object.keys():
                #  Если в списке есть выбранный ip адрес, то выводим информацию
                if self.dict_object[_].ip_adr == self.object_name:
                    self.obj_info.obj_info_text.configure(state='normal')
                    self.obj_info.obj_info_text.delete(1.0, tk.END)
                    self.obj_info.obj_info_text.insert(tk.INSERT, "IP Адрес\n", 'head')
                    self.obj_info.obj_info_text.insert(tk.INSERT, f"10.64.{self.dict_object[_].ip_adr}\n")
                    self.obj_info.obj_info_text.insert(tk.INSERT, "Описание\n", 'head')
                    self.obj_info.obj_info_text.insert(tk.INSERT, f"{self.dict_object[_].descr}\n")
                    self.obj_info.obj_info_text.configure(state='disabled')
                    # Получаем координаты объекта
                    _x, _y, _x1, _y1 = self.main_canvas.coords(_)
                    # Создаем анимацию на канве для отображения места объекта
                    for _crat in range(200, 0, -4):
                        if _crat == 200:
                            rect = self.main_canvas.create_rectangle(_x - _crat, _y - _crat, _x1 + _crat, _y1 + _crat)
                        else:
                            self.main_canvas.coords(rect, _x - _crat, _y - _crat, _x1 + _crat, _y1 + _crat)
                            self.main_canvas.update()
                            time.sleep(0.005)
                    self.main_canvas.delete(rect)
