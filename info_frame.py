import tkinter as tk
from PIL import Image, ImageTk
# from device import Device
from object import Object
from main_menu import MainMenu

class InfoFrame(tk.Frame):
    def __init__(self, type, root, map_width, map_height):
        super().__init__(root)
        if type == 'info':
            self.load_info(map_width, map_height)
        if type == 'ping':
            self.ping_info(map_width, map_height)

    def load_info(self, map_width, map_height):
        # Создаем информационное поле внизу программы
        frame_map = tk.Frame(bg='gray90', bd=2)
        frame_map.place(x=0, y=585, width=map_width, height=map_height)
        # Добавляем информационное поле
        self.title_left_down_text = tk.StringVar()
        self.title_left_down_text.set("Привет")
        self.title_left_down = tk.Label(frame_map, anchor="w", height=1, width=50, textvariable=self.title_left_down_text)
        self.title_left_down.place(relx=0, rely=0)

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


