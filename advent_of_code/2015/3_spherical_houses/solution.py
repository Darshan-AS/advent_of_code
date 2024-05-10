from itertools import accumulate
from numbers import Complex
from operator import add
import os
from more_itertools import distribute
from toolz.functoolz import compose
from toolz.curried import map, accumulate
from typing import Iterable, Literal, Mapping

Instruction = Literal["^", ">", "v", "<"]
Step = Complex
House = Complex

Move: Mapping[Instruction, Step] = {"^": 1j, ">": 1, "v": -1j, "<": -1}


def happy_houses(xs: Iterable[Instruction]) -> set[House]:
    return compose(set, accumulate(add, initial=0), map(Move.get))(xs)


def santa_delivery(xs: Iterable[Instruction]) -> int:
    return len(happy_houses(xs))


def santa_and_robot_delivery(xs: Iterable[Instruction]) -> int:
    santa_steps, robot_steps = distribute(2, xs)
    return len(happy_houses(santa_steps) | happy_houses(robot_steps))


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        instructions = file.read().rstrip()

        s_houses = santa_delivery(instructions)
        print(f"Part One: {s_houses}")

        sr_houses = santa_and_robot_delivery(instructions)
        print(f"Part Two: {sr_houses}")


if __name__ == "__main__":
    main()
