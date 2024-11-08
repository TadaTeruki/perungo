import random
import pygame as pg
from typy.units.defs import Unit


class Enemy(Unit):
    prev_direction: tuple[int, int]

    def __init__(self, coord: tuple[int, int]):
        super().__init__(coord)
        self.prev_direction = (0, 0)

    def walk(
        self, wall_coords: list[tuple[int, int]], block_coords: list[tuple[int, int]]
    ):
        if not self.ready_to_move():
            return

        directions = self.get_4_directions()

        if self.prev_direction != (0, 0):
            directions += [self.prev_direction for _ in range(10)]

        next_coords = [(self.coord[0] + d[0], self.coord[1] + d[1]) for d in directions]

        next_coords = [
            coord
            for coord in next_coords
            if coord not in wall_coords and coord not in block_coords
        ]

        if next_coords:
            index = random.randint(0, len(next_coords) - 1)
            next_coord = next_coords[index]

            direction = next_coord[0] - self.coord[0], next_coord[1] - self.coord[1]

            self.move(next_coord, 20)
            self.prev_direction = direction

    def draw(self, screen: pg.Surface, block_pixel_width: int, block_pixel_height: int):
        true_coord = self.get_true_coord()
        pg.draw.circle(
            screen,
            (0, 255, 0),
            (
                true_coord[0] * block_pixel_width + block_pixel_width // 2,
                true_coord[1] * block_pixel_height + block_pixel_height // 2,
            ),
            block_pixel_width // 2,
        )
