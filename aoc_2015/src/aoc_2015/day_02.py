from typing import NamedTuple, Iterable

class Box(NamedTuple):
    l: int
    w: int
    h: int

    @classmethod
    def from_repr(cls, dimensions_str: str):
        l, w, h = map(int, dimensions_str.strip().split('x'))
        return Box(l, w, h)

    @property
    def side_surfaces(self):
        l, w, h = self.l, self.w, self.h
        return l*w, w*h, h*l

    @property
    def side_perimeters(self):
        l, w, h = self.l, self.w, self.h
        return 2*(l+w), 2*(w+h), 2*(h+l)

    @property
    def volume(self):
        return self.l * self.w * self.h

    @property
    def paper_required(self):
        return 2 * sum(self.side_surfaces) + min(self.side_surfaces)

    @property
    def ribbon_required(self):
        return min(self.side_perimeters) + self.volume

    def __repr__(self):
        return f"{self.l}x{self.w}x{self.h}"


def total_paper(boxes: Iterable[str]) -> int:
    return sum(
        Box.from_repr(_l).paper_required
        for line in boxes if (_l := line.strip())
    )

def total_ribbon(boxes: Iterable[str]) -> int:
    return sum(
        Box.from_repr(_l).ribbon_required
        for line in boxes if (_l := line.strip())
    )

def test_ribbon():
    assert Box(2, 3, 4).ribbon_required == 34
    assert Box(1, 1, 10).ribbon_required == 14


def main(data: str):
    boxes = data.splitlines()
    yield total_paper(boxes)
    yield total_ribbon(boxes)
