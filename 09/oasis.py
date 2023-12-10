import os
import argparse


class EnvReport:
    def __init__(self, line):
        self.history = [[int(i) for i in line.split()]]
        while set(self.history[-1]) != set([0]):
            last = None
            new_line = []
            for i in self.history[-1]:
                if last is not None:
                    new_line.append(i - last)
                last = i
            self.history.append(new_line)

    def pad_values(self):
        self.history[-1] + [0,0]
        line_count = len(self.history) - 1
        for idx in range(line_count):
            current_line = line_count - idx
            for pos in range(-1, 1):
                if pos < 0:
                    new_value = (
                        self.history[current_line - 1][pos]
                        + self.history[current_line][pos]
                    )
                    self.history[current_line - 1].append(new_value)
                else:
                    new_value = (
                        self.history[current_line - 1][pos]
                        - self.history[current_line][pos]
                    )
                    self.history[current_line - 1].insert(0, new_value)


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Process map")
    parser.add_argument(
        "--filename", help="Path to the input file", default="input.txt"
    )
    args = parser.parse_args()

    # Input parsing to Objects
    new_values = {1: [], 2: []}
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            ev = EnvReport(line.strip())
            ev.pad_values()
            new_values[1].append(ev.history[0][-1])
            new_values[2].append(ev.history[0][0])
    for i in range(1, 3):
        print(f"Part {i}: Sum of new values is {sum(new_values[i])}")


if __name__ == "__main__":
    main()
