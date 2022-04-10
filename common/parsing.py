from pathlib import Path
from typing import List, Tuple

import numpy as np

from common.data_models import Block, Field, Rewards, Solution


def parse_puzzle(filename: str) -> Tuple[Field, List[Block], Rewards]:
    """Parse puzzle specification into a Field, Block list and Rewards."""
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


def parse_solution(filename: str) -> Solution:
    """Read and parse a solution from file"""
    fp = open(filename, "r")
    lines = fp.readlines()
    solution = Solution()
    for line in lines:
        block_id, block_position = map(int, line.split())
        solution.block_ids.append(block_id)
        solution.block_positions.append(block_position)

    return solution
