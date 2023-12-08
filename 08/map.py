import os
import argparse
import re
import math


class Map:
    def __init__(self):
        self.directions = None
        self.steps = {}
        self.current_direction = 0
        self.matches = {}
        self.intervals = []

    def add_line(self, line):
        match = re.match("([\w\d]{3}) = \(([\w\d]{3}), ([\w\d]{3})\)+", line)
        if match is not None:
            self.steps[match.group(1)] = [match.group(2), match.group(3)]
        if self.directions is None:
            self.directions = line

    def get_next_step(self, start, step_count):
        direction_index = step_count % len(self.directions)
        step_index = 0
        if self.directions[direction_index] == "R":
            step_index = 1
        next_step = self.steps[start][step_index]
        return next_step

    def add_thread_match(self, step_count, thread):
        if thread not in self.matches:
            self.matches[thread] = []
        self.matches[thread].append(step_count)
        if len(self.matches[thread]) == 2:
            self.intervals.append(self.matches[thread][1] - self.matches[thread][0])

    def reset_intervals(self):
        self.matches = {}
        self.intervals = []

    def get_step_count(self, start_pattern, end_pattern):
        self.reset_intervals()
        step_count = 0
        next_steps = list(
            filter(lambda x: re.match(start_pattern, x), self.steps.keys())
        )
        while True:
            end_steps = []
            for i in range(len(next_steps)):
                next_steps[i] = self.get_next_step(next_steps[i], step_count)
            step_count += 1
            # Check how many next_steps match the end_pattern
            for idx, j in enumerate(next_steps):
                if re.match(end_pattern, j):
                    end_steps.append(idx)
            # If count of end_steps is number of next_steps, this is the end
            if len(end_steps) >= len(next_steps):
                return step_count
            # If only some threads match end_pattern, determine the interval
            # from the previous match for this thread
            for thread in end_steps:
                self.add_thread_match(step_count, thread)
            # Once we have enough intervals, get the least common multiple
            if len(self.intervals) >= len(next_steps):
                return math.lcm(*self.intervals)


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Process map")
    parser.add_argument(
        "--filename", help="Path to the input file", default="input.txt"
    )
    args = parser.parse_args()
    parts = {
        1: {"start_pattern": "AAA", "end_pattern": "ZZZ"},
        2: {"start_pattern": "..A", "end_pattern": "..Z"},
    }
    map = Map()
    # Input parsing to Objects
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            map.add_line(line.strip())

    for part in range(1, 3):
        start_pattern = parts[part]["start_pattern"]
        end_pattern = parts[part]["end_pattern"]
        print(
            f"Part {part}: Steps needed are: "
            f"{map.get_step_count(start_pattern, end_pattern)}"
        )


if __name__ == "__main__":
    main()
