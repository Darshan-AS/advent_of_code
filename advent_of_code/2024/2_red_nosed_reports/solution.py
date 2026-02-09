from collections import Counter
from itertools import (
    chain,
    compress,
    islice,
    repeat,
    starmap,
    tee,
    zip_longest,
)
from numbers import Integral, Real
from operator import sub
import os
from typing import Iterable
from more_itertools import all_equal, takewhile_inclusive, pairwise, triplewise
from toolz import compose
from toolz.curried import map

Level = Integral
Report = Iterable[Level]


def sign(x: Real):
    return (x > 0) - (x < 0)


def is_safe_step(x: Integral):
    return 1 <= abs(x) <= 3


def is_safe_report(report: Report) -> bool:
    xs = starmap(sub, pairwise(report))
    ys, zs = tee(xs, 2)
    a = all_equal(map(sign, ys))
    b = all(map(is_safe_step, zs))
    return a and b

def is_safe_report2(report: Report) -> bool:
    ks = list(report)
    xs = list(starmap(sub, pairwise(report)))
    s = Counter(map(sign, starmap(sub, pairwise(report)))).most_common()[0][0]

    kk = list(is_safe_step(x) and sign(x) == s for x in xs)
    k = kk.index(False) if False in kk else len(kk)
    a = chain(repeat(True, k), (False,), repeat(True))
    b = chain(repeat(True, k + 1), (False,), repeat(True))

    aa = list(compress(ks, a))
    bb = list(compress(ks, b))
    return is_safe_report(aa) or is_safe_report(bb)


def safe_reports_count(reports: Iterable[Report]) -> int:
    return sum(map(is_safe_report, reports))


def safe_reports_count2(reports: Iterable[Report]) -> int:
    return sum(map(is_safe_report2, reports))


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        lines = file.readlines()

        to_report = compose(tuple, map(int), str.split)
        reports = tuple(map(to_report, lines))

        count = safe_reports_count(reports)
        print(f"Part One: {count}")

        s = safe_reports_count2(reports)
        print(f"Part Two: {s}")

        # print(is_safe_report2([23, 7, 6, 4, 2, 1]))


if __name__ == "__main__":
    main()
