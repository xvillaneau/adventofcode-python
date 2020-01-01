def iter_rows(image: str, width: int):
    i = 0
    while i < len(image):
        yield image[i : i + width]
        i += width


def iter_layers(image: str, width: int, height: int):
    layer = []
    for row in iter_rows(image, width):
        layer.append(row)
        if len(layer) == height:
            yield layer.copy()
            layer = []


def check_image(image: str, width: int = 25, height: int = 6):
    def counter(char):
        def func(lay):
            return sum(row.count(char) for row in lay)

        return func

    layer = min(iter_layers(image, width, height), key=counter("0"))
    return counter("1")(layer) * counter("2")(layer)


def decode_image(image: str, width: int = 25, height: int = 6):
    layers = list(iter_layers(image, width, height))
    image = layers[-1]
    for layer in layers[-2::-1]:
        for r, row in enumerate(layer):
            image[r] = "".join(
                bottom if top == "2" else top for top, bottom in zip(row, image[r])
            )
    return ("\n" + "\n".join(image)).replace("0", " ").replace("1", "#")


def main(data: str):
    yield check_image(data)
    yield decode_image(data)
