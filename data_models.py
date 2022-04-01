import dataclasses
from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np

color_mapper = {
    "Y": "🟨",
    "G": "🟩",
    "B": "🟦",
    "R": "🟥",
    "P": "🟪",
    "O": "🟧",
    "W": "⬜",
}


@dataclass(frozen=True)
class Block:
    block_id: int
    width: int
    height: int
    color: str
    values: np.array  # Note: first row is the bottom, values are flipped when printing the result

    def __post_init__(self):
        if self.width != len(self.values[0]) or self.height != len(self.values):
            raise Exception(
                f"This block with width {self.width}, height: {self.height} and values {self.values} does not exist"
            )

    def __repr__(self):
        result_str = "Block:\n"
        for row in reversed(self.values):
            for item in row:
                result_str += color_mapper[item] if item else "⬜️"
            result_str += "\n"
        return result_str


@dataclass(frozen=True)
class Rewards:
    points: Dict[str, int]
    multiplication_factors: Dict[str, int]


@dataclass()
class Field:
    width: int
    height: int
    values: Optional[
        np.ndarray
    ] = None  # Note: first row is the bottom, values are flipped when printing the result

    def __post_init__(self):
        self.values = np.empty((self.height, self.width), dtype=str)
        self.values[:] = ""

    def __repr__(self):
        result_str = "⬛️" * (self.width + 2) + "\n"
        for row in reversed(self.values):
            result_str += "⬛️"
            for item in row:
                result_str += color_mapper[item] if item else "⬜"
            result_str += "⬛️\n"
        result_str += "⬛️" * (self.width + 2)
        return result_str

    def clear_field(self):
        self.values[:] = ""


@dataclass()
class Solution:
    """A solution comprises two lists that describe which blocks are dropped in what order and where
    - order: order of the list
    - which blocks: determined by block_ids
    - where: most left part of the block is dropped at block_position
    """

    block_ids: List[int] = dataclasses.field(default_factory=list)
    block_positions: List[int] = dataclasses.field(default_factory=list)
