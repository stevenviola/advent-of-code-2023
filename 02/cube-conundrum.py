import re
import os
import argparse


def process_colors(colors, limits):
    product = 1
    is_valid = True
    for color, value in colors.items():
        product *= value
        if color in limits and value > limits[color]:
            is_valid = False
    return (is_valid, product)


def process_rolls(line):
    colors = {}
    pattern = re.compile("(\d+) (\w+)")
    for round in line.split(";"):
        for dice in round.split(","):
            match = re.match(pattern, dice.strip())
            if match is None:
                print(f"Couldn't process {dice}")
                continue
            count = int(match.group(1))
            color = match.group(2)
            if color not in colors or colors[color] < count:
                colors[color] = count
    return colors


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(
        description="Process dice rolls for an elf"
    )
    parser.add_argument("filename", help="Path to the input file")
    args = parser.parse_args()
    limits = {"red": 12, "green": 13, "blue": 14}
    valid_games = []
    powers = []
    pattern = re.compile("Game (\d+):(.*)$")
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            line = line.strip()
            match = re.match(pattern, line)
            game_num = int(match.group(1))
            colors = process_rolls(match.group(2))
            is_valid, product = process_colors(colors, limits)
            powers.append(product)
            if is_valid:
                valid_games.append(game_num)
    print(f"PART 1: Sum of all valid games: {sum(valid_games)}")
    print(f"PART 2: Sum of powers: {sum(powers)}")


if __name__ == "__main__":
    main()
