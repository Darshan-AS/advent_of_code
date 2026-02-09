from itertools import islice, pairwise, starmap
from operator import not_
import os
from typing import Callable, Counter, Iterable
from more_itertools import ilen, triplewise
from toolz.functoolz import compose, curry, juxt
from toolz.curried.operator import contains, le, eq, sub, gt
from toolz.curried import filter, map
from toolz.itertoolz import partition, reduceby, groupby, first, second

Rule = Callable[[Iterable], bool]

banned = (("a", "b"), ("c", "d"), ("p", "q"), ("x", "y"))

has_3_vowels: Rule = compose(le(3), ilen, filter(contains("aeiou")))
has_double_letters: Rule = compose(any, curry(starmap)(eq), pairwise)
has_no_banned_strs: Rule = compose(not_, any, map(contains(banned)), pairwise)

has_pair_ge_2: Rule = lambda s: Counter(partition(2, s)).most_common(1)[0][1] >= 2
foo: Rule = lambda s: has_pair_ge_2(s) or has_pair_ge_2(islice(s, 1, None))
has_xyx = compose(any, map(lambda s: s[0] == s[2]), triplewise)

def bar(s):
    xs = enumerate(pairwise(s))
    ys = groupby(second, xs)
    # print(ys)
    zs = [list(map(first, v)) for v in ys.values()]
    # print(zs)
    ps = [list(starmap(sub, pairwise(z))) for z in zs]
    # print(ps)
    qs = [list(filter(gt(-1), p)) for p in ps]
    # print(qs)
    rs = [ilen(q) for q in qs]
    # print(rs)
    return any(rs)


def is_nice(text: str) -> bool:
    return all(juxt(has_3_vowels, has_double_letters, has_no_banned_strs)(text))

def is_nice2(text: str) -> bool:
    return all(juxt(bar, has_xyx)(text))

count_nice = compose(sum, map(is_nice2))


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        texts = file.readlines()

        # t = "ieodomkazucvgmuy"
        # print(bar(t), has_xyx(t), is_nice2(t))

        # n = count_nice(texts)
        # print(f"Part One: {n}")

        n = count_nice(texts)
        print(f"Part Two: {n}")


if __name__ == "__main__":
    main()
