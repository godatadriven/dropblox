from common.data_models import Block
from typing import List
import numpy as np


def get_random_block(blocks: List[Block]):
    """
    Get a random block from the given list.
    """
    return np.random.choice(blocks)


def get_blocks_of_color(blocks: List[Block], color: str) -> List[Block]:
    """
    Filter the list of blocks by only the given color.

    Color codes are as follows:

    | Emoji | Color code | Points | Multiplication factor |
    |-------|------------|--------|-----------------------|
    | 🟦     | "B"        | 100    | 0                     |
    | 🟨     | "Y"        | 1      | 3                     |
    | 🟩     | "G"        | 3      | 1                     |
    | 🟪     | "P"        | 5      | 2                     |
    | 🟧     | "O"        | 5      | 3                     |
    | 🟥     | "R"        | 8      | 4                     |
    """

    def color_only(color: str):
        return lambda block: block.color == color

    return list(filter(color_only(color), blocks))
