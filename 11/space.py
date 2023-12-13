import os
import argparse


class GalacticMap:
    def __init__(self, f):
        self.map = []
        self.galaxy_locations = []
        self.empty_space = {0: [], 1: []}
        # Parse input file
        for line in f:
            self.map.append(list(line.strip()))
            if set(self.map[-1]) == set(["."]):
                self.empty_space[0].append(len(self.map) - 1)
        empty_cols = [i for i in range(len(self.map[0]))]
        for row_num, row in enumerate(self.map):
            for col_num, col_val in enumerate(row):
                if col_num in empty_cols and col_val != ".":
                    empty_cols.remove(col_num)
                if col_val == "#":
                    self.galaxy_locations.append((row_num, col_num))
        self.empty_space[1] = empty_cols

    def find_distances(self, start_pos, empty_space_multiplier=1):
        idx = self.galaxy_locations.index(start_pos)
        for goal in self.galaxy_locations[idx + 1 :]:
            steps = 0
            for i in range(2):
                min_pos = min(goal[i], start_pos[i])
                max_pos = max(goal[i], start_pos[i])
                steps += max_pos - min_pos
                for j in range(min_pos, max_pos + 1):
                    if j in self.empty_space[i]:
                        steps += empty_space_multiplier
            yield steps


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Process galactic map")
    parser.add_argument(
        "--filename", help="Path to the input file", default="input.txt"
    )
    args = parser.parse_args()
    parts = {1: 1, 2: 999999}
    # Input parsing to Objects
    with open(f"{path}/{args.filename}", "r") as f:
        gm = GalacticMap(f)
    for part_num, empty_space_multiplier in parts.items():
        count = 0
        for i in gm.galaxy_locations:
            count += sum([i for i in gm.find_distances(i, empty_space_multiplier)])
        print(f"Part {part_num}: Sum of all distances is: {count}")


if __name__ == "__main__":
    main()
