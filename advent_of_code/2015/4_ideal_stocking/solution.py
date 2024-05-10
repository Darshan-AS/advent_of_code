from hashlib import md5
from itertools import count
from operator import add
import os
from toolz.curried.operator import add
from toolz.functoolz import compose
from toolz.itertoolz import first

md5_hex = lambda x: md5(x).hexdigest()


def mine(secret_key: str, n_zeros: int) -> int:
    target = "0" * n_zeros
    hash_ = compose(md5_hex, str.encode, add(secret_key), str)
    return first(filter(lambda x: hash_(x)[:n_zeros] == target, count()))


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        secret_key = file.read().rstrip()

        num = mine(secret_key, 5)
        print(f"Part One: {num}")

        num = mine(secret_key, 6)
        print(f"Part Two: {num}")


if __name__ == "__main__":
    main()
