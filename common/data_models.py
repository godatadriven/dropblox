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
class Solution:
    """A solution comprises two lists that describe which blocks are dropped in what order and where
    - order: order of the list
    - which blocks: determined by block_ids
    - where: most left part of the block is dropped at block_position
    """

    block_ids: List[int] = dataclasses.field(default_factory=list)
    block_positions: List[int] = dataclasses.field(default_factory=list)


@dataclass()
class Field:
    width: int
    height: int
    values: Optional[
        np.ndarray
    ] = None  # Note: first row is the bottom, values are flipped when printing the result
    block_ids: Optional[List[int]] = None
    block_positions: Optional[List[int]] = None

    def __post_init__(self):
        self.values = np.empty((self.height, self.width), dtype=str)
        self.clear_field()

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
        self.block_ids = []
        self.block_positions = []

    def fit(self, block: Block, x: int, y: int) -> bool:
        """Check if the block fits with the left bottom on (x, y)

        field: where field.values is an array where first row is the bottom of the playing field
        block: where block.values is an array where first row is the bottom of the block
        x, y: start position of left bottom of the block's bounding box
        """
        out_of_bounds_on_the_right = x + block.width > self.width
        out_of_bounds_on_the_top = y + block.height > self.height
        out_of_bounds_on_the_left = x < 0
        out_of_bounds_on_the_bottom = y < 0
        if (
            out_of_bounds_on_the_right
            or out_of_bounds_on_the_top
            or out_of_bounds_on_the_bottom
            or out_of_bounds_on_the_left
        ):
            return False

        # select area of the field where the block should fit
        selected_field_area = self.values[y: y +
                                          block.height, x: x + block.width]
        for block_row, field_row in zip(block.values, selected_field_area):
            for block_value, field_value in zip(block_row, field_row):
                # block fits if: field value or block value is an empty string
                if block_value and field_value:
                    return False
        return True

    def update(self, block: Block, x: int, y: int) -> None:
        """Update the field by dropping the block on position (x,y)"""
        for update_y, block_row in zip(range(y, y + block.height), block.values):
            field_row = self.values[update_y][x: x + block.width]

            # make sure we don't overwrite an existing field block if the block
            # has an empty space where in the field the value is filled
            new_row = [f if f else b for f, b in zip(field_row, block_row)]
            self.values[update_y][x: x + block.width] = new_row

    def drop_block(self, block: Block, x: int) -> None:
        """Try to add the block on position x;
        If it fits then update the field, if not then raise exception.

        x: position of the most left part of the block
        """
        if block.block_id in self.block_ids:
            raise Exception(
                f"Block {block.block_id} was already used. You can only use each block once."
            )
        y = self.height - block.height
        fits_somewhere = False
        while self.fit(block, x, y):
            fits_somewhere = True
            y -= 1

        if not fits_somewhere:
            raise Exception(f"{block} does not fit on x: {x}")
        self.update(block, x, y + 1)
        self.block_ids.append(block.block_id)
        self.block_positions.append(x)

    def drop_blocks(self, blocks: List[Block], solution: Solution) -> None:
        """Drop the blocks for the solution in the playing field"""
        if len(solution.block_ids) != len(set(solution.block_ids)):
            raise Exception("You can only use each block once")
        if (max(solution.block_ids) >= len(blocks)) or (min(solution.block_ids) < 0):
            raise Exception("You used a block id that doesn't exist")

        for block_id, block_position in zip(solution.block_ids, solution.block_positions):
            self.drop_block(blocks[block_id], block_position)

    def score_row(self, row: np.array, rewards: Rewards) -> int:
        def color_points(row: list, rewards: Rewards) -> int:
            score = 0
            for color in row:
                if color == "":
                    score -= 1
                else:
                    score += rewards.points[color]
            return score

        def multiplication_factor_for_full_color_row(row: list, rewards: Rewards) -> int:
            if row[0] != "" and len(set(row)) == 1:
                return rewards.multiplication_factors[row[0]]
            return 1

        full_row = not any(row == "")
        empty_row = "".join(row) == ""
        score = 0
        if not empty_row:
            score += color_points(row, rewards)
        if full_row:
            score *= multiplication_factor_for_full_color_row(row, rewards)
        return score

    def score_solution(self, rewards: Rewards) -> int:
        score = 0
        for row in self.values:
            score += self.score_row(row, rewards)
        return score

    def write_solution(self, filename: str) -> None:
        """Write an output file containing a solution block list"""
        with open(filename, "w") as fp:
            for block_id, block_position in zip(
                self.block_ids, self.block_positions
            ):
                print(f"{block_id} {block_position}", file=fp)
