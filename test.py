# TEST LOGGER
from time import sleep
from ComputerVision.ComputerVision import ComputerVision


def test():
    for i in range(10):
        c = ComputerVision()
        x, y = c.get_icon_coords("pasar")
        print(x, y)
        sleep(1)


if __name__ == "__main__":
    test()
    # logTest()
