import tkinter as tk
from main_frame import MainFrame
from main_menu import MainMenu
from info_frame import InfoFrame

dict_object = {}
del_object = {}
# dict_object['a']=1
root = tk.Tk()
root.title(("Ping Master - v.1.0"))
root.geometry("1200x608+100+100")  # Создаем окно
root.resizable(False, False)  # Запрещаем изменять размер окна
root.configure(background='#ffffff')  # Устанавливаем цвет фона

map = MainFrame(root, 1000, 560, dict_object, del_object)
info = InfoFrame(root,1200,20)
MainMenu(root, map, info, dict_object, del_object)
root.mainloop()  # Запускаем отображение
# print(dict_object)