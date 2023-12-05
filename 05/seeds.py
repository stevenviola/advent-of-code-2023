import argparse
import os
import re


class SeedMap:
    def __init__(self):
        self.mapping = {}
        self.current_mapping = None
        self.previous_mapping = None

    def add_line(self, line):
        if self.current_mapping:
            map_match = re.match("(\d+)\s(\d+)\s(\d+)", line.strip())
            if not map_match:
                self.previous_mapping = self.current_mapping
                self.current_mapping = None
                return
            self.mapping[self.current_mapping]["maps"].append(
                [
                    int(map_match.group(1)),
                    int(map_match.group(2)),
                    int(map_match.group(3)),
                ]
            )
        else:
            title_match = re.match("(\w+)-to-(\w+) map:", line.strip())
            if title_match:
                self.current_mapping = title_match.group(1)
                self.mapping[self.current_mapping] = {
                    "parent": self.previous_mapping,
                    "child": title_match.group(2),
                    "maps": [],
                }
                self.mapping[title_match.group(2)] = {
                    "parent": self.current_mapping,
                    "maps": [],
                }

    def get_min_mappings(self):
        min_values = []
        for _, value in self.mapping.items():
            if "child" not in value:
                continue
            child = value["child"]
            for i in value["maps"]:
                yield (child, i[0])

    # Given an input value and src, get a value at final_dest by traversing up
    # to parents or down to children until final_dest is reached
    def traverse_linked_list(self, input, src, final_dest, field):
        next_dest = self.mapping[src][field]
        maps = {
            "parent": self.mapping[next_dest]["maps"],
            "child": self.mapping[src]["maps"],
        }
        for link, start, length in maps[field]:
            if field == "parent":
                this_start = link
                other_start = start
            elif field == "child":
                this_start = start
                other_start = link
            if input >= this_start and input < this_start + length:
                mapped_location = input - this_start + other_start
                break
        else:
            mapped_location = input
        if final_dest == next_dest:
            return mapped_location
        else:
            return self.traverse_linked_list(mapped_location, next_dest, final_dest, field)


class Seeds:
    def __init__(self, seeds):
        self.seeds = seeds
        self.seed_ranges = []
        self.check_seeds = {1: [], 2: []}
        for idx, seed in enumerate(seeds):
            if idx % 2:
                seed_range.append(seed)
                self.seed_ranges.append(seed_range)
            else:
                seed_range = [seed]
                self.add_valid_seed(seed, 2)
            self.add_valid_seed(seed, 1)

    def add_valid_seed(self, seed, part):
        if self.is_valid_seed(seed, part):
            self.check_seeds[part].append(seed)

    def is_valid_seed(self, seed, part):
        if part == 1:
            return True if seed in self.seeds else False
        elif part == 2:
            for seed_range in self.seed_ranges:
                if seed >= seed_range[0] and seed < seed_range[0] + seed_range[1]:
                    return True
        return False


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Process seed mapping")
    parser.add_argument(
        "--filename", help="Path to the input file", default="input.txt"
    )
    args = parser.parse_args()

    # Objects to itterate over later
    seeds = None
    seed_map = SeedMap()

    # Input parsing to Objects
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            if not seeds:
                seed_match = re.match("seeds: (.*)", line.strip())
                seeds = Seeds([int(i) for i in seed_match.group(1).split(" ")])
            else:
                seed_map.add_line(line)

    # Done parsing input. Check lowest map values to find potential seeds
    # which would map to low locations. Add seeds to short list to be checked
    # later
    for parent, i in seed_map.get_min_mappings():
        test_seed = seed_map.traverse_linked_list(
            i, src=parent, final_dest="seed", field="parent"
        )
        for part in range(1, 3):
            seeds.add_valid_seed(test_seed, part)

    # Check all the possible seeds to get lowest seed location for each part
    answers = {1: [], 2: []}
    for part in range(1, 3):
        for k in seeds.check_seeds[part]:
            loc = seed_map.traverse_linked_list(
                k, src="seed", final_dest="location", field="child"
            )
            answers[part].append(loc)
        print(f"Part {part}: Lowest location is: {min(answers[part])}")


if __name__ == "__main__":
    main()
