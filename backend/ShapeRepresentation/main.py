import shape
from random import randint


def main():
    points = [[randint(1, 10), randint(1, 10)] for i in range(20)]
    test_shape = shape.Representation(points)
    test_shape.get_final_shape().write("test.scad")


if __name__ == "__main__":
    main()
