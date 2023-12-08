import os
import argparse


class Hand:
    def __init__(self, line, part):
        face_cards = {
            1: {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14},
            2: {"T": 10, "J": 1, "Q": 12, "K": 13, "A": 14},
        }
        # Map a hand to a type given the length of distinct cards, and the max
        # number of a single card in the hand. Order is decending
        possible_types = {
            0: {5: 6},  # All Jokers
            1: {5: 6},  # 5 of a kind
            2: {4: 5, 3: 4},  # 4 of a kind or Full House
            3: {3: 3, 2: 2},  # 3 of a kind or 2 pair
            4: {2: 1},  # One pair
            5: {1: 0},  # High card
        }
        card_info = line.strip().split()
        self.bid = int(card_info[1])
        self.cards = []
        self.hand_type = None
        card_count = {}
        for i in card_info[0].strip():
            if i.isdigit():
                self.cards.append(int(i))
            else:
                self.cards.append(face_cards[part][i])
            if self.cards[-1] not in card_count:
                card_count[self.cards[-1]] = 0
            card_count[self.cards[-1]] += 1
        # Set the type of the hand
        jokers = 0
        if part == 2 and 1 in card_count:
            # In part 2, J is wildcard
            jokers = card_count[1]
            del card_count[1]
        if len(card_count) > 0:
            max_one_card = max(card_count.values()) + jokers
        else:
            max_one_card = jokers
        self.hand_type = possible_types[len(card_count)][max_one_card]


class AllHands:
    def __init__(self):
        self.all_hands = {}

    def add_hand(self, hand):
        if hand.hand_type not in self.all_hands:
            self.all_hands[hand.hand_type] = [hand]
        else:
            for i in range(len(self.all_hands[hand.hand_type])):
                for j in range(5):
                    if hand.cards[j] == self.all_hands[hand.hand_type][i].cards[j]:
                        continue
                    if hand.cards[j] < self.all_hands[hand.hand_type][i].cards[j]:
                        self.all_hands[hand.hand_type].insert(i, hand)
                        return
                    else:
                        break
            self.all_hands[hand.hand_type].append(hand)

    def get_winnings(self):
        rank = 1
        total_winnings = 0
        for i in sorted(self.all_hands.keys()):
            for j in self.all_hands[i]:
                total_winnings += rank * j.bid
                rank += 1
        return total_winnings


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Process camel cards")
    parser.add_argument(
        "--filename", help="Path to the input file", default="input.txt"
    )
    args = parser.parse_args()
    all_hands = {1: AllHands(), 2: AllHands()}
    # Input parsing to Objects
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            for part in range(1, 3):
                all_hands[part].add_hand(Hand(line, part))
    for part in range(1, 3):
        print(f"Part {part}: Total Winnings is {all_hands[part].get_winnings()}")


if __name__ == "__main__":
    main()
