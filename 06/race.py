import argparse
import os
import re


class Race:
    def __init__(self, time=None, distance=None):
        self.time = time
        self.distance = distance

    def set_distance(self, distance):
        self.distance = distance

    def get_first_win(self, start, stop, step):
        for i in range(start, stop, step):
            if (self.time - i) * i > self.distance:
                return i

    def get_winners(self):
        return (
            self.get_first_win(0, self.time, 1),
            self.get_first_win(self.time, 0, -1),
        )


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Process race sheet")
    parser.add_argument(
        "--filename", help="Path to the input file", default="input.txt"
    )
    args = parser.parse_args()
    parts = {1: {"races": {}, "concat": False}, 2: {"races": {}, "concat": True}}
    # Input parsing to Objects
    input_pattern = re.compile("([\d]+)")
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            for _, part in parts.items():
                matches = re.findall(input_pattern, line)
                if part["concat"]:
                    matches = ["".join(matches)]
                for idx, match in enumerate(matches):
                    num = int(match)
                    if idx not in part["races"]:
                        part["races"][idx] = Race(time=num)
                    else:
                        part["races"][idx].set_distance(num)

    # Done parsing input.
    product_winners = None
    for part_num, part in parts.items():
        for _, race in part["races"].items():
            winners = race.get_winners()
            num_winners = winners[1] - winners[0] + 1
            if product_winners is None:
                product_winners = num_winners
            else:
                product_winners *= num_winners
        print(
            f"Part {part_num}: {num_winners} ways to win, "
            f"product of all possible winning races is: {product_winners}"
        )


if __name__ == "__main__":
    main()
