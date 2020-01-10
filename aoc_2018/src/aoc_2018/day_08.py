def metadata_sum(data: str):
    numbers = [int(n) for n in reversed(data.split())]

    def reduce_sum():
        n_children, n_meta = numbers.pop(), numbers.pop()
        return (
            sum(reduce_sum() for _ in range(n_children))
            + sum(numbers.pop() for _ in range(n_meta))
        )

    return reduce_sum()


def metadata_value(data: str):
    numbers = [int(n) for n in reversed(data.split())]

    def reduce_value() -> int:
        n_children, n_meta = numbers.pop(), numbers.pop()
        children = [reduce_value() for _ in range(n_children)]
        metadata = [numbers.pop() for _ in range(n_meta)]
        if not n_children:
            return sum(metadata)
        return sum(
            children[i-1] if 0 < i <= n_children else 0
            for i in metadata
        )

    return reduce_value()


def main(data: str):
    yield metadata_sum(data)
    yield metadata_value(data)
