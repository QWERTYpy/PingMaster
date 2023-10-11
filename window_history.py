import tkinter as tk
import os
from datetime import datetime
# Всплывающее меню при создании или редактировании информации о объекте
class History(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.button = None
        self.label_dsc = tk.Label(self, text="История опроса:")
        self.label_dsc.place(x=0, y=0)
        _x = 10
        for history_files in self.read_history_file():
            # print(history_files)
            button_hist = tk.Button(self, text=history_files, width=8, command=lambda el=history_files: self.button_hist(el))
            button_hist.place(x=_x, y=30)
            _x += 70
        # frame_map = tk.Frame(bg='gray90', bd=2)
        # frame_map.place(x=1025, y=0, width=map_width, height=map_height)
        # Создаем скролл для прокрутки сообщений
        self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        # Создаем текствое поле для ввода информации о пингах
        self.text_history = tk.Text(self, width=45, height=24, yscrollcommand=self.scroll.set)
        # Создаем теги для цветового оформления текста
        self.text_history.tag_config('ON', background="green", foreground="black")
        self.text_history.tag_config('OFF', background="red", foreground="yellow")
        self.scroll.config(command=self.text_history.yview)
        self.scroll.place(in_=self.text_history, relx=1.0, relheight=1.0, bordermode="outside")
        self.text_history.place(x=10, y=70)

    def button_hist(self,text_button):
        self.text_history.delete(1.0, tk.END)
        with open(f"history/{text_button}.txt", "r") as f:
            while True:
                line_history = f.readline()
                if not line_history:
                    break
                line_history = line_history.split('-')
                line_history = [_.strip() for _ in line_history]
                # print(line_history[2])
                if line_history[1] == 'ON':
                    self.text_history.insert(tk.INSERT, f"{line_history[0]} - {datetime.fromtimestamp(float(line_history[2])).strftime('%H:%M:%S')}\n", 'ON')
                if line_history[1] == 'OFF':
                    self.text_history.insert(tk.INSERT, f"{line_history[0]} - {datetime.fromtimestamp(float(line_history[2])).strftime('%H:%M:%S')}\n", 'OFF')


    def read_history_file(self):
        history_files = os.listdir('history')
        history_files = [_[:-4] for _ in history_files]
        history_files = history_files[-5:]
        return history_files



