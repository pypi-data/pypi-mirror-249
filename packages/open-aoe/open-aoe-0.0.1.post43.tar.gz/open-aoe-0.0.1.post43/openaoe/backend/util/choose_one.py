import random
from typing import List


def choose_one(items: List):
    if len(items) == 1:
        return items[0]
    return random.choice(items)


def choose_one_with_weight(items: List, weights: List):
    if len(items) == 1:
        return items[0]
    return random.choices(items, weights=weights, k=1)[0]


if __name__ == "__main__":

    pass
