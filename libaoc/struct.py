from bisect import bisect_left
from collections.abc import Iterable, Iterator, MutableSet
from typing import TypeVar

T = TypeVar("T")


class SortedSet(MutableSet[T]):

    def __init__(self, elements: Iterable[T] = ()):
        self._data: list[T] = []
        self.update(elements)

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __contains__(self, item: T) -> bool:
        i = bisect_left(self._data, item)
        return i < len(self._data) and self._data[i] == item

    def add(self, item: T) -> None:
        i = bisect_left(self._data, item)
        if i >= len(self._data) or self._data[i] != item:
            self._data.insert(i, item)

    def discard(self, item: T) -> None:
        i = bisect_left(self._data, item)
        if i < len(self._data) and self._data[i] == item:
            self._data.pop(i)

    def update(self, *others: Iterable[T]) -> None:
        for items in others:
            for item in items:
                self.add(item)
