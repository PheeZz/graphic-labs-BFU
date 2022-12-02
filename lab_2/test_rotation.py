from pprint import pprint
from tkinter import Canvas, mainloop


def getangle(event):
    dx = canvas.canvasx(event.x) - center[0]
    dy = canvas.canvasy(event.y) - center[1]
    try:
        return complex(dx, dy) / abs(complex(dx, dy))
    except ZeroDivisionError:
        return 0.0  # cannot determine angle


def press(event):
    # calculate angle at start point
    global start
    start = getangle(event)


def motion(event):
    # calculate current angle relative to initial angle
    global start
    angle = getangle(event) / start
    offset = complex(*center)
    new_coordinates = []
    for x, y in coordinates:
        vertex = angle * (complex(x, y) - offset) + offset
        new_coordinates.extend((vertex.real, vertex.imag))
    canvas.coords("current", *new_coordinates)


if __name__ == '__main__':
    canvas = Canvas(width=200, height=200)
    canvas.pack()

    # square
    coordinates = [(50, 50),
                   (150, 50),
                   (150, 150),
                   (50, 150)]

    polygon_item = canvas.create_polygon(coordinates)

    center = 100.0, 100.0
    canvas.bind("<Button-1>", press)
    canvas.bind("<B1-Motion>", motion)

    mainloop()
