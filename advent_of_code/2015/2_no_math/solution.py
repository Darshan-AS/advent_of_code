from itertools import starmap
import os
from toolz.functoolz import compose, curry
from toolz.curried import map
from typing import Iterable


Box = tuple[int, int, int]


def paper(box: Box) -> int:
    l, w, h = box
    areas = (l * w, w * h, h * l)
    return 2 * sum(areas) + min(areas)


def total_paper(boxes: Iterable[Box]) -> int:
    return sum(map(paper, boxes))


def ribbon(box: Box) -> int:
    l, w, h = box
    return 2 * (l + w + h - max(l, w, h)) + l * w * h


def total_ribbon(boxes: Iterable[Box]) -> int:
    return sum(map(ribbon, boxes))


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        lines = file.readlines()
        to_box = compose(tuple, map(int), curry(str.split)(sep="x"))
        boxes = tuple(map(to_box, lines))

        p = total_paper(boxes)
        print(f"Part One: {p}")

        r = total_ribbon(boxes)
        print(f"Part Two: {r}")


if __name__ == "__main__":
    main()
