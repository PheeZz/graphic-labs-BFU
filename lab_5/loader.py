from tkinter import colorchooser, filedialog, Label, Tk, Scale, HORIZONTAL, IntVar, Menu, Button, Canvas, N, S, E, W
from turtle import Vec2D

from PIL import Image, ImageDraw, ImageGrab, ImageTk


class easy_shapes:
    def __init__(self, root: Tk):
        self.x, self.y = 0, 0
        self.brush_color = "black"

        Label(root, text="Параметры:").grid(row=0, column=0, padx=6)
        Label(root, text="Размер кисти:").grid(row=0, column=3, padx=6)
        Scale(root, from_=1, to=100, orient=HORIZONTAL,
              variable=IntVar(value=10), length=200,
              command=self.select).grid(row=0, column=4, padx=6)

        self.color_label = Label(root, bg=self.brush_color, width=10)
        self.color_label.grid(row=0, column=2, padx=6)

        self.setup_menu()
        self.setup_brush()
        self.setup_canvas()
        self.setup_bind()
        self.setup_button()

    def setup_button(self):
        Button(root, text="Цвет", command=self.choose_color).grid(
            row=0, column=1, padx=6)

        Button(root, text="Очистить", command=self.clear_canvas).grid(
            row=0, column=6, padx=6)

        Button(root, text="Заливка", command=self.pour).grid(
            row=0, column=5, padx=6)

        Button(root, text="Сохранить", command=self.save_image).grid(
            row=1, column=3, padx=6)

        Button(root, text="Загрузить", command=self.open_image).grid(
            row=1, column=4, padx=6)

        Button(root, text="Переместить", command=self.start_drag).grid(
            row=1, column=0, padx=6)

        Button(root, text="Остановить перемещение", command=self.stop_drag).grid(
            row=1, column=1, padx=6)

    def setup_menu(self):
        self.menu = Menu(tearoff=0)
        self.menu.add_command(label="300x300 Сравнение методов",
                              command=self.by_neighbours_mid_size)
        # self.menu.add_command(label="300x300 Линейная интерполяция",
        #                       command=self.linear_interpolation_mid_size)
        # self.menu.add_command(label="300x300 Сплайновая интерполяция",
        #                       command=self.spline_interpolation_mid_size)

    def setup_brush(self):
        self.brush_color = "black"
        self.brush_size = 10

    def setup_canvas(self):
        self.canvas = Canvas(root, width=1280, height=720, bg="white")
        self.canvas.grid(row=2, column=0, columnspan=7,
                         padx=5, pady=5, sticky=N + S + E + W)

    def setup_bind(self):
        """Bind mouse events to canvas"""
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-3>", self.popup)

    def draw(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)

        self.canvas.create_oval(x1, y1, x2, y2,
                                fill=self.brush_color, outline=self.brush_color)

    def choose_color(self):
        rgb, hx = colorchooser.askcolor()
        self.brush_color = hx
        self.color_label['bg'] = hx

    def select(self, value):
        self.brush_size = int(value)

    def pour(self):
        self.canvas.delete("all")
        self.canvas['bg'] = self.brush_color

    def clear_canvas(self):
        self.canvas.delete("all")
        self.canvas['bg'] = 'white'

    def popup(self, event):
        self.x, self.y = event.x, event.y
        self.menu.post(event.x_root, event.y_root)

    def open_image(self):
        """open image and draw it on canvas"""
        image = Image.open(filedialog.askopenfilename())
        self.image = ImageTk.PhotoImage(image)
        self.canvas.create_image(self.x, self.y, image=self.image, anchor='nw')

    def save_image(self):
        """save image as png"""
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save('screenshot.png')

    def start_drag(self):
        self.canvas.bind("<B1-Motion>", self.drag)

    def drag(self, event):
        self.canvas.move("current", event.x - self.x, event.y - self.y)
        self.x, self.y = event.x, event.y

    def stop_drag(self):
        self.setup_bind()

    # open 3 images next to each other and draw them on canvas with different methods
    def by_neighbours_mid_size(self):
        self.file_path = filedialog.askopenfilename()
        image = Image.open(self.file_path)
        image1 = Image.open(self.file_path)
        image2 = Image.open(self.file_path)

        image = image.resize((400, 400), Image.NEAREST)
        image1 = image1.resize((400, 400), Image.ANTIALIAS)
        image2 = image2.resize((400, 400), Image.BICUBIC)

        self.image = ImageTk.PhotoImage(image)
        self.image1 = ImageTk.PhotoImage(image1)
        self.image2 = ImageTk.PhotoImage(image2)

        self.canvas.create_image(0, 0, image=self.image, anchor='nw')
        self.canvas.create_image(400, 0, image=self.image1, anchor='nw')
        self.canvas.create_image(800, 0, image=self.image2, anchor='nw')

    # def linear_interpolation_mid_size(self):
    #     image = Image.open(self.file_path)
    #     image1 = Image.open(self.file_path)
    #     image2 = Image.open(self.file_path)

    #     image = image.resize((300, 300), Image.ANTIALIAS)
    #     image2 = image2.resize((300, 300), Image.ANTIALIAS)

    #     self.image = ImageTk.PhotoImage(image)
    #     self.image1 = ImageTk.PhotoImage(image1)
    #     self.image2 = ImageTk.PhotoImage(image2)

    #     self.canvas.create_image(0, 0, image=self.image, anchor='nw')
    #     self.canvas.create_image(300, 0, image=self.image1, anchor='nw')
    #     self.canvas.create_image(600, 0, image=self.image2, anchor='nw')

    # def spline_interpolation_mid_size(self):
    #     image = Image.open(self.file_path)
    #     image1 = Image.open(self.file_path)
    #     image2 = Image.open(self.file_path)

    #     image = image.resize((300, 300))
    #     image1 = image1.resize((300, 300))

    #     image = image.resize((300, 300), Image.BICUBIC)
    #     image1 = image1.resize((300, 300), Image.BICUBIC)

    #     self.image = ImageTk.PhotoImage(image)
    #     self.image1 = ImageTk.PhotoImage(image1)
    #     self.image2 = ImageTk.PhotoImage(image2)

    #     self.canvas.create_image(0, 0, image=self.image, anchor='nw')
    #     self.canvas.create_image(300, 0, image=self.image1, anchor='nw')
    #     self.canvas.create_image(600, 0, image=self.image2, anchor='nw')


root = Tk()
root.title("Paint")
root.geometry("1280x720")
root.resizable(0, 0)

root.columnconfigure(6, weight=1)
root.rowconfigure(2, weight=1)
