# 🟨🟦🟥 DropBlox 🟩🟧🟪 

Welcome! I'm assuming you came here to give this coding challenge a try, great! After all, you could be the one to take home the big prize... So, let's get right to it!

## Quickstart 🎬

You can either:

1. Open the Colab example

    [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1NmfslkeZ4TWp-PZmq6XqWjoZhABoV82W?usp=sharing)

    OR

2. Clone this repo

    ```shell
    git clone https://github.com/godatadriven/dropblox.git
    ```

    and open `quick_start.ipynb` ✓

> Check out the Quickstart example in the provided notebook on how to generate the solutions file.


## Challenge and Rules 📜

The task is simple: given a rectangular field and a set of predefined blocks, fill the field with the blocks in a way to maximize your score.

How do you score high? That depends on the colors of the blocks you used, the rows you filled and the amount of empty tiles in the final field. 

### > Field

You are given a `Field` object `field` with `field.height = field.width = 100`. Initially it is empty, but you can drop blocks in the field which will change the array `field.values`. To make it visual, simply print your field and view the result in a text editor.

### > Blocks

Blocks have a shape, a color and a unique ID. They are defined as instances of the class `Block`. The list of available blocks is defined as `blocks` in the provided notebook. Similar as with the field, we can visualize the blocks. The first block, `B = blocks[0]` with `B.block_id = 0`, looks like this:
```
🟧🟧🟧
🟧⬜️🟧
⬜️⬜️🟧
```
This is an orange block, so `B.color = "O"`, and it has `B.width = B.height = 3`. 

Blocks can be dropped into the field from top to bottom, and they stop falling until they hit another block or the bottom of the field. Blocks are dropped in the field *as is*, so they cannot be rotated. Also, a block can only be dropped once, but you don't have to use all of the provided blocks. 

Okay, now we can drop this block in our field, but how do we decide where to drop it?

### > Rewards

Each color has a number of *points* and a *multiplication factor*. These will determine your score, once you dropped some of blocks in the field. The values for each color are defined under `rewards`. For example, for orange, we have `rewards.points["O"] = 5` and `rewards.multiplication_factors["O"] = 
3`. 

This means: for every orange tile in our final field, we get +5 points. So just by dropping the orange block from above we would already get +30 points. 

With the multiplication factor, things can get crazy: if the *<ins>entire row</ins>* is filled with tiles of the *<ins> same color</ins>*, you get the values of those tiles multiplied by the corresponding factor. 

Lastly, you can get minus points. If a row contains at least one colored tile, all empty tiles in that row count as -1 towards your final score.

That should help you decide which blocks to drop, and where!

The rewards are like follows:

| Emoji | Color code | Points | Multiplication factor |
|-------|------------|--------|-----------------------|
| 🟦     | "B"        | 100    | 0                     |
| 🟨     | "Y"        | 1      | 3                     |
| 🟩     | "G"        | 3      | 1                     |
| 🟪     | "P"        | 5      | 2                     |
| 🟧     | "O"        | 5      | 3                     |
| 🟥     | "R"        | 8      | 4                     |


## Your Solution 💻

Your solution should be a `.txt` file where each line specifies which block (by block ID) to drop in the field, and at which x-coordinate. To clarify, the *bottom left* of the block will be dropped at the provided x-coordinate in the field.

For exmple, you could write `solution.txt` with:
```
322 54
12 4
...
```
which tells us to first drop the block with `block_id = 322` at x-coordinate `54`, and then drop the block with `block_id = 12` at x-coordinate `4`, etc.

Submit your solution `.txt` at: https://dropblox.azurewebsites.net/submit.

> Note: loading the website may take a moment - it sleeps when not used. If loading fails, please try again.

<br>
Good luck! 💪🏻

## Leaderboard 🏆

https://dropblox.azurewebsites.net/leaderboard

## Contact

dropblox@godatadriven.com

## About
> This challenge is hosted by [GoDataDriven](https://godatadriven.com/) for PyData Eindhoven 2022.
