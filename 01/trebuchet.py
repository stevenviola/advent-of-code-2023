import argparse
import os


def words_to_numbers(input_string):
    word_to_number = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }
    for word, number in word_to_number.items():
        if input_string[: len(word)] == word:
            return number


def extract_digits(line, convert_words=False):
    numbers = []
    for i in range(len(line)):
        if line[i].isnumeric():
            numbers.append(int(line[i]))
        elif convert_words:
            converted_number = words_to_numbers(line[i:])
            if converted_number is not None:
                numbers.append(converted_number)
    if len(numbers) < 1:
        return None
    number = int(f"{numbers[0]}{numbers[-1]}")
    print(f"{line} : {number}")
    return number


def main():
    path = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(
        description="Extract first and last digits from each line of a file."
    )
    parser.add_argument("filename", help="Path to the input file")
    parser.add_argument(
        "-p",
        "--parse-digits",
        help="Parse input text to convert words to digits",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()
    numbers = []
    with open(f"{path}/{args.filename}", "r") as f:
        for line in f:
            line = line.strip()
            digits = extract_digits(line, args.parse_digits)
            if digits is None:
                print(f"No numbers found in : {line}")
                continue
            numbers.append(digits)
    print(sum(numbers))


if __name__ == "__main__":
    main()
