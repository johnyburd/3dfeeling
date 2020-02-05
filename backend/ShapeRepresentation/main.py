import shape
from random import randint
from random import random


def main():
    height_test()
    points = [[randint(1, 10), randint(1, 10)] for i in range(20)]

    test_shape = shape.Representation(points)
    test_shape.get_final_shape().write("test.scad")

def height_test():
    # random range float [0,1]
    vad_points = [(random(), random(), random()) for i in range(20)]
    for p in vad_points:
        for x in range(5):
            print(shape.height_function(p, x))


if __name__ == "__main__":
    main()
