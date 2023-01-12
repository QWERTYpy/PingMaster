import time
import tkinter as tk
from ping3 import ping
import datetime
import threading


from PIL import Image, ImageTk
# from device import Device
from object import Object
from main_menu import MainMenu

class InfoFrame(tk.Frame):
    def __init__(self, type, root, map, dict_object, map_width, map_height, obj_info = None, _info = None, stat = None):
        self.map = map
        self.main_canvas = map.main_canvas
        self.dict_object = dict_object
        self.ms_time = 600000
        self.ms_time_delta = 0
        super().__init__(root)
        if type == 'info':
            self.load_info(map_width, map_height)
        if type == 'stat':
            self.load_stat(map_width, map_height)
        if type == 'ping':
            self.obj_info = obj_info
            self.info = _info
            self.stat = stat
            self.object_name = ""
            self.ping_info(map_width, map_height)
        if type == 'obj':
            self.object_info(map_width, map_height)

    def load_info(self, map_width, map_height):
        # Создаем информационное поле внизу программы
        frame_map = tk.Frame(bg='gray90', bd=2)
        frame_map.place(x=0, y=585, width=map_width, height=map_height)
        # Добавляем информационное поле
        self.title_left_down_text = tk.StringVar()
        self.title_left_down_text.set("Привет")
        self.title_left_down = tk.Label(frame_map, anchor="w", height=1, width=50, textvariable=self.title_left_down_text)
        self.title_left_down.place(relx=0, rely=0)
        # self.ping_timer()



    def load_stat(self, map_width, map_height):
        # Создаем информационное поле внизу программы
        frame_map = tk.Frame(bg='gray90', bd=2)
        frame_map.place(x=350, y=585, width=map_width, height=map_height)
        # Добавляем информационное поле
        # self.stat_text = tk.StringVar()
        # self.stat_text.set("Привет111")
        # self.stat = tk.Label(frame_map, anchor="w", height=1, width=50, textvariable=self.stat_text)
        # self.stat.place(relx=0, rely=0)
        self.stat = tk.Text(frame_map,width=40, height=1)
        self.stat.tag_config('on', font=('Times New Roman',10,'bold'), foreground="green" )
        self.stat.tag_config('off', font=('Times New Roman', 10, 'bold'), foreground="red")
        self.stat.tag_config('all', font=('Times New Roman', 10, 'bold'), foreground="black")
        self.stat.place(relx=0, rely=0)

    def object_info(self, map_width, map_height):
        # Создаем информационное поле для вывода информации о объекте
        frame_map = tk.Frame(bg='gray90', bd=2)
        frame_map.place(x=1025, y=400, width=map_width, height=map_height)
        # self.title_obj_info_text = tk.StringVar()
        # self.title_obj_info_text.set("")
        # self.title_obj_info = tk.Label(frame_map, anchor="w", height=10, width=25,
        #                                 textvariable=self.title_obj_info_text)
        # self.title_obj_info.place(relx=0, rely=0)
        self.obj_info_text = tk.Text(frame_map, width=20, height=10)
        self.obj_info_text.tag_config('head', font=('Times New Roman',12,'bold'))
        self.obj_info_text.place(relx=0, rely=0)

    def ping_info(self, map_width, map_height):
        # Создаем информационное поле для вывода информации о пинге
        frame_map = tk.Frame(bg='gray90', bd=2)
        frame_map.place(x=1025, y=0, width=map_width, height=map_height)
        # Создаем скролл для прокрутки сообщений
        self.scroll = tk.Scrollbar(frame_map, orient=tk.VERTICAL)
        # Создаем текствое поле для ввода информации о пингах
        self.text_right_info = tk.Text(frame_map, width=19, height=24, yscrollcommand=self.scroll.set)
        # Создаем теги для цветового оформления текста
        self.text_right_info.tag_config('warning', background="yellow", foreground="red")
        self.text_right_info.tag_config('cool', background="green", foreground="black")
        self.scroll.config(command=self.text_right_info.yview)
        # Для блокировки ввода
        # self.text_right_info.configure(state='disabled')
        self.scroll.place(in_=self.text_right_info, relx=1.0, relheight=1.0, bordermode="outside")
        # text.insert(INSERT, 'text' * 500)
        # self.text_right_info.insert(tk.INSERT, '0123456789ABCDEFG\n'*50)
        # self.text_right_info.configure(state='disabled')
        self.text_right_info.place(relx=0, rely=0)
        self.text_right_info.bind("<Button-1>", self.button_b1)
        self.ping_status = False
        self.start_ping()
        self.ping_timer()

    def start_ping(self):
        print("Event")
        if not self.ping_status:
            self.ping_status = True
            self.ping_thread = threading.Thread(target=self.ping_object)
            self.ping_thread.start()

        # print(t.is_alive())
        # t.join()
        self.aft_ping = self.after(self.ms_time,self.start_ping)

    def ping_timer(self):
        if self.map.reboot_ping:
            self.map.reboot_ping  = False
            self.after_cancel(self.aft_ping)
            self.start_ping()

        if not self.ping_status:
            print_time = self.ms_time/1000-self.ms_time_delta
            self.info.title_left_down_text.set(f"Осталось: {int(print_time)} c.")
            self.ms_time_delta +=1
        self.after(999, self.ping_timer)

    def ping_object(self):
        # if self.ping_thread.is_alive():
        #     print("Break")
        #     return
        print("Start Ping")
        # Опрос устройств
        self.info.title_left_down_text.set(f"Выполняется опрос устройств ...")
        # stat.stat.insert(tk.INSERT,f"qqq",'off')
        # while True:
        self.stat_info()
        # info.title_left_down_text.set(f"")
        for _ in self.dict_object.keys():
            # Составляем IP адрес устройства
            ping_result = ping("10.64." + self.dict_object[_].ip_adr)
            ping_result_bool = True  # Пинг прошёл
            if ping_result is None or type(ping_result) is not float:
                ping_result_bool = False
            if ping_result_bool:
                self.map.main_canvas.itemconfig(_, fill="green")
                if not self.dict_object[_].ping_status:
                    self.dict_object[_].ping_status = True
            else:
                self.map.main_canvas.itemconfig(_, fill="red")
                if self.dict_object[_].ping_status:
                    self.dict_object[_].ping_status = False
                    self.dict_object[_].ping_off = time.time()
            self.ping_object_info()
            self.stat_info()
        print("Stop Ping")
        self.ping_status = False
        self.ms_time_delta = 0
        # self.after(1000, self.ping_object)
            #stat_info()
        # time.sleep(600)

        # print("Ping")

    def stat_info(self):
        self.stat.stat.delete(1.0, tk.END)
        self.stat.stat.insert(tk.INSERT, f"Всего: {len(self.dict_object)}  ", 'all')
        on = 0
        off = 0
        for _ in self.dict_object.values():
            if _.ping_status:
                on += 1
            else:
                off += 1
        self.stat.stat.insert(tk.INSERT, f"На связи: {on}  ", 'on')
        self.stat.stat.insert(tk.INSERT, f"Отсутсвуют: {off}  ", 'off')

    def ping_object_info(self):
        self.text_right_info.configure(state='normal')
        self.text_right_info.delete(1.0, tk.END)
        for __ in self.dict_object.keys():
            if not self.dict_object[__].ping_status:
                self.text_right_info.insert(tk.INSERT,
                                                 f"{self.dict_object[__].ip_adr}-{datetime.timedelta(seconds=int(time.time() - self.dict_object[__].ping_off))}\n",
                                                 'warning')
        self.text_right_info.configure(state='disabled')
        # self.text_right_info.update()
        # self.main_canvas.update()

    def button_b1(self, event):
        # print(event.x, event.y)
        if len(self.text_right_info.get(1.0, tk.END))-1:
            # Получаем номер строки из координат курсора
            index, _ = event.widget.index("@%s,%s" % (event.x, event.y)).split('.')
            # Получаем строку и отделяем IP
            self.object_name, _ = self.text_right_info.get(f"{index}.0", f"{index}.{tk.END}").split('-')
            # print(self.object_name)
            # Ищем объект в общем списке
            for _ in self.dict_object.keys():
                if self.dict_object[_].ip_adr == self.object_name:
                    # print(self.object_name,"-",_)

                    # self.obj_info.title_obj_info_text.set(f"\nIP Адрес:\n10.64.{self.dict_object[_].ip_adr}\n"
                    #                              f"Описание:\n{self.dict_object[_].descr}\n")
                    self.obj_info.obj_info_text.configure(state='normal')
                    self.obj_info.obj_info_text.delete(1.0, tk.END)
                    self.obj_info.obj_info_text.insert(tk.INSERT,"IP Адрес\n", 'head')
                    self.obj_info.obj_info_text.insert(tk.INSERT, f"10.64.{self.dict_object[_].ip_adr}\n")
                    self.obj_info.obj_info_text.insert(tk.INSERT, "Описание\n", 'head')
                    self.obj_info.obj_info_text.insert(tk.INSERT, f"{self.dict_object[_].descr}\n")
                    self.obj_info.obj_info_text.configure(state='disabled')
                    # Получаем координаты объекта
                    _x, _y, _x1, _y1 = self.main_canvas.coords(_)
                    # Создаем анимацию на канве для отображения места объекта
                    for _crat in range(200,0,-4):
                        if _crat == 200:
                            rect = self.main_canvas.create_rectangle(_x-_crat, _y-_crat, _x1+_crat, _y1+_crat)
                        else:
                            self.main_canvas.coords(rect, _x-_crat, _y-_crat, _x1+_crat, _y1+_crat)
                            self.main_canvas.update()
                            time.sleep(0.005)
                    self.main_canvas.delete(rect)


