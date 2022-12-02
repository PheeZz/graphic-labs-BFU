from pprint import pprint
from tkinter import *
from tkinter import colorchooser
from turtle import Vec2D

from PIL import Image, ImageDraw


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

        Button(root, text="Переместить", command=self.start_drag).grid(
            row=1, column=0, padx=6)

        Button(root, text="Остановить перемещение", command=self.stop_drag).grid(
            row=1, column=1, padx=6)

        Button(root, text="Начать поворот", command=self.bind_rotation).grid(
            row=1, column=3, padx=6)

        Button(root, text="Остановить поворот", command=self.stop_rotation).grid(
            row=1, column=4, padx=6)

    def setup_menu(self):
        self.menu = Menu(tearoff=0)
        self.menu.add_command(label="Квадрат", command=self.square)
        self.menu.add_command(label="Круг", command=self.circle)
        self.menu.add_command(label="Угол 90", command=self.angle_90)
        self.menu.add_command(label="Светофор", command=self.traffic_light)
        self.menu.add_command(label="Ромб", command=self.rhombus)

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

    def get_shape_center(self, points) -> tuple:
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

    def start_drag(self):
        self.canvas.bind("<B1-Motion>", self.drag)

    def drag(self, event):
        self.canvas.move("current", event.x - self.x, event.y - self.y)
        self.x, self.y = event.x, event.y

    def stop_drag(self):
        self.setup_bind()

    # TODO: add function to rotate polygon from test.py

    def get_angle(self, event):
        """Get angle between two vectors to rotate polygon."""
        def get_center():
            """get center coordinates of polygon

            Args:
                points (tuple): get it from canvas.coords("current")

            Returns:
                tuple: x,y coordinates of center
            """
            points = self.canvas.coords("current")
            x = sum(points[::2]) / 4
            y = sum(points[1::2]) / 4
            return x, y

        self.center_current_polygon = get_center()
        dx = self.canvas.canvasx(event.x) - self.center_current_polygon[0]
        dy = self.canvas.canvasy(event.y) - self.center_current_polygon[1]
        try:
            return complex(dx, dy) / abs(complex(dx, dy))
        except ZeroDivisionError:
            return 0.0  # cannot determine angle

    def bind_rotation(self):
        self.canvas.bind("<Button-1>", self.press_rotation)
        self.canvas.bind("<B1-Motion>", self.motion_to_rotate)

    def press_rotation(self, event):
        self.start_position = self.get_angle(event)

    def motion_to_rotate(self, event):
        angle = self.get_angle(event)/self.start_position
        offset = complex(*self.center_current_polygon)

        def get_all_shape_coordinates():
            """Get all coordinates of current shape on canvas."""
            points = self.canvas.coords("current")
            if len(points) == 4:
                # if shape is square
                # TODO recalculate coordinates to get all 4 points with x,y
                # as list of tuples
                points = [(points[0], points[1]),
                          (points[2], points[1]),
                          (points[2], points[3]),
                          (points[0], points[3])]
            else:
                # recalculate coordinates to get all 4 points with x,y
                # as list of tuples
                # every 2 points is one point with x,y is tuple
                points = [(points[i], points[i+1])
                          for i in range(0, len(points), 2)]
            print(
                f'points: {points}, type: {type(points)}, len: {len(points)}')
            return points

        new_coordinates = []
        coordinates = get_all_shape_coordinates()
        for x, y in coordinates:
            vertex = angle * (complex(x, y) - offset) + offset
            new_coordinates.extend((vertex.real, vertex.imag))
        pprint(new_coordinates)
        try:
            self.canvas.coords("current", *new_coordinates)
        except TclError as e:
            print(f'Error: {e}')

    def stop_rotation(self):
        self.setup_bind()


root = Tk()
root.title("Paint")
root.geometry("800x600")
root.resizable(0, 0)

root.columnconfigure(6, weight=1)
root.rowconfigure(2, weight=1)


image1 = Image.new("RGB", (800, 600), "white")
draw_image = ImageDraw.Draw(image1)
