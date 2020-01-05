def top_floor(data):
    floor = 0
    for character in data:
        if character == "(":
            floor += 1
        else:
            floor -= 1
    return floor


def first_basement(data):
    floor = 0
    position = 1
    for character in data:
        if character == "(":
            floor += 1
        else:
            floor -= 1
        if floor == -1:
            break
        position += 1
    return position


def main(data):
    yield top_floor(data)
    yield first_basement(data)
