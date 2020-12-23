#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Set, Dict


Color = str

TARGET_COLOR = 'shiny gold'


@dataclass
class Rule:
    parent: Color
    children: Dict[Color, int] = field(default_factory=lambda: defaultdict(int))


def parse_rule(rule_text: str) -> Rule:
    tokens = rule_text.split()

    rule = Rule(' '.join(tokens[:2]))

    # Discard container color spec
    tokens = tokens[4:]

    # Parse contents specification, each 4 tokens long. Will break when
    # no rules are left and on empty rules, which have 3 remaining tokens.
    while len(tokens) >= 4:
        rule.children[' '.join(tokens[1:3])] = int(tokens[0])
        tokens = tokens[4:]

    return rule


def invert_rules(rules: List[Rule]):
    """
    Transform input rules into a form better suited for the task of finding
    valid containers for any given color, inverting the parent-child
    relationships.
    """

    inverted: Dict[Color, Set[Color]] = defaultdict(set)

    for r in rules:
        for c in r.children:
            inverted[c].add(r.parent)

    return inverted


def find_container_colors(color: Color, rules: Dict[Color, Set[Color]]):
    return rules[color].union(
        *[find_container_colors(c, rules) for c in rules[color]]
    )


def count_contained_bags(color: Color, rule_map: Dict[Color, Rule]):
    return sum(
        [v + v * count_contained_bags(c, rule_map) for c, v in rule_map[color].children.items()]
    )


def solve():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('input_file')

    args = arg_parser.parse_args()

    with open(args.input_file, 'r') as input_file:
        rules = [parse_rule(l) for l in input_file.read().splitlines()]

    print("TOP LEVEL COLORS:", len(find_container_colors(TARGET_COLOR, invert_rules(rules))))
    print("BAG COUNT:", count_contained_bags(TARGET_COLOR, {r.parent: r for r in rules}))


if __name__ == '__main__':
    solve()
