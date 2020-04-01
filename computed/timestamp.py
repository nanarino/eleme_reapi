import time


def timestamp():
    return str(int(time.time()))


if __name__ == "__main__":
    print(timestamp())