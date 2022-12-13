# Создание интерфейса пользователя
import tkinter as tk
from PIL import Image, ImageTk

class Window:
    def __init__(self):
        self.root = tk.Tk()
        main_w = 1200
        main_h = 600
        self.root.title("Ping Master - start")  # Заголовок окна
        self.root.geometry(f"{main_w}x{main_h}+100+100")  # Создаем окно
        self.root.resizable(False, False)  # Запрещаем изменять размер окна
        self.root.configure(background='#ffffff')
        # Создаем меню
        self.main_menu = tk.Menu(self.root)
        self.root.config(menu=self.main_menu)
        self.main_menu.add_command(label="OK")
        # Создаем ползунки
        self.main_vscroll = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.main_hscroll = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.main_canvas = tk.Canvas(self.root, height=main_h-40, width=main_w-200, xscrollcommand=self.main_hscroll.set,
                                     yscrollcommand=self.main_vscroll.set)
        self.main_vscroll.config(command=self.main_canvas.yview)
        self.main_hscroll.config(command=self.main_canvas.xview)
        self.main_vscroll.place(in_=self.main_canvas, relx=1.0, relheight=1.0, bordermode="outside")
        self.main_hscroll.place(in_=self.main_canvas, relx=0.0, rely=1.0, relwidth=1.0, bordermode="outside")
        self.main_canvas.configure(background='#ffffff')
        self.main_images = Image.open("images/main.jpg")  # Открываем картинку
        height = self.main_images.height
        width = self.main_images.width
        self.im_ratio = width/height
        # print(self.im_ratio, height, width)
        self.main_images_copy = self.main_images.resize((main_w - 200, int((main_w-200)/self.im_ratio)), Image.LANCZOS)  # Изменяем размер
        self.main_canvas.config(scrollregion=f"0 0 {self.main_images_copy.width} {self.main_images_copy.height}")
        # Создаем копию изображения для дальнейшей работы

        self.main_images_pi = ImageTk.PhotoImage(self.main_images_copy)
        self.main_canvas.create_image(0, 0, anchor='nw', image=self.main_images_pi)  # Размещаем
        self.main_canvas.place(x=0, y=0)

        # self.root.bind("<Configure>", self.resize)  # Отрисовка при изменении геометрии окна. Пока отключена.
        # self.root.bind("<Motion>", self.left_button)
        self.root.bind("<MouseWheel>", self.mousewheel)
        self.root.bind("<B3-Motion>", self.move_img)
        self.root.bind("<Button-3>", self.right_button_click)


    def right_button_click(self, event):
        self.old_x = event.x
        self.old_y = event.y

    def move_img(self, event):
        if event.x > self.old_x:
            self.main_canvas.xview_scroll(number=1, what="units")
            # x_l, x_h = self.main_hscroll.get()
            # self.main_hscroll.set(x_l+0.1,x_h+0.1)
            self.old_x = event.x
        if event.x < self.old_x:
            self.main_canvas.xview_scroll(number=-1, what="units")
            self.old_x = event.x
        if event.y > self.old_y:
            self.main_canvas.yview_scroll(number=1, what="units")
            self.old_y = event.y
        if event.y < self.old_y:
            self.main_canvas.yview_scroll(number=-1, what="units")
            self.old_y = event.y
        # print(self.main_hscroll.get())
        # self.main_canvas.yview_scroll(number=1, what="units")



    def mousewheel(self,event):
        """
        Действия при прокрутке ролика мышки
        :param event:
        :return:
        """
        if event.delta > 0:
            height = self.main_images_copy.height
            size = (int((height+100)*self.im_ratio), (height+100))
        else:
            height = self.main_images_copy.height
            size = (int((height-100)*self.im_ratio), (height-100))


        self.main_images_copy = self.main_images.resize(size, Image.ANTIALIAS)
        self.main_canvas.config(scrollregion=f"0 0 {self.main_images_copy.width} {self.main_images_copy.height}")
        self.main_images_pi = ImageTk.PhotoImage(self.main_images_copy)
        self.main_canvas.create_image(0, 0, anchor='nw', image=self.main_images_pi)



    def after_resize(self):
        self.width_window = self.root.winfo_width()
        self.height_window = self.root.winfo_height()
        print("press")

    def left_button(self,event):
        """
        Действия при нажатии левой кнопки мышки
        :param event:
        :return:
        """
        self.after_resize()


    def resize(self, event):
        """
        Действия при изменении размера окна приложения
        :param event:
        :return:
        """
        size = (event.width, event.height)
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
