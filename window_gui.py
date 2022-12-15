# Создание интерфейса пользователя
import os.path
import tkinter as tk
from PIL import Image, ImageTk
from device import Device
import configparser

class Window:
    def __init__(self):
        self.list_device = []
        self.dict_device = {}
        self.root = tk.Tk()
        self.main_window_w = 1200  # Ширина программы
        self.main_window_h = 600  # Высота программы
        self.delta = 2  # Коэффициент увеличения
        self.delta_x = 1  # Текущая кратность
        self.root.title("Ping Master - start")  # Заголовок окна
        self.root.geometry(f"{self.main_window_w}x{self.main_window_h}+100+100")  # Создаем окно
        self.root.resizable(False, False)  # Запрещаем изменять размер окна
        self.root.configure(background='#ffffff')
        # Создаем главное меню
        self.main_menu()
        # # Создаем контекстное меню
        # self.r_menu()
        # Добавляем канву с ползунками
        self.canvas_scroll()
        # Добавляем инормационное поле
        self.title_left_down_text = tk.StringVar()
        self.title_left_down_text.set("Привет")
        self.title_left_down = tk.Label(self.root, anchor="w", height=1, width=50, textvariable=self.title_left_down_text)


        self.title_left_down.place(x=0,y=580)
        # Подгружаем изображение
        self.main_images = Image.open("images/main.jpg")  # Открываем картинку
        # if self.main_images.width%2:
        #     self.images_resize_w = self.main_images.width+1
        # if self.main_images.height%2:
        #     self.images_resize_h = self.main_images.height+1
        self.im_ratio = round(self.main_images.width/self.main_images.height, 0)  # Получаем отношение сторон изображения
        # print(self.im_ratio)
        # print(self.im_ratio, main_images_height, width)
        # Подгоняем картинку к размеру окна
        # self.images_resize_w//self.main_window_w
        self.images_resize_h = int((self.main_window_w - 200) / self.im_ratio)
        self.images_resize_w = self.main_window_w - 200
        # Создаем отдельный экземпляр изображения, чтобы потом можно было ресайзить не подгружая
        self.main_images_copy = self.main_images.resize((self.images_resize_w, self.images_resize_h), Image.LANCZOS)  # Изменяем размер
        self.main_canvas.config(scrollregion=f"0 0 {self.main_images_copy.width} {self.main_images_copy.height}")
        # Создаем копию изображения для дальнейшей работы

        self.main_images_pi = ImageTk.PhotoImage(self.main_images_copy)
        self.main_canvas.create_image(0, 0, anchor='nw', image=self.main_images_pi)  # Размещаем
        self.main_canvas.place(x=0, y=0)

        # self.root.bind("<Configure>", self.resize)  # Отрисовка при изменении геометрии окна. Пока отключена.
        # self.root.bind("<Motion>", self.left_button)
        # Обрабатываем действия пользователя
        self.bind()

    # def r_menu(self):
    #     """
    #     Контекстное меню по правой кнопке мышки
    #     :return:
    #     """
    #     self.right_menu = tk.Menu(self.root, tearoff=0)
    #     self.right_menu.add_command(label="Создать", command=self.create_object)
    #     self.right_menu.add_command(label="Удалить", command=self.del_object)

    def del_object(self,element):
        self.main_canvas.delete(element)
        # self.list_device.pop()

    def name_obj(self, event, element):
        # print(element)
        # self.main_canvas.delete(element-2)
        # print(self.main_canvas.find_all()) #показывает все ID
        print(self.main_canvas.coords(self.oval))
    def create_object(self):
        """
        Создание новых объектов
        :return:
        """
        print("Создание")
        # # Преобразование координат для точного позиционирования при увеличении картинки
        # self.set_position_x = round(self.left_position_hscroll*self.images_resize_w, 0)+self.position_cursor_old_x
        # self.set_position_y = round(self.left_position_vscroll*self.images_resize_h, 0)+self.position_cursor_old_y
        # Преобразуем координаты окна в координаты канвы
        self.set_position_x = self.main_canvas.canvasx(self.position_cursor_old_x)
        self.set_position_y = self.main_canvas.canvasy(self.position_cursor_old_y)
        # print(self.set_position_x, self.main_canvas.canvasx(self.position_cursor_old_x))

        # Создание нового объекта и назначение ему обработчиков
        x = round(self.set_position_x/self.delta_x,0)
        y = round(self.set_position_y/self.delta_x,0)
        # print(x,y)





        # Создаем точку и назначаем для нее действия
        self.oval = self.main_canvas.create_oval((x - 1) * self.delta_x, (y - 1) * self.delta_x, (x + 1) * self.delta_x,
                                                 (y + 1) * self.delta_x, fill='red')
        self.dict_device[f"{self.oval}"] = Device()
        self.dict_device[f"{self.oval}"].set(x, y)
        self.main_canvas.tag_bind(self.oval, "<Button-1>",
                                  lambda event, element=self.oval: self.name_obj(event, element))
        self.main_canvas.tag_bind(self.oval, "<Button-3>",
                                  lambda event, element=self.oval: self.right_button_click(event, element))

        # self.list_device.append((self.oval, Device()))
        # print(type(self.oval))
        # print(self.oval)
        # print(self.dict_device)
        # print(self.dict_device[f"{self.oval}"].coord)
        # print(self.list_device)
        # print(self.list_device[0][0])
        # print(self.list_device[0][1].test)

    def main_menu(self):
        # Создаем меню
        self.main_menu = tk.Menu(self.root)
        self.root.config(menu=self.main_menu)
        self.main_menu.add_command(label="Сохранить", command=self.save_onject)

    def save_onject(self):
        # # if os.path.exists("ip_config.ini"):
        # config = configparser.ConfigParser()
        # for _ in self.dict_device.keys():
        #     # print(self.main_canvas.move(_, delta, delta))
        #     x, y = self.dict_device[_].coord
        self.title_left_down_text.set("Сохранено")

    def canvas_scroll(self):
        # Создаем ползунки
        self.main_vscroll = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.main_hscroll = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.main_canvas = tk.Canvas(self.root, height=self.main_window_h - 40, width=self.main_window_w - 200,
                                     xscrollcommand=self.main_hscroll.set,
                                     yscrollcommand=self.main_vscroll.set)
        self.main_vscroll.config(command=self.main_canvas.yview)
        self.main_hscroll.config(command=self.main_canvas.xview)
        self.main_vscroll.place(in_=self.main_canvas, relx=1.0, relheight=1.0, bordermode="outside")
        self.main_hscroll.place(in_=self.main_canvas, relx=0.0, rely=1.0, relwidth=1.0, bordermode="outside")
        self.main_canvas.configure(background='#ffffff')

    def bind(self):
        """
        Обработчики событий
        :return:
        """
        self.root.bind("<MouseWheel>", self.mousewheel)
        self.root.bind("<B3-Motion>", self.move_img)
        self.root.bind("<Button-3>", self.right_button_click)
        # self.main_canvas.tag_bind(self.main_images_pi,"<Button-3>", self.right_button_click)
        #self.root.bind("<Button-3>", lambda event: self.menu.post(event.x_root, event.y_root))


    def right_button_click(self, event, element = None):
        """
        Обработка правого щелчка мышки
        :param event:
        :return:
        """
        self.right_menu = tk.Menu(self.root, tearoff=0)
        if element is None:
            # print("p")
            self.right_menu.add_command(label="Создать", command=self.create_object)
        else:
            # print("o")
            self.right_menu.add_command(label="Удалить", command = lambda el=element: self.del_object(el))
                                        # command=self.del_object)




        self.position_cursor_old_x = event.x
        self.position_cursor_old_y = event.y
        self.left_position_hscroll, self.right_position_hscroll = self.main_hscroll.get()
        self.left_position_vscroll, self.right_position_vscroll = self.main_vscroll.get()
        self.right_menu.post(event.x_root, event.y_root)
        # print(self.position_cursor_old_x, self.position_cursor_old_y)


    # def left_button(self, event):
    #     """
    #     Действия при нажатии левой кнопки мышки
    #     :param event:
    #     :return:
    #     """
    #     self.after_resize()
    #
    # def after_resize(self):
    #     self.width_window = self.root.winfo_width()
    #     self.height_window = self.root.winfo_height()
    #     print("press")


    def move_img(self, event):
        if event.x > self.position_cursor_old_x:
            self.main_canvas.xview_scroll(number=1, what="units")
            # x_l, x_h = self.main_hscroll.get()
            # self.main_hscroll.set(x_l+0.1,x_h+0.1)
            self.position_cursor_old_x = event.x
        if event.x < self.position_cursor_old_x:
            self.main_canvas.xview_scroll(number=-1, what="units")
            self.position_cursor_old_x = event.x
        if event.y > self.position_cursor_old_y:
            self.main_canvas.yview_scroll(number=1, what="units")
            self.position_cursor_old_y = event.y
        if event.y < self.position_cursor_old_y:
            self.main_canvas.yview_scroll(number=-1, what="units")
            self.position_cursor_old_y = event.y
        # print(self.main_hscroll.get())
        # self.main_canvas.yview_scroll(number=1, what="units")
        # self.main_canvas.tag_raise(self.oval)



    def mousewheel(self,event):
        """
        Действия при прокрутке ролика мышки
        :param event:
        :return:
        """

        height = self.main_images_copy.height
        width = self.main_images_copy.width
        print(self.main_window_w - 200, width, self.main_images.height)
        delta = int(round(height*0.05,0))
        if event.delta > 0 and width < self.main_images.width:
            self.images_resize_h = height*2
            self.images_resize_w = (height*2) * self.im_ratio
            self.delta_x *= 2
            for _ in self.dict_device.keys():
                # print(self.main_canvas.move(_, delta, delta))
                x,y = self.dict_device[_].coord
                x*=self.delta_x
                y*=self.delta_x
                self.main_canvas.coords(_, x-self.delta_x, y-self.delta_x, x+self.delta_x, y+self.delta_x)
                self.main_canvas.tag_raise(_)

        elif event.delta < 0 and width > self.main_window_w - 200:
            self.delta_x/=2
            self.images_resize_h = height/2
            self.images_resize_w = height*self.im_ratio/2
            for _ in self.dict_device.keys():
                # print(self.main_canvas.move(_,-delta,-delta))
                x, y = self.dict_device[_].coord
                x *= self.delta_x
                y *= self.delta_x
                self.main_canvas.coords(_, x - self.delta_x, y - self.delta_x, x + self.delta_x, y + self.delta_x)
                self.main_canvas.tag_raise(_)

        size = (int(self.images_resize_w), int(self.images_resize_h))
        print(size)
        self.main_images_copy = self.main_images.resize(size, Image.ANTIALIAS)
        self.main_canvas.config(scrollregion=f"0 0 {self.main_images_copy.width} {self.main_images_copy.height}")
        self.main_images_pi = ImageTk.PhotoImage(self.main_images_copy)
        self.main_canvas.create_image(0, 0, anchor='nw', image=self.main_images_pi)
        # self.main_canvas.tag_raise(self.oval)
        # Поднимаем все объекты над канвой
        for _ in self.dict_device.keys():
            self.main_canvas.tag_raise(_)









    def resize(self, event):
        """
        Действия при изменении размера окна приложения
        :param event:
        :return:
        """
        size = (event.width, event.main_images_height)
        # print(size, self.root.winfo_reqwidth(), self.root.winfo_width())
        # print(self.root.winfo_height())
        # self.main_images = Image.open("images/main.jpg")
        # self.main_images = self.main_images.resize(size, Image.ANTIALIAS)
        # self.main_images_pi = ImageTk.PhotoImage(self.main_images)
        # self.display.delete("IMG")
        self.main_canvas.config(height=self.root.winfo_height()-20, width=self.root.winfo_width()-20)
        self.main_canvas.create_image(0, 0, anchor='nw', image=self.main_images_pi)

    def mainloop(self):
        """
        Запуск
        :return:
        """
        self.root.mainloop()  # Запускает цикл событий
