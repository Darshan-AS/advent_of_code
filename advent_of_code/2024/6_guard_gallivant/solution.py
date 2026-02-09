from itertools import product
import os
from typing import Sequence

from toolz import curry, flip

type Pair[T] = tuple[T, T]
type Point = Pair[int]
type Bounds = tuple[Pair, Pair]
type Grid[T] = Sequence[Sequence[T]]

def turn_right(dir):
    if dir == (-1, 0):
        return (0, 1)
    if dir == (0, 1):
        return (1, 0)
    if dir == (1, 0):
        return (0, -1)
    if dir == (0, -1):
        return (-1, 0)

@curry
def point_in_bounds(bs: Bounds, p: Point) -> bool:
    (x1, y1), (x2, y2) = bs
    (x, y) = p
    return x1 <= x < x2 and y1 <= y < y2

def foo1(grid, start, pose):
    m, n = len(grid), len(grid[0])
    bounds = ((0, 0), (m, n))
    curr = start
    dir = pose
    xs = {start}
    while point_in_bounds(bounds, curr):
        i, j = curr
        di, dj = dir
        if point_in_bounds(bounds, (i + di, j + dj)) and grid[i + di][j + dj] == "#":
            dir = turn_right(dir)
            continue
        curr = (i + di, j + dj)
        xs.add(curr)
    return len(xs) - 1

def foo2(grid, start, pose):
    return 0

def find_start(grid):
    m, n = len(grid), len(grid[0])
    for i, j in product(range(m), range(n)):
        if grid[i][j] == '^':
            return i, j, (-1, 0)
        elif grid[i][j] == '>':
            return i, j, (0, 1)
        elif grid[i][j] == '<':
            return i, j, (0, -1)
        elif grid[i][j] == 'v':
            return i, j, (1, 0)

def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        lines = file.read().splitlines()
        lab_map = list(map(list, lines))
        i, j, pose = find_start(lab_map)
        lab_map[i][j] = '.'

        n = foo1(lab_map, (i, j), pose)
        print(f"Part One: {n}")

        n = foo2(lab_map, (i, j), pose)
        print(f"Part Two: {n}")


if __name__ == "__main__":
    main()
