import tkinter as tk
from PIL import Image, ImageTk
# from device import Device
from object import Object
from main_menu import MainMenu

class InfoFrame(tk.Frame):
    def __init__(self, root, map_width, map_height):
        super().__init__(root)
        self.load_info(map_width, map_height)

    def load_info(self, map_width, map_height):
        frame_map = tk.Frame(bg='gray90', bd=2)
        frame_map.place(x=0, y=585, width=map_width, height=map_height)
        # Добавляем инормационное поле
        self.title_left_down_text = tk.StringVar()
        self.title_left_down_text.set("Привет")
        self.title_left_down = tk.Label(frame_map, anchor="w", height=1, width=50, textvariable=self.title_left_down_text)
        self.title_left_down.place(relx=0, rely=0)

