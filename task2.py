import numpy as np
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f'({self.x}, {self.y})'


class Line:
    def __init__(self, A: Point, B: Point):
        self.A = A
        self.B = B


def read_file(path):
    points = []
    with open(path) as f:
        rows = f.readlines()

    for row in rows:
        row = row.split()
        points.append(Point(float(row[0]), float(row[1])))

    return points[0], points[1:]


def check_side(point: Point, line: Line):
    d = np.array([[point.x, point.y, 1],
                  [line.A.x, line.A.y, 1],
                  [line.B.x, line.B.y, 1]])

    if np.linalg.det(d) < 0:
        return False

    return True


def check_point(point, fig):
    star = True
    for i in range(-1, len(fig) - 1):
        if not check_side(point, Line(fig[i], fig[i + 1])):
            star = False
            break

    return star

def plot(point, fig):
    fig = np.array([[p.x, p.y] for p in fig])

    plt.fill(fig[:, 0], fig[:, 1], fill=False)
    plt.scatter(x=point.x, y=point.y)
    plt.show()


if __name__ == '__main__':
    point, fig = read_file('test.txt')

    if check_point(point, fig):
        print('Ok')
    else:
        print('Error')

    plot(point, fig)
