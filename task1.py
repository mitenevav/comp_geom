import numpy as np


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

    return points


def get_new_pos(point: Point, line: Line):
    l = ((line.B.x - line.A.x) ** 2 + (line.B.y - line.A.y) ** 2) ** (1 / 2)
    num = (line.B.x - line.A.x) * (point.y - line.A.y) - (line.B.y - line.A.y) * (point.x - line.A.x)
    y = np.abs(num / l)

    A_p = ((point.x - line.A.x) ** 2 + (point.y - line.A.y) ** 2) ** (1 / 2)
    x = (A_p ** 2 - y ** 2) ** (1 / 2)

    scalar = (point.x - line.A.x) * (line.B.x - line.A.x) + (point.y - line.A.y) * (line.B.y - line.A.y)

    if scalar != 0:
        x *= scalar / np.abs(scalar)

    return Point(x, y)


def get_first_step(points):
    new_points = [get_new_pos(p, Line(points[0], points[1])) for p in points]

    ptr = np.array([[p.x, p.y] for p in new_points])

    left = np.argmin(ptr[:, 0])
    right = np.argmax(ptr[:, 0])
    height = np.argmax(ptr[:, 1])

    per = (ptr[right, 0] - ptr[left, 0] + ptr[height, 1]) * 2
    area = (ptr[right, 0] - ptr[left, 0]) * ptr[height, 1]

    return per, area, right, height, left


def get_info(points, base, prev_r, prev_h, prev_l):
    base_line = Line(points[base], points[(base + 1) % len(points)])

    left_x = get_new_pos(points[prev_l], base_line).x

    left_i = prev_l
    while True:
        left_i = (left_i + 1) % len(points)
        new_x = get_new_pos(points[left_i], base_line).x
        if left_x <= new_x:
            left_i = (left_i - 1) % len(points)
            break
        left_x = new_x

    right_x = get_new_pos(points[prev_r], base_line).x
    right_i = prev_r
    while True:
        right_i = (right_i + 1) % len(points)
        new_x = get_new_pos(points[right_i], base_line).x
        if right_x >= new_x:
            right_i = (right_i - 1) % len(points)
            break
        right_x = new_x

    height = get_new_pos(points[prev_h], base_line).y
    height_i = prev_h
    while True:
        height_i = (height_i + 1) % len(points)
        new_h = get_new_pos(points[height_i], base_line).y
        if height >= new_h:
            height_i = (height_i - 1) % len(points)
            break
        height = new_h

    per = (right_x - left_x + height) * 2
    area = (right_x - left_x) * height

    return per, area, right_i, height_i, left_i


def write_result(result, path):
    res = np.array(result)

    area_i = np.argmin(res[:, 1])
    area_res = res[area_i][2:].astype(int)

    per_i = np.argmin(res[:, 0])
    per_res = res[per_i][2:].astype(int)

    text = f'Area: {area_res[0]}, {area_res[1]}, {area_res[2]}, {area_res[3]}, {area_res[4]}\n' \
           f'Perimeter: {per_res[0]}, {per_res[1]}, {per_res[2]}, {per_res[3]}, {per_res[4]}'
    with open(path, 'w') as f:
        f.write(text)


def run(points):
    result = []
    base = 0
    per, area, right_i, height_i, left_i = get_first_step(points)
    result.append((per, area, 0, 1, right_i, height_i, left_i))

    for base in range(1, len(points)):
        per, area, right_i, height_i, left_i = get_info(points,
                                                        base,
                                                        result[-1][4],
                                                        result[-1][5],
                                                        result[-1][6])
        result.append((per,
                       area,
                       base,
                       (base + 1) % len(points),
                       right_i,
                       height_i,
                       left_i
                       ))

    return result


if __name__ == "__main__":
    points = read_file('test.txt')

    res = run(points)

    write_result(res, 'output.txt')
