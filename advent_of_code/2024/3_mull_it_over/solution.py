from itertools import starmap
from numbers import Integral
from operator import mul
import os
import re
from typing import Callable, Iterable, Literal

from toolz import compose, curry
from toolz.curried import map, take

Fn = Callable
findall = curry(re.findall)
starmap = curry(starmap)

CorruptInstructions = str

Conditional = Literal["do()"] | Literal["don't()"]
Expression = str # strings of type "mul(x,y)"
Instruction = Conditional | Expression

BinaryOperands = tuple[Integral, Integral]

P = r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)"

@curry
def execute_conditionals(xs: Iterable[Instruction], skip: bool = False) -> Iterable[Expression]:
    use = True
    for x in xs:
        if x == "do()": use = True or skip
        elif x == "don't()": use = False or skip
        elif use: yield x

def recover(xs: CorruptInstructions, skip_conditionals: bool = False) -> Iterable[Expression]:
    return compose(execute_conditionals(skip=skip_conditionals), findall(P))(xs)

to_operands \
    : Fn[[Iterable[Expression]], BinaryOperands] \
    = compose(tuple, take(2), map(int), findall(r"\d+"))

compute \
    : Fn[[Iterable[Expression]], Integral] \
    = compose(sum, starmap(mul), map(to_operands))

recover_and_compute \
    : Fn[[CorruptInstructions, bool], Integral] \
    = compose(compute, recover)


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        instructions = file.read()

        result = recover_and_compute(instructions, True)
        print(f"Part One: {result}")

        result = recover_and_compute(instructions, False)
        print(f"Part Two: {result}")


if __name__ == "__main__":
    main()
