from tkinter import *
from tkinter import colorchooser

from PIL import Image, ImageDraw


class easy_shapes:
    def __init__(self, root: Tk):
        self.x, self.y = 0, 0
        self.brush_color = "black"

        Label(root, text="Параметры:").grid(row=0, column=0, padx=6)

        Scale(root, from_=1, to=100, orient=HORIZONTAL,
              variable=IntVar(value=10), length=200,
              command=self.select).grid(row=0, column=3, padx=6)

        self.color_label = Label(root, bg=self.brush_color, width=10)
        self.color_label.grid(row=0, column=2, padx=6)

        self.setup_menu()
        self.setup_brush()
        self.setup_canvas()
        self.setup_bind()
        self.setup_button()

    def setup_menu(self):
        self.menu = Menu(tearoff=0)
        self.menu.add_command(label="Квадрат", command=self.square)
        self.menu.add_command(label="Круг", command=self.circle)
        self.menu.add_command(label="Угол 90", command=self.angle_90)
        self.menu.add_command(label="Светофор", command=self.traffic_light)

    def setup_brush(self):
        self.brush_color = "black"
        self.brush_size = 10

    def setup_canvas(self):
        self.canvas = Canvas(root, bg="white")
        self.canvas.grid(row=2, column=0, columnspan=7,
                         padx=5, pady=5, sticky=N + S + E + W)

    def setup_bind(self):
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<Button-3>", self.popup)

    def setup_button(self):
        Button(root, text="Цвет", command=self.choose_color).grid(
            row=0, column=1, padx=6)

        Button(root, text="Очистить", command=self.clear_canvas).grid(
            row=0, column=5, padx=6)

        Button(root, text="Заливка", command=self.pour).grid(
            row=0, column=7, padx=6)

    def draw(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)

        self.canvas.create_oval(x1, y1, x2, y2,
                                fill=self.brush_color, outline=self.brush_color)
        draw_image.ellipse(
            [x1, y1, x2, y2],
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
        draw_image.rectangle((0, 0, 800, 600), fill='white', outline='white')

    def popup(self, event):
        self.x, self.y = event.x, event.y
        self.menu.post(event.x_root, event.y_root)

    def square(self):
        self.canvas.create_rectangle(
            self.x, self.y,
            self.x + self.brush_size,
            self.y + self.brush_size,
            fill=self.brush_color, outline=self.brush_color)

    def circle(self):
        self.canvas.create_oval(
            self.x, self.y,
            self.x + self.brush_size,
            self.y + self.brush_size,
            fill=self.brush_color, outline=self.brush_color)

    def angle_90(self):
        self.canvas.create_arc(self.x, self.y,
                               self.x + self.brush_size,
                               self.y + self.brush_size,
                               start=90, extent=90, fill=self.brush_color, outline='black')

    def traffic_light(self):
        # draw 3 circles with different colors
        self.canvas.create_oval(self.x, self.y,
                                self.x + self.brush_size,
                                self.y + self.brush_size,
                                fill='red', outline='black')

        self.canvas.create_oval(self.x, self.y + self.brush_size,
                                self.x + self.brush_size,
                                self.y + 2*self.brush_size, fill='yellow', outline='black')

        self.canvas.create_oval(self.x, self.y + 2*self.brush_size,
                                self.x + self.brush_size,
                                self.y + 3*self.brush_size,
                                fill='green', outline='black')


root = Tk()
root.title("Paint")
root.geometry("800x600")
root.resizable(0, 0)

root.columnconfigure(6, weight=1)
root.rowconfigure(2, weight=1)


image1 = Image.new("RGB", (800, 600), "white")
draw_image = ImageDraw.Draw(image1)
