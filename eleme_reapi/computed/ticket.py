import random


def _random_hex(n):
    return hex(random.randint(0, 16**n))[2:].zfill(n)


def ticket():
    ticket_arr = [_random_hex(i) for i in (8, 4, 4, 4, 12)]
    return '-'.join(ticket_arr).upper()


if __name__ == "__main__":
    print(ticket())