import os
import argparse


class Schematic:
    def __init__(self):
        self.schematic = []
        self.number_locations = []
        self.gear_locations = []

    def add_line(self, line):
        y = len(self.schematic)
        row = []
        x_min = 0
        current_number = []
        for x, i in enumerate(line):
            row.append(i)
            if i == "*":
                self.gear_locations.append(("*", x, y))
            if i.isdigit():
                if len(current_number) < 1:
                    x_min = x
                current_number.append(i)
            else:
                # Try storing the current number
                self.store_numbers(x_min, y, current_number)
                current_number = []
        # Store any number left over at the end of the line
        self.store_numbers(x_min, y, current_number)
        self.schematic.append(row)

    def store_numbers(self, x, y, num_list):
        try:
            num = int("".join(num_list))
            self.number_locations.append((num, x, y))
        except:
            pass

    def check_for_symbol(self, x1, y1, x2, y2):
        for line in self.schematic[y1 : y2 + 1]:
            for character in line[x1:x2]:
                if not character.isdigit() and character != ".":
                    return True
        return False

    def get_number_at_loc(self, x, y, max_characters=3):
        number = []
        x_min = max(0, x - max_characters)
        x_max = x + max_characters + 1
        touches = False
        for char_x, character in enumerate(self.schematic[y][x_min:x_max]):
            if character.isdigit():
                if char_x+x_min == x:
                    touches = True
                number.append(character)
            elif len(number) > 0 and touches:
                break
            else:
                number = []
        if touches:
            return int("".join(number))

    def check_for_gear(self, x1, y1, x2, y2):
        numbers = []
        for y_offset, line in enumerate(self.schematic[y1:y2+1]):
            parsing_digit = False
            for x_offset, character in enumerate(line[x1:x2]):
                x = x_offset + x1
                y = y_offset + y1
                if character.isdigit():
                    if not parsing_digit:
                        number = self.get_number_at_loc(x, y)
                        if number is not None:
                            parsing_digit = True
                            numbers.append(number)
                else:
                    parsing_digit = False
        if len(numbers) > 1:
            return numbers[0] * numbers[1]

    def parse_schematic(self, location):
        for num_loc in location:
            number = num_loc[0]
            x = num_loc[1]
            y = num_loc[2]
            x1 = max(0, x - 1)
            x2 = x + 1 + len(str(number))
            y1 = max(0, y - 1)
            y2 = y + 1
            yield (number, x1, y1, x2, y2)

    def part1(self):
        adjcent_nums = []
        for number, x1, y1, x2, y2 in self.parse_schematic(self.number_locations):
            if self.check_for_symbol(x1, y1, x2, y2):
                adjcent_nums.append(number)
        return sum(adjcent_nums)

    def part2(self):
        gear_products = []
        for _, x1, y1, x2, y2 in self.parse_schematic(self.gear_locations):
            gear = self.check_for_gear(x1, y1, x2, y2)
            if gear is not None:
                gear_products.append(gear)
        return sum(gear_products)


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Process engine schematic")
    parser.add_argument(
        "--filename", help="Path to the input file", default="input.txt"
    )
    args = parser.parse_args()
    s = Schematic()
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            s.add_line(line.strip())
    print(f"Part 1: Sum of numbers adjcent to symbols is {s.part1()}")
    print(f"Part 2: Sum of product of gears is {s.part2()}")


if __name__ == "__main__":
    main()
