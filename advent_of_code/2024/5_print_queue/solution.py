from collections import Counter, defaultdict
from functools import reduce
from itertools import chain, compress, pairwise, starmap
from operator import eq, le, getitem
import os
from typing import Hashable, Iterable, Mapping, Sequence

from more_itertools import split_at
from toolz import compose, curry, flip, complement, mapcat, concat
from toolz.curried import map, remove

eq = curry(eq)
getitem = curry(getitem)
starmap = curry(starmap)

type Edge[T] = tuple[T, T]
type Graph[T: Hashable] = Mapping[T, Iterable[T]]
type TopologicalGroup[T] = Iterable[Iterable[T]]

type Page = int
type OrderingRule = tuple[Page, Page]
type PageUpdate = Sequence[Page]


def to_graph[T](edges: Iterable[Edge[T]]) -> Graph[T]:
    return reduce(
        lambda g, e: g[e[0]].add(e[1]) or g,
        edges,
        defaultdict(set),
    )


@curry
def clip_subgraph[T](graph: Graph[T], nodes: Iterable[T]) -> Graph[T]:
    xs = set(nodes)
    return {x: graph[x] & xs for x in xs}


def topologically_group[T](graph: Graph[T]) -> TopologicalGroup[T]:
    in_degrees = Counter(concat(graph.values()))
    filter_0_degrees = remove(getitem(in_degrees))

    nbrs = graph.keys()
    while nbrs:
        level = tuple(filter_0_degrees(nbrs))
        yield level
        nbrs = tuple(mapcat(getitem(graph), level))
        for v in nbrs:
            in_degrees[v] -= 1


def is_ordered(group: TopologicalGroup[Page], update: PageUpdate) -> bool:
    page_to_levels = {p: level for level, pages in enumerate(group) for p in pages}
    page_orders = map(getitem(page_to_levels), update)
    return all(starmap(le, pairwise(page_orders)))


@curry
def groupify_update(
    graph: Graph[Page], update: PageUpdate
) -> Iterable[TopologicalGroup[Page]]:
    return compose(tuple, topologically_group, clip_subgraph)(graph, update)


def ordered_updates_median_sum(
    rules: Iterable[OrderingRule], updates: Sequence[PageUpdate]
) -> int:
    graph = to_graph(rules)
    groups = map(groupify_update(graph), updates)
    selector = map(is_ordered, groups, updates)

    ordered_updates = compress(updates, selector)
    return sum(map(lambda x: x[len(x) // 2], ordered_updates))


def unordered_updates_median_sum(
    rules: Iterable[OrderingRule], updates: Sequence[PageUpdate]
) -> int:
    graph = to_graph(rules)
    groups = tuple(map(groupify_update(graph), updates))
    selector = map(complement(is_ordered), groups, updates)

    unordered_update_groups = compress(groups, selector)
    ordered_updates = map(compose(tuple, concat), unordered_update_groups)
    return sum(map(lambda x: x[len(x) // 2], ordered_updates))


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        lines = file.read().splitlines()
        raw_rules, raw_updates = split_at(lines, eq(""))

        split_to_ints = compose(tuple, map(int), str.split)
        rules = [split_to_ints(r, "|") for r in raw_rules]
        updates = [split_to_ints(u, ",") for u in raw_updates]

        k = ordered_updates_median_sum(rules, updates)
        print(f"Part One: {k}")

        k = unordered_updates_median_sum(rules, updates)
        print(f"Part Two: {k}")


if __name__ == "__main__":
    main()
