import openpyscad as ops
from functools import reduce
import numpy as np

MAX_TIME = 20
MAX_VALUES = 0.75 * 20


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
