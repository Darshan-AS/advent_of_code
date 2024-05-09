from itertools import accumulate, dropwhile
import os
from toolz.functoolz import compose, curry
from toolz.itertoolz import second, first
from typing import Iterable, Literal

Instruction = Literal["(", ")"]


def steps(xs: Iterable[Instruction]) -> Iterable[int]:
    return ((-1, 1)[x == "("] for x in xs)


def final_floor(xs: Iterable[Instruction]) -> int:
    return sum(steps(xs))


def basement_position(xs: Iterable[Instruction]) -> int:
    return compose(
        first,
        first,
        curry(dropwhile)(lambda x: second(x) > -1),
        curry(enumerate)(start=1),
        accumulate,
        steps,
    )(xs)


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        instructions = file.read()

        floor = final_floor(instructions)
        print(f"Part One: {floor}")

        position = basement_position(instructions)
        print(f"Part Two: {position}")


if __name__ == "__main__":
    main()
