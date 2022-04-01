from pathlib import Path
from typing import List, Tuple

import numpy as np

from dropblox.data_models import Block, Field, Rewards, Solution


def write_file(solution: Solution, filename: str) -> None:
    """Write an output file containing a solution block list"""
    with open(filename, "w") as fp:
        for block_id, block_position in zip(
            solution.block_ids, solution.block_positions
        ):
            print(f"{block_id} {block_position}", file=fp)


def parse_input_file(filename) -> Tuple[Field, List[Block], Rewards]:
    lines = Path(filename).read_text().splitlines()

    width, height = map(int, lines.pop(0).split())
    field = Field(width, height)

    nr_blocks, nr_rewards = map(int, lines.pop(0).split())

    blocks = []
    for block_id in range(nr_blocks):
        width, height, color = lines.pop(0).split()
        width, height = int(width), int(height)
        values = [
            "" if v == "0" else v for v in lines.pop(0).split()
        ]  # replace 0 with empty string for empty value
        values = np.reshape(values, (height, width))
        blocks.append(Block(block_id, width, height, color, values))

    points = {}
    multiplication_factors = {}
    for i in range(nr_rewards):
        color, point, multiplication_factor = lines.pop(0).split()
        points[color] = int(point)
        multiplication_factors[color] = int(multiplication_factor)

    return field, blocks, Rewards(points, multiplication_factors)


def parse_solution(data: str) -> Solution:
    solution = Solution()
    for line in data.splitlines():
        block_id, block_position = map(int, line.split())
        solution.block_ids.append(block_id)
        solution.block_positions.append(block_position)

    return solution


def parse_solution_file(filename: str) -> Solution:
    """Read and parse a solution from file"""
    fp = open(filename, "r")
    lines = fp.readlines()
    solution = Solution()
    for line in lines:
        block_id, block_position = map(int, line.split())
        solution.block_ids.append(block_id)
        solution.block_positions.append(block_position)

    return solution


def drop_blocks(field: Field, blocks: List[Block], solution: Solution) -> None:
    """Drop the blocks for the solution in the playing field"""
    if len(solution.block_ids) != len(set(solution.block_ids)):
        raise Exception("You can only use each block once")
    if (max(solution.block_ids) >= len(blocks)) or (min(solution.block_ids) < 0):
        raise Exception("You used a block id that doesn't exist")

    for block_id, block_position in zip(solution.block_ids, solution.block_positions):
        add_block(field, blocks[block_id], block_position)


def add_block(field: Field, block: Block, x: int) -> None:
    """Try to add the block on position x;
    If it fits then update the field, if not then raise exception.

    x: position of the most left part of the block
    """
    y = field.height - block.height
    fits_somewhere = False
    while fit(field, block, x, y):
        fits_somewhere = True
        y -= 1

    if not fits_somewhere:
        raise Exception(f"{block} does not fit on x: {x}")
    update(field, block, x, y + 1)


def fit(field: Field, block: Block, x: int, y: int) -> bool:
    """Check if the block fits with the left bottom on (x, y)

    field: where field.values is an array where first row is the bottom of the playing field
    block: where block.values is an array where first row is the bottom of the block
    x, y: start position of left bottom of the block's bounding box
    """
    out_of_bounds_on_the_right = x + block.width > field.width
    out_of_bounds_on_the_top = y + block.height > field.height
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
    selected_field_area = field.values[y : y + block.height, x : x + block.width]
    for block_row, field_row in zip(block.values, selected_field_area):
        for block_value, field_value in zip(block_row, field_row):
            # block fits if: field value or block value is an empty string
            if block_value and field_value:
                return False
    return True


def update(field: Field, block: Block, x: int, y: int) -> None:
    """Update the field by dropping the block on position (x,y)"""
    for update_y, block_row in zip(range(y, y + block.height), block.values):
        field_row = field.values[update_y][x : x + block.width]

        # make sure we don't overwrite an existing field block if the block
        # has an empty space where in the field the value is filled
        new_row = [f if f else b for f, b in zip(field_row, block_row)]
        field.values[update_y][x : x + block.width] = new_row
