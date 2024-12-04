from itertools import chain, product
from operator import eq
import os
from typing import Iterable, Sequence

from toolz import curry, compose
from toolz.curried import map, filter

eq = curry(eq)

type Pair[T] = tuple[T, T]
type Point = Pair[int]
type Bounds = tuple[Pair, Pair]
type Slice = Iterable[Point]
type Grid[T] = Sequence[Sequence[T]]


ORTHOGONAL_STEPS = ((1, 0), (0, 1), (-1, 0), (0, -1))
DIAGONAL_STEPS = ((1, 1), (1, -1), (-1, 1), (-1, -1))


@curry
def point_in_bounds(bs: Bounds, p: Point) -> bool:
    (x1, y1), (x2, y2) = bs
    (x, y) = p
    return x1 <= x < x2 and y1 <= y < y2


@curry
def slice_in_bounds(bs: Bounds, slice: Slice) -> bool:
    return all(map(point_in_bounds(bs), slice))


@curry
def get_word(grid: Grid[str], slice: Slice) -> str:
    return "".join(grid[i][j] for i, j in slice)


@curry
def count_matches(grid: Grid[str], pattern: str, slices: Iterable[Slice]) -> int:
    m, n = len(grid), len(grid[0])
    bounds = ((0, 0), (m, n))
    return compose(
        sum,
        map(eq(pattern)),
        map(get_word(grid)),
        filter(slice_in_bounds(bounds)),
    )(slices)


@curry
def explore(
    center: Point, n: int, offset: int = 0, include_orthogonals: bool = True
) -> Iterable[Slice]:
    i, j = center
    start, end = offset, offset + n

    steps = chain(
        ORTHOGONAL_STEPS if include_orthogonals else (),
        DIAGONAL_STEPS,
    )

    return [[(i + di * w, j + dj * w) for w in range(start, end)] for di, dj in steps]


@curry
def find_points[T](grid: Grid[T], val: T) -> Iterable[Point]:
    m, n = len(grid), len(grid[0])
    return filter(lambda p: grid[p[0]][p[1]] == val, product(range(m), range(n)))


def count_XMAS(grid: Grid[str]) -> int:
    start_points = find_points(grid, "X")
    count_at_point = compose(
        count_matches(grid, "XMAS"),
        explore(n=4, offset=0),
    )
    return sum(map(count_at_point, start_points))


def count_MAS(grid: Grid[str]) -> int:
    start_points = find_points(grid, "A")
    count_at_point = compose(
        eq(2),
        count_matches(grid, "MAS"),
        explore(n=3, offset=-1, include_orthogonals=False),
    )
    return sum(map(count_at_point, start_points))


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        grid = list(map(str.strip, file.readlines()))

        XMAS_count = count_XMAS(grid)
        print(f"Part One: {XMAS_count}")

        MAS_count = count_MAS(grid)
        print(f"Part Two: {MAS_count}")


if __name__ == "__main__":
    main()
