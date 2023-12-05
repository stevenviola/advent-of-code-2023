import argparse
import os
import re


class Scratchcard:
    def __init__(self, card):
        match = re.match("Card\s+(\d+):(.+)\|(.+)", card)
        if match is None:
            raise Exception(f"Can't process {card}")
        self.card_num = int(match.group(1))
        self.winners = [int(i) for i in match.group(2).strip().split()]
        self.scratchs = [int(j) for j in match.group(3).strip().split()]

    def get_matches(self):
        matches = []
        for i in self.winners:
            if i in self.scratchs:
                matches.append(i)
        return matches

    def get_card_worth(self):
        total_matches = len(self.get_matches())
        if total_matches < 1:
            return 0
        return 2 ** (total_matches - 1)


class Part2Rules:
    def __init__(self, all_scratchcards):
        self.all_scratchcards = all_scratchcards
        self.total_cards = []
        self.all_cards_mapping = {}
        for i in reversed(range(1, len(all_scratchcards) + 1)):
            card_count = self.recursive_check_cards(i)
            self.all_cards_mapping[i] = card_count
            self.total_cards.append(card_count)

    def recursive_check_cards(self, card_num=1, card_count=1):
        if card_num in self.all_cards_mapping:
            return self.all_cards_mapping[card_num]
        s = self.all_scratchcards[card_num - 1]
        new_cards = len(s.get_matches())
        for i in range(new_cards):
            new_card_num = card_num + i + 1
            if new_card_num > len(self.all_scratchcards):
                return 0
            card_count += self.recursive_check_cards(new_card_num)
        return card_count


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Process engine schematic")
    parser.add_argument(
        "--filename", help="Path to the input file", default="input.txt"
    )
    args = parser.parse_args()
    all_scratchcards = []
    total_worth = []
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            s = Scratchcard(line)
            all_scratchcards.append(s)
            total_worth.append(s.get_card_worth())
    print(f"Part 1: Sum of all the cards is: {sum(total_worth)}")
    p2 = Part2Rules(all_scratchcards)
    print(f"Part 2: Total number of cards is: {sum(p2.total_cards)}")


if __name__ == "__main__":
    main()
