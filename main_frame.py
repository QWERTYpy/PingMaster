# Создание интерфейса пользователя
import os.path
import tkinter as tk
from PIL import Image, ImageTk
from device import Device
from object import Object
from main_menu import MainMenu

class MainFrame(tk.Frame):
    def __init__(self, root, map_width, map_height, dict_object):
        super().__init__(root)
        self.main_window_w = map_width
        self.delta = 2  # Коэффициент увеличения
        self.delta_x = 1  # Текущая кратность
        self.dict_object = dict_object
        self.load_map(map_width, map_height)


    def load_map(self, map_width, map_height):
        frame_map = tk.Frame(bg='white', bd=2)
        frame_map.place(x=0, y=0, width=map_width+25, height=map_height+25)
        # Создаем ползунки
        self.main_vscroll = tk.Scrollbar(frame_map, orient=tk.VERTICAL)
        self.main_hscroll = tk.Scrollbar(frame_map, orient=tk.HORIZONTAL)
        self.main_canvas = tk.Canvas(frame_map, height=map_height, width=map_width,
                                     xscrollcommand=self.main_hscroll.set,
                                     yscrollcommand=self.main_vscroll.set)
        self.main_vscroll.config(command=self.main_canvas.yview)
        self.main_hscroll.config(command=self.main_canvas.xview)
        self.main_vscroll.place(in_=self.main_canvas, relx=1.0, relheight=1.0, bordermode="outside")
        self.main_hscroll.place(in_=self.main_canvas, relx=0.0, rely=1.0, relwidth=1.0, bordermode="outside")
        self.main_canvas.configure(background='#ffffff')
        self.main_images = Image.open("images/main.jpg")  # Открываем картинку
        self.im_ratio = round(self.main_images.width / self.main_images.height,
                              0)  # Получаем отношение сторон изображения
        # Подгоняем картинку к размеру окна
        # self.images_resize_w//self.main_window_w
        images_resize_h = int(map_width / self.im_ratio)
        images_resize_w = map_width
        # print(frame_map.winfo_width(),frame_map.)
        # Создаем отдельный экземпляр изображения, чтобы потом можно было ресайзить не подгружая
        self.main_images_copy = self.main_images.resize((images_resize_w, images_resize_h),
                                                        Image.LANCZOS)  # Изменяем размер
        self.main_canvas.config(scrollregion=f"0 0 {self.main_images_copy.width} {self.main_images_copy.height}")
        self.main_images_pi = ImageTk.PhotoImage(self.main_images_copy)
        self.main_canvas.create_image(0, 0, anchor='nw', image=self.main_images_pi)  # Размещаем
        self.main_canvas.place(x=0, y=0)
        # Задаем реакции
        self.main_canvas.bind("<MouseWheel>", self.mousewheel)
        self.main_canvas.bind("<Button-3>", self.right_button_click)

    def mousewheel(self,event):
        """
        Действия при прокрутке ролика мышки
        :param event:
        :return:
        """
        height = self.main_images_copy.height
        width = self.main_images_copy.width
        # print(self.main_window_w - 200, width, self.main_images.height)
        # delta = int(round(height*0.05,0))
        if event.delta > 0 and width < self.main_images.width:
            images_resize_h = height*2
            images_resize_w = (height*2) * self.im_ratio
            self.delta_x *= 2
            for _ in self.dict_object.keys():
                self.dict_object[_].resize(self.delta_x)

        elif event.delta < 0 and width > self.main_window_w:
            self.delta_x/=2
            images_resize_h = height/2
            images_resize_w = height*self.im_ratio/2
            for _ in self.dict_object.keys():
                self.dict_object[_].resize(self.delta_x)

        else:
            return

        size = (int(images_resize_w), int(images_resize_h))
        # print(size)
        self.main_images_copy = self.main_images.resize(size, Image.ANTIALIAS)
        self.main_canvas.config(scrollregion=f"0 0 {self.main_images_copy.width} {self.main_images_copy.height}")
        self.main_images_pi = ImageTk.PhotoImage(self.main_images_copy)
        self.main_canvas.create_image(0, 0, anchor='nw', image=self.main_images_pi)
        # self.main_canvas.tag_raise(self.oval)
        # Поднимаем все объекты над канвой
        for _ in self.dict_object.keys():
            self.main_canvas.tag_raise(_)
        # print(self.main_canvas.find_all())

    def right_button_click(self, event, element = None):
        """
        Обработка правого щелчка мышки
        :param event:
        :return:
        """
        self.right_menu = tk.Menu(self.main_canvas, tearoff=0)
        if element is None:
            print("p")
            self.right_menu.add_command(label="Создать", command=self.create_object)
        else:
            # print("o")
            self.right_menu.add_command(label="Удалить", command = lambda el=element: self.del_object(el))
                                        # command=self.del_object)
        self.position_cursor_old_x = event.x
        self.position_cursor_old_y = event.y
        # self.left_position_hscroll, self.right_position_hscroll = self.main_hscroll.get()
        # self.left_position_vscroll, self.right_position_vscroll = self.main_vscroll.get()
        self.right_menu.post(event.x_root, event.y_root)


    def create_object(self):
        """
        Создание новых объектов
        :return:
        """
        print("Создание")
        # Преобразуем координаты окна в координаты канвы
        self.set_position_x = self.main_canvas.canvasx(self.position_cursor_old_x)
        self.set_position_y = self.main_canvas.canvasy(self.position_cursor_old_y)
        # print(self.set_position_x, self.position_cursor_old_x)
        # print(di)
        # print(x,y)
        # Создаем новое устройство и сохраняем
        new_device = Object(self.main_canvas, self.set_position_x, self.set_position_y, self.delta_x)
        self.dict_object[new_device.oval] = new_device
        print(self.dict_object)
        # # Создаем точку и назначаем для нее действия
        # self.oval = self.main_canvas.create_oval((x - 1) * self.delta_x, (y - 1) * self.delta_x, (x + 1) * self.delta_x,
        #                                          (y + 1) * self.delta_x, fill='red')
        # self.dict_device[f"{self.oval}"] = Device()
        # self.dict_device[f"{self.oval}"].set(x, y)
        # self.main_canvas.tag_bind(self.oval, "<Button-1>",
        #                           lambda event, element=self.oval: self.name_obj(event, element))
        # self.main_canvas.tag_bind(self.oval, "<Button-3>",
        #                           lambda event, element=self.oval: self.right_button_click(event, element))


