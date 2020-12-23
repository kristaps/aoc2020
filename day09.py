#!/usr/bin/env python3

from argparse import ArgumentParser
from typing import List
from itertools import combinations


def check_number(n: int, latest: List[int]):
    # Reduce combination count by eliminating numbers that are
    # too large to sum up to n with any of the other numbers
    max_valid = n - min(latest)
    latest = [i for i in latest if i <= max_valid]

    return any(
        (n1 + n2 == n for n1, n2 in combinations(latest, 2))
    )


def find_mismatch(numbers, preamble_length=25):
    latest, numbers = numbers[:preamble_length], numbers[preamble_length:]

    for n in numbers:
        if not check_number(n, latest):
            return n

        latest.append(n)
        latest.pop(0)


def find_weakness(numbers, mismatch):
    for i in range(0, len(numbers)):
        range_sum = 0
        for j in range(i, len(numbers)):
            range_sum += numbers[j]

            if range_sum == mismatch:
                matching_range = numbers[i:j]
                return min(matching_range) + max(matching_range)

            if range_sum > mismatch:
                break


def solve():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--preamble-length', default=25, type=int)
    arg_parser.add_argument('input_file')

    args = arg_parser.parse_args()

    with open(args.input_file, 'r') as input_file:
        numbers = [int(l) for l in input_file.read().splitlines()]

    mismatch = find_mismatch(numbers, args.preamble_length)
    weakness = find_weakness(numbers, mismatch)

    print("MISMATCH:", mismatch)
    print("WEAKNESS:", weakness)


if __name__ == '__main__':
    solve()
