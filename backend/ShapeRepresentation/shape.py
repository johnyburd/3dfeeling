import openpyscad as ops
from functools import reduce
import numpy as np

MAX_TIME = 20
MAX_VALUES = 0.75 * 20


def circ_function_r(vad, theta):
    """
    A function for finding the radius value of the circle shape function

    :parameter: vad, tuple of valence, arousal, and dominance
                     all in range [0,1]
    :parameter: theta, float value in range [0, 2pi)

    :return: r, where r is a float representing the radius of the "circle" at theta
    """
    v, a, d = vad

    v *= 19
    v += 3
    v = round(v)

    a += 1

    r = 5 + a * np.sin((26 - v) * theta) + (1 - d) * np.sin(30 * theta)
    return r


def polygon_points(num_corners, num_points):
    """
    Generates points of a regular polygon.

    Code in this function taken from:
    https://math.stackexchange.com/questions/41940/is-there-an-equation-to-describe-regular-polygons

    :parameter: num_corners The number of corners the polygon should have
    :parameter: num_points How many points to generate.

    :return: [x, y] List of float values that are the points of the polygon.
    """
    theta_values = np.arange(0, 2 * np.pi, 2 * np.pi / num_points)
    pi_n = np.pi / num_corners
    r_values = []
    for i in range(num_points):
        r_values.append(10 * (np.cos(pi_n) / (np.cos((theta_values[i] % (2 * pi_n)) - pi_n))))
    return r_values


def polygon_cylinder(vads, num_points):
    vads = np.array(vads)
    polygons = []
    length = int(np.log(vads.shape[0]) * 10)
    if vads.shape[0] > 9:
        for i in range(vads.shape[0] // 10):
            arg = np.argmax(np.square(vads[i * 10:i * 10 + 10, 2] - 0.5))
            val = vads[i * 10 + arg, 2]
            sides = round(15 - (val * 12))
            polygons.append(polygon_points(sides, num_points))
    else:
        arg = np.argmax(np.square(vads[:, 2] - 0.5))
        val = vads[arg, 2]
        sides = round(15 - (val * 12))
        polygons.append(polygon_points(sides, num_points))

    theta_values = np.arange(0, 2 * np.pi, 2 * np.pi / num_points)
    points_3d = []
    faces = []
    for i, x in enumerate(np.arange(0, length, length / vads.shape[0])[0:vads.shape[0]]):
        poly = min(len(polygons) - 1, i // 10)
        for j, th in enumerate(theta_values):
            r = 0.3 * circ_function_r(vads[i], th)
            r += polygons[poly][j]
            r *= (4 - abs(((i % 10) - 5))) * 0.075 + 1
            points_3d.append([x, r * np.cos(th), r * np.sin(th)])
    for i in range(len(vads) - 1):
        faces.append([i * num_points,
                      (i + 1) * num_points - 1,
                      (i + 2) * num_points - 1,
                      (i + 1) * num_points])
        for j in range(num_points - 1):
            faces.append(circ_neighbors(i * num_points + j, num_points))

    size = len(points_3d)
    faces.append(list(range(num_points - 1, -1, -1))[::-1])
    faces.append(list(range(size - 1, size - num_points - 1, -1)))

    return ops.Polyhedron(points=points_3d, faces=faces)


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


def circ_function(vad, theta):
    """
    A function for finding the x and y values of the polar function used to describe the cylindrical shape.

    :parameter: vad, tuple of valence, arousal, and dominance
                     all in range [0,1]
    :parameter: theta, float value in range [0, 2pi)

    :return: (x, y), where x and y are floats representing the x, y coordinates of function at theta
    """
    v, a, d = vad

    v *= 19
    v += 3
    v = round(v)

    a += 1

    r = 5 + a * np.sin((26 - v) * theta) + (1 - d) * np.sin(30 * theta)
    return (r * np.cos(theta), r * np.sin(theta))


def circ_neighbors(index, width):
    return [index, index + width, index + width + 1, index + 1]


def generate_cylinder(vads, num_points):
    """
    Will generate a cylindrical object that represents the sentiment in the vad array.
    Uses the circ_function to generate each of the layers of the cylinder.

    :parameter: vads, array of vad tuples
    :paramter: num_pts, number of points to be sampled for each layer of the cylinder

    :return: returns an openpyscad polyhedron that represents the cylindrical object
    """
    theta_values = np.arange(0, 2 * np.pi, 2 * np.pi / num_points)
    points_3d = []
    faces = []
    for i, x in enumerate(np.arange(0, 25, 25 / len(vads))):
        for j in theta_values:
            y, z = circ_function(vads[i], j)
            points_3d.append([x, y, z])
    for i in range(len(vads) - 1):
        faces.append([i * num_points,
                      (i + 1) * num_points - 1,
                      (i + 2) * num_points - 1,
                      (i + 1) * num_points])
        for j in range(num_points - 1):
            faces.append(circ_neighbors(i * num_points + j, num_points))

    size = len(points_3d)
    faces.append(list(range(num_points - 1, -1, -1))[::-1])
    faces.append(list(range(size - 1, size - num_points - 1, -1)))

    return ops.Polyhedron(points=points_3d, faces=faces)


def neighbors(index, width):
    return [index + 1, index + width + 1, index + width, index]


def generate_terrain(vads, num_points):
    width = 10
    y_points = np.arange(0, width, width / num_points)
    points_3d = []
    for i, e in enumerate(np.arange(0, 15, 15 / len(vads))):
        for j in y_points:
            points_3d.append([e, j, height_function(vads[i], j)])

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


def get_height(vads, x, y, t_length):
    partitions_size = t_length / len(vads)
    vad_index = int(x // partitions_size)
    vad = vads[vad_index]

    return height_function(vad, y)


# dimensions of base 10x15
# these dimensions should be a hard coded, consistent standard
X_LENGTH = 15
Y_LENGTH = 10


def generate_terrain2_electric_boogaloo(vads):
    # x = dimension along time axis/ multiple sentences
    # y = dimension along a single sentence/ wave
    # z = height

    width = Y_LENGTH
    length = X_LENGTH
    # sample 10 times per unit of width
    num_y_samples = width * 10
    num_x_samples = length * 5

    # points to sample z-height from along x and y axes
    y_points = np.arange(0, width, width / num_y_samples)
    x_points = np.arange(0, length, length / num_x_samples)
    points_3d = []
    for x in x_points:
        for y in y_points:
            points_3d.append([x, y, get_height(vads, x, y, length)])
    faces = []
    for i in range(num_x_samples - 1):
        for j in range(num_y_samples - 1):
            faces.append(neighbors(i * num_x_samples + j, num_x_samples))

    size = len(points_3d)

    points_3d.append([0, 0, 0])
    points_3d.append([0, width, 0])
    points_3d.append([length, 0, 0])
    points_3d.append([length, width, 0])

    faces.append([size, size + 1, size + 3, size + 2])
    faces.append([size + 1] + list(range(num_y_samples))[::-1] + [size])
    faces.append([size + 2] + list(range(size - num_y_samples, size)) + [size + 3])
    faces.append([size] + list(range(0, size, num_y_samples)) + [size + 2])
    faces.append([size + 1, size + 3] + list(range(num_y_samples - 1, size, num_y_samples))[::-1])

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
    # generate_terrain(np.random.random((5, 3)), 250).write("test.scad")
    # generate_cylinder(np.random.random((5, 3)), 250).write("test.scad")
    polygon_cylinder(np.random.random((100, 3)), 250).write("polycyl.scad")
