import os
import argparse


class Map:
    def __init__(self):
        self.map = []
        self.start_pos = None
        self.loop_positions = []

    def add_line(self, line):
        self.map.append(list(line))
        if self.start_pos is None and "S" in line:
            self.start_pos = [len(self.map) - 1, self.map[-1].index("S")]

    def expand_map(self):
        new_map = [["*"] * ((len(self.map[0]) * 2) + 1)]
        for i in self.map:
            new_map.append(list("*" + "*".join(i) + "*"))
            new_map.append(new_map[0].copy())
        self.map = new_map
        prev = self.loop_positions[-1]
        for i in self.loop_positions:
            self.fill_loop(prev, i)
            prev = i

    def fill_loop(self, prev, curr):
        current_pos = [(i * 2) + 1 for i in curr]
        prev_pos = [(i * 2) + 1 for i in prev]
        x = 0 if prev_pos[0] != current_pos[0] else 1
        inc = -1 if current_pos[x] > prev_pos[x] else 1
        for i in range(current_pos[x], prev_pos[x], inc):
            if x == 0:
                self.map[i][prev_pos[1]] = "#"
            else:
                self.map[prev_pos[0]][i] = "#"

    def outter_fill(self, pos):
        stack = []
        visited = set()
        stack.append(pos)
        while len(stack) != 0:
            pos = stack.pop()
            pos_joined = "_".join([str(i) for i in pos])
            if pos_joined not in visited:
                visited.add(pos_joined)
            if self.map[pos[0]][pos[1]] in ["#", "$"]:
                continue
            self.map[pos[0]][pos[1]] = "$"
            for y in range(max(pos[0] - 1, 0), min(pos[0] + 2, len(self.map))):
                for x in range(max(pos[1] - 1, 0), min(pos[1] + 2, len(self.map[0]))):
                    if "_".join([str(y), str(x)]) in visited:
                        continue
                    stack.append([y, x])

    def count_original_values(self, updated_vals=["$", "#", "*"]):
        count = 0
        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[0])):
                if self.map[y][x] not in updated_vals:
                    count += 1
        return count

    def traverse_map(self):
        count = 0
        current_pos = self.start_pos
        previous_pos = self.start_pos
        next_symbol = None
        while next_symbol != "S":
            next_pos, next_symbol = self.get_next_tile(current_pos, previous_pos)
            self.loop_positions.append(next_pos)
            count += 1
            previous_pos = current_pos
            current_pos = next_pos
        return count

    def get_next_tile(self, pos, previous_pos):
        moves = self.get_possible_directions(pos)
        for i in moves:
            next_symbol = self.map[i[0]][i[1]]
            if i == previous_pos:
                continue

            if self.is_valid_move(pos, i):
                return (i, next_symbol)

    def get_possible_directions(self, pos):
        ret = []
        possible_symbols = ["S", "-", "|", "F", "7", "J", "L"]
        # North
        if pos[0] > 0 and self.map[pos[0] - 1][pos[1]] in possible_symbols:
            ret.append([pos[0] - 1, pos[1]])
        # South
        if (
            pos[0] < len(self.map[0]) - 1
            and self.map[pos[0] + 1][pos[1]] in possible_symbols
        ):
            ret.append([pos[0] + 1, pos[1]])
        # East
        if pos[1] < len(self.map) and self.map[pos[0]][pos[1] + 1] in possible_symbols:
            ret.append([pos[0], pos[1] + 1])
        # West
        if pos[1] > 0 and self.map[pos[0]][pos[1] - 1] in possible_symbols:
            ret.append([pos[0], pos[1] - 1])
        return ret

    def is_valid_move(self, current_pos, possible_move):
        current_symbol = self.map[current_pos[0]][current_pos[1]]
        next_symbol = self.map[possible_move[0]][possible_move[1]]
        if current_symbol in ["7", "F", "L", "J"] and current_symbol == next_symbol:
            # Right angle connectors can't connect to themselves
            return False
        if possible_move[0] < current_pos[0]:
            # Moving North
            if next_symbol in ["L", "J", "-"]:
                # Can't move north into L or J right angles
                return False
            if current_symbol in ["7", "F", "-"]:
                # Can't move north from 7 or F right angles
                return False
        elif possible_move[0] > current_pos[0]:
            # Moving South
            if next_symbol in ["7", "F", "-"]:
                # Can't move south into 7 or F right angles
                return False
            if current_symbol in  ["L", "J", "-"]:
                # Can't move south from J or L right angles
                return False
        elif possible_move[1] < current_pos[1]:
            # Moving West
            if next_symbol in ["J", "7", "|"]:
                # Can't move west into J or 7 right angles
                return False
            if current_symbol in ["L", "F", "|"]:
                # Can't move west from L or F right angles
                return False
        elif possible_move[1] > current_pos[1]:
            # Moving East
            if next_symbol in ["L", "F", "|"]:
                # Can't move east into L or F right angles
                return False
            if current_symbol in ["J", "7", "|"]:
                # Can't move east from J or 7 right angles
                return False
        return True


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Process map")
    parser.add_argument(
        "--filename", help="Path to the input file", default="input.txt"
    )
    args = parser.parse_args()
    m = Map()
    # Input parsing to Objects
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            m.add_line(line.strip())
    count = int(m.traverse_map() / 2)
    print(f"Part 1: Farthest distance is {count}")
    m.expand_map()
    m.outter_fill([0, 0])
    print(f"Part 2: Inside the ring, there are {m.count_original_values()} values")


if __name__ == "__main__":
    main()
