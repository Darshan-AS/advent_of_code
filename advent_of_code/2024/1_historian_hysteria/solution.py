from collections import Counter
from numbers import Integral
from operator import mul, sub
import os
from toolz import compose, get
from typing import Iterable
from toolz.curried import map
from more_itertools import unzip

LocationID = Integral
List = Iterable[LocationID]


def distance(left_list: List, right_list: List) -> int:
    return sum(map(compose(abs, sub), sorted(left_list), sorted(right_list)))


def similarity(left_list: List, right_list: List) -> int:
    return sum(map(mul, left_list, get(left_list, Counter(right_list))))


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        lines = file.readlines()

        list1, list2 = compose(
            map(list),
            map(map(int)),
            unzip,
            map(str.split),
        )(lines)

        d = distance(list1, list2)
        print(f"Part One: {d}")

        s = similarity(list1, list2)
        print(f"Part One: {s}")


if __name__ == "__main__":
    main()
