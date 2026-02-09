import os


def foo(rotations):
    return 5


def main():
    filepath = os.path.join(os.path.dirname(__file__), "input.txt")
    with open(filepath, "r") as file:
        lines = file.readlines()

        rotations = map(lambda x: (x[0], int(x[1:])), lines)

        password = foo(rotations)
        print(f"Part One: {password}")


if __name__ == "__main__":
    main()
