import random


def load_stage():
    # 0 - empty
    # 1 - blocks
    # 2 - player
    # 3 - enemy
    # 4 - wall
    stage = [
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 3, 1, 0, 4],
        [4, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 4],
        [4, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 0, 0, 4],
        [4, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 4],
        [4, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4],
        [4, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 4],
        [4, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 4],
        [4, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 4],
        [4, 3, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1, 3, 4],
        [4, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 4],
        [4, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4],
        [4, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 3, 1, 0, 4],
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [4, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 4],
        [4, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
    ]

    # randomly flip the stage
    if random.randint(0, 1):
        stage = [row[::-1] for row in stage]
    if random.randint(0, 1):
        stage = stage[::-1]

    return stage


def get_coords_of_number(stage: list[list[int]], number: int):
    coords: list[tuple[int, int]] = []
    for y, row in enumerate(stage):
        for x, cell in enumerate(row):
            if cell == number:
                coords.append((x, y))
    return coords
