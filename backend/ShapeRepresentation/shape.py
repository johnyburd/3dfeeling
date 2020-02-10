import openpyscad as ops
from functools import reduce
import numpy as np

MAX_TIME = 20
MAX_VALUES = 0.75 * 20


def height_function(vad, x):
    """
    A function for sampling the height of a continuous function based on the values
    of valence, arousal and dominance at a specific point, x.

    Height, y, can range from ~[3, 8]

    :parameter: vad, a tuple of valence, arousal, and dominance
                x, a float related to 2D cartesian plane (x,y)

    :return: float y, where y = f(v,a,d,x) is related to a + a*sin(x/v) + (1/d)*sin(1/xd)
    """

    v, a, d = vad
    return a + a * np.sin(x / v) + a * np.cos(x / np.sqrt(a * d)) + 5


def neighbors(index, width):
    return [index + 1, index + width + 1, index + width, index]


def generate_terrain(vads, num_points):
    width = 10
    y_points = np.arange(0, width, width / num_points)
    points_3d = []
    for i in range(len(vads)):
        for j in y_points:
            points_3d.append([i, j, height_function(vads[i], j)])

    faces = []
    for i in range(len(vads) - 1):
        for j in range(num_points - 1):
            faces.append(neighbors(i * num_points + j, num_points))

    size = len(points_3d)

    points_3d.append([0, 0, 0])
    points_3d.append([0, width, 0])
    points_3d.append([len(vads) - 1, 0, 0])
    points_3d.append([len(vads) - 1, width, 0])

    faces.append([size + 2, size + 3, size + 1, size])
    faces.append([size + 1] + list(range(num_points))[::-1] + [size])
    faces.append([size + 2] + list(range(size - num_points, size)) + [size + 3])
    faces.append([size] + list(range(0, size, num_points)) + [size + 2])
    faces.append([size + 1, size + 3] + list(range(num_points - 1, size, num_points))[::-1])

    return ops.Polyhedron(points=points_3d, faces=faces)


def transform(x, size):
    return [size] + x


def union(r1, r2):
    return r1 + r2


def scale_points(data, max_x, max_y):
    points = np.array(data)
    largest_x = np.max(points[:, 0])
    largest_y = np.max(points[:, 1])

    scale_x = float(max_x) / largest_x
    scale_y = float(max_y) / largest_y

    transformed_points = []
    for p in data:
        transformed_points.append([p[0] * scale_x, p[1] * scale_y])
    return transformed_points


class TimeRange(object):

    def __init__(self, start, end, step):
        self.start = start
        self.end = end
        self.step = step
        self.cur = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur < self.end:
            temp = self.cur
            self.cur += self.step
            return temp
        else:
            raise StopIteration()


class Representation:

    def __init__(self, points):
        self.points = scale_points(points, MAX_VALUES, MAX_VALUES)
        self.time_steps_size = MAX_TIME / len(self.points)
        self.time_steps = TimeRange(0, MAX_TIME, self.time_steps_size)
        self.rects = self.transform_points()
        self.shape = self.build_shape()
        # self.total = self.shape.sum()
        self.total = self.sum()

    def transform_points(self):
        return [transform(p, self.time_steps_size) for p in self.points]

    def build_shape(self):
        shape = []
        for t, offset in enumerate(self.time_steps):
            shape.append(ops.Cube(self.rects[t]).translate([offset, 0, 0]))
        return shape

    def sum(self):
        return reduce(union, self.shape)

    def get_rects(self):
        return self.rects

    def get_final_shape(self):
        return self.total


if __name__ == "__main__":
    generate_terrain(np.random.random((30, 3)), 250).write("test.scad")
