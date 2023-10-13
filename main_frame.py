# Создание интерфейса пользователя
import tkinter as tk
from PIL import Image, ImageTk
from object import Object, ObjectDict
from description import Descr
import saveload as sl


# Создает основное окно

class MainFrame(tk.Frame):
    def __init__(self, root, map_width, map_height, objectDict: ObjectDict):
        super().__init__(root)
        self.root = root
        self.main_window_w = map_width
        self.delta = 2  # Коэффициент увеличения
        self.delta_x = 1  # Текущая кратность
        self.objectDict = objectDict  # Создаем Объект со словарями
        self.load_map(map_width, map_height)

    def load_map(self, map_width, map_height):
        # Загружаем карту
        frame_map = tk.Frame(bg='white', bd=2)
        frame_map.place(x=0, y=0, width=map_width + 25, height=map_height + 25)
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
        images_resize_h = int(map_width / self.im_ratio)
        images_resize_w = map_width
        # Создаем отдельный экземпляр изображения, чтобы потом можно было ресайзить не подгружая
        self.main_images_copy = self.main_images.resize((images_resize_w, images_resize_h),
                                                        Image.LANCZOS)  # Изменяем размер
        self.main_canvas.config(scrollregion=f"0 0 {self.main_images_copy.width} {self.main_images_copy.height}")
        self.main_images_pi = ImageTk.PhotoImage(self.main_images_copy)
        self.main_canvas.create_image(0, 0, anchor='nw', image=self.main_images_pi)  # Размещаем
        self.main_canvas.place(x=0, y=0)
        # Загружаем объекты из файла конфигурации
        for ini_block in sl.load_ini():
            new_device = Object(self.main_canvas, ini_block, self.delta_x, self.objectDict)
            new_device.setcolor()  # Устанавливаем цвет метки
            self.objectDict.dict_object[new_device.oval] = new_device  # Добавляем созданное устройство в словарь
        # Задаем реакции
        self.main_canvas.bind("<MouseWheel>", self.mousewheel)
        self.main_canvas.bind("<Button-3>", self.right_button_click)

    def mousewheel(self, event):
        """
        Действия при прокрутке ролика мышки
        :param event:
        :return:
        """
        height = self.main_images_copy.height
        width = self.main_images_copy.width
        # Если надо увеличить и текущий размер меньше размера картинки
        if event.delta > 0 and width < self.main_images.width:
            images_resize_h = height * 2
            images_resize_w = (height * 2) * self.im_ratio
            self.delta_x *= 2
            for _ in self.objectDict.dict_object.keys():
                self.objectDict.dict_object[_].resize(self.delta_x)
        # Если надо уменьшить и текущий размер больше размера окна
        elif event.delta < 0 and width > self.main_window_w:
            self.delta_x /= 2
            images_resize_h = height / 2
            images_resize_w = height * self.im_ratio / 2
            for _ in self.objectDict.dict_object.keys():
                self.objectDict.dict_object[_].resize(self.delta_x)
        else:
            return

        size = (int(images_resize_w), int(images_resize_h))
        self.main_images_copy = self.main_images.resize(size, Image.LANCZOS)
        self.main_canvas.config(scrollregion=f"0 0 {self.main_images_copy.width} {self.main_images_copy.height}")
        self.main_images_pi = ImageTk.PhotoImage(self.main_images_copy)
        self.main_canvas.create_image(0, 0, anchor='nw', image=self.main_images_pi)
        # Поднимаем все объекты над канвой
        for _ in self.objectDict.dict_object.keys():
            self.main_canvas.tag_raise(_)
            if self.objectDict.dict_object[_].red_oval:
                self.main_canvas.tag_raise(self.objectDict.dict_object[_].red_oval)
            # Отображаем метки только если масштаб 4 и больше
            if self.delta_x > 3:
                self.main_canvas.tag_raise(self.objectDict.dict_object[_].label)
            else:
                self.main_canvas.tag_lower(self.objectDict.dict_object[_].label)
        # Поднимаем выделение
        for _ in self.objectDict.dict_del_object.keys():
            self.main_canvas.tag_raise(self.objectDict.dict_del_object[_])
        # print(self.main_canvas.find_all())

    def right_button_click(self, event):  # , element = None):
        """
        Обработка правого щелчка мышки
        !!!!!! Исправить убрать else
        :param event:
        :return:
        """
        self.right_menu = tk.Menu(self.main_canvas, tearoff=0)
        # if element is None:
        self.right_menu.add_command(label="Создать", command=self.create_object)
        # else:
        #     self.right_menu.add_command(label="Удалить", command=lambda el=element: self.del_object(el))
        #                                 # command=self.del_object)
        self.position_cursor_old_x = event.x
        self.position_cursor_old_y = event.y
        self.right_menu.post(event.x_root, event.y_root)

    def create_object(self):
        """
        Создание новых объектов
        :return:
        """
        # Преобразуем координаты окна в координаты канвы
        self.set_position_x = self.main_canvas.canvasx(self.position_cursor_old_x)
        self.set_position_y = self.main_canvas.canvasy(self.position_cursor_old_y)
        # Отображаем окно для ввода дополнительной информации
        descr = Descr(self.main_canvas, self.delta_x, coord=[self.set_position_x, self.set_position_y], objectDict=self.objectDict)
        _, x, y = self.root.geometry().split('+')
        descr.geometry(f"200x200+{self.position_cursor_old_x + int(x) + 10}+{self.position_cursor_old_y + int(y)}")
        descr.grab_set()
        descr.wait_window()
