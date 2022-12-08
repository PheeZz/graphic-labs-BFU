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
        self.menu.add_command(label="Квадрат", command=self.square)
        self.menu.add_command(label="Круг", command=self.circle)
        self.menu.add_command(label="Угол 90", command=self.arc_90_degrees)
        self.menu.add_command(label="Светофор", command=self.traffic_light)
        self.menu.add_command(label="Ромб", command=self.rhombus)
        self.menu.add_command(label="Кривая Безье",
                              command=self.curve)
        self.menu.add_command(
            label="Текстура", command=self.draw_circle_with_texture)

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

    def arc_90_degrees(self):
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

    def get_shape_center(self, points) -> tuple():
        """Get center of shape."""
        x = sum(p[0] for p in points) / len(points)
        y = sum(p[1] for p in points) / len(points)
        return x, y

    def rotate2D(self, angle, x0, y0, x1, y1):
        """Rotate (x0, y0) -> (x1, y1) vector by *angle*."""

        x, y = Vec2D(x1-x0, y1-y0).rotate(angle)
        return x + x0, y + y0

    def draw_2d_polygon(self, points, alpha, origin, *, color='gray'):
        points = [self.rotate2D(alpha, *[*origin, *p]) for p in points]
        self.canvas.create_polygon(points, outline=color, fill=color)

    def rhombus(self):
        """draw square and rotate it"""
        points = [(self.x, self.y),
                  (self.x + self.brush_size, self.y),
                  (self.x + self.brush_size, self.y + self.brush_size),
                  (self.x, self.y + self.brush_size)]
        origin = self.get_shape_center(points)
        self.draw_2d_polygon(points, 45, origin, color=self.brush_color)

    def curve(self, points=[], continue_flag=True, debug_mode=True):
        """draw lines with smooth edges"""
        if not continue_flag:
            return
        # remove hold lmb drawning
        self.canvas.unbind("<B1-Motion>")

        def stop_drawning(event):
            # loop until right mouse button clicked

            nonlocal continue_flag, points
            continue_flag = False
            del points
            self.canvas.unbind("<Button-1>")
            self.setup_bind()

        try:
            self.canvas.bind("<Button-3>", stop_drawning)
        except Exception as e:
            print(e)

        def add_point(event):
            # wait while 3 points be added to list by pressing left mouse button
            points.append((event.x, event.y))
            if len(points) == 3:
                self.canvas.unbind('<Button-1>')

        try:
            while len(points) < 3:
                self.canvas.bind('<Button-1>', add_point)
                self.canvas.update()
        except UnboundLocalError:
            # reference before assignment, fix for extra use of function
            return
        print(points)
        if debug_mode:
            # draw points as circles 'red' for first and last, 'green' for second point
            self.canvas.create_oval(points[0][0] - 5, points[0][1] - 5,
                                    points[0][0] + 5, points[0][1] + 5, fill='red')
            self.canvas.create_oval(points[1][0] - 5, points[1][1] - 5,
                                    points[1][0] + 5, points[1][1] + 5, fill='green')
            self.canvas.create_oval(points[2][0] - 5, points[2][1] - 5,
                                    points[2][0] + 5, points[2][1] + 5, fill='red')

        curves = []
        for dot in map(lambda x: x/100.0, range(0, 105, 5)):

            # calculate square curve
            x = (1.0-dot)**2*points[0][0] + 2*(1.0-dot) * \
                dot*points[1][0] + dot**2*points[2][0]

            y = (1.0-dot)**2*points[0][1] + 2*(1.0-dot) * \
                dot*points[1][1] + dot**2*points[2][1]

            curves.append([x, y])

        self.canvas.create_line(curves, fill=self.brush_color)

        if continue_flag:
            self.curve([points[-1]])

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

    def load_texture(self):
        """load texture for brush"""
        self.texture = Image.open(filedialog.askopenfilename())

    def draw_circle_with_texture(self):
        """crop texture as circle and draw it by using pillow"""
        texture = self.texture
        texture = texture.crop((0, 0, texture.width, texture.height))
        texture = texture.resize((self.brush_size, self.brush_size))
        texture = ImageTk.PhotoImage(texture)
        self.canvas.create_image(self.x, self.y, image=texture, anchor='nw')

    def start_drag(self):
        self.canvas.bind("<B1-Motion>", self.drag)

    def drag(self, event):
        self.canvas.move("current", event.x - self.x, event.y - self.y)
        self.x, self.y = event.x, event.y

    def stop_drag(self):
        self.setup_bind()


root = Tk()
root.title("Paint")
root.geometry("1280x720")
root.resizable(0, 0)

root.columnconfigure(6, weight=1)
root.rowconfigure(2, weight=1)

