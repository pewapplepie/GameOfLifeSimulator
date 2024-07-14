import collections
from typing import Set, Tuple
import numpy as np


def findLives(live: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    count = collections.Counter()
    for i, j in live:
        for x in range(i - 1, i + 2):
            for y in range(j - 1, j + 2):
                if x == i and y == j:
                    continue
                count[x, y] += 1
    result = set()
    for (i, j), cnt in count.items():
        if cnt == 3 or (cnt == 2 and (i, j) in live):
            result.add((i, j))
    return result


def updateBoard(live: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    return findLives(live)


# Define patterns
patterns = {
    "Tub": [(1, 2), (2, 1), (2, 3), (3, 2)],
    "Block": [(1, 1), (1, 2), (2, 1), (2, 2)],
    "Loaf": [(1, 2), (1, 3), (2, 1), (2, 4), (3, 2), (3, 4), (4, 3)],
    "Blinker": [(1, 2), (2, 2), (3, 2)],
    "Toad": [(2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3)],
    "Glider": [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)],
    "Light-weight spaceship": [
        (1, 2),
        (1, 3),
        (1, 4),
        (1, 5),
        (2, 1),
        (2, 5),
        (3, 5),
        (4, 1),
        (4, 4),
    ],
    "Middle-weight spaceship": [
        (1, 3),
        (1, 4),
        (1, 5),
        (1, 6),
        (2, 2),
        (2, 6),
        (3, 6),
        (4, 2),
        (4, 5),
    ],
    "Heavy-weight spaceship": [
        (1, 4),
        (1, 5),
        (1, 6),
        (1, 7),
        (2, 3),
        (2, 7),
        (3, 7),
        (4, 3),
        (4, 6),
    ],
    "Gosper glider gun": [
        (5, 1),
        (5, 2),
        (6, 1),
        (6, 2),
        (5, 11),
        (6, 11),
        (7, 11),
        (4, 12),
        (8, 12),
        (3, 13),
        (9, 13),
        (3, 14),
        (9, 14),
        (6, 15),
        (4, 16),
        (8, 16),
        (5, 17),
        (6, 17),
        (7, 17),
        (6, 18),
        (3, 21),
        (4, 21),
        (5, 21),
        (3, 22),
        (4, 22),
        (5, 22),
        (2, 23),
        (6, 23),
        (1, 25),
        (2, 25),
        (6, 25),
        (7, 25),
        (3, 35),
        (4, 35),
        (3, 36),
        (4, 36),
    ],
}


def rotate_pattern(pattern, rotation):
    if rotation == 0:
        return pattern
    elif rotation == 90:
        return [(c, -r) for r, c in pattern]
    elif rotation == 180:
        return [(-r, -c) for r, c in pattern]
    elif rotation == 270:
        return [(-c, r) for r, c in pattern]


def place_pattern(pattern_name, live_cells, board_size):
    pattern = patterns[pattern_name]

    if pattern_name == "Gosper glider gun":
        center_offset = (
            board_size[0] // 2 - max(r for r, _ in pattern) // 2,
            board_size[1] // 2 - max(c for _, c in pattern) // 2,
        )
        new_live_cells = {
            (r + center_offset[0], c + center_offset[1]) for r, c in pattern
        }
        return live_cells | new_live_cells

    rotation = np.random.choice([0, 90, 180, 270])
    rotated_pattern = rotate_pattern(pattern, rotation)
    offset = (
        np.random.randint(0, board_size[0] - 4),
        np.random.randint(0, board_size[1] - 4),
    )
    new_live_cells = {(r + offset[0], c + offset[1]) for r, c in rotated_pattern}
    return live_cells | new_live_cells
