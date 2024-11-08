import random
import pygame as pg
from typy.units.defs import Unit


class Enemy(Unit):
    prev_direction: tuple[int, int]
    aggressive: int

    def __init__(self, coord: tuple[int, int]):
        super().__init__(coord)
        self.prev_direction = (0, 0)
        self.aggressive = 0

    def is_aggressive(self):
        return self.aggressive > 0

    def walk(
        self, wall_coords: list[tuple[int, int]], block_coords: list[tuple[int, int]]
    ):
        if not self.ready_to_move():
            return

        # randomly change its mode
        if random.randint(0, 100) < 4 and not self.is_aggressive():
            self.aggressive = 30

        if self.is_aggressive():
            self.aggressive -= 1

        directions = self.get_4_directions()

        if self.prev_direction != (0, 0):
            directions += [self.prev_direction for _ in range(10)]

        coords_to_avoid = wall_coords + block_coords
        if self.is_aggressive():
            coords_to_avoid = wall_coords

        next_coords = [(self.coord[0] + d[0], self.coord[1] + d[1]) for d in directions]

        next_coords = [coord for coord in next_coords if coord not in coords_to_avoid]

        if next_coords:
            index = random.randint(0, len(next_coords) - 1)
            next_coord = next_coords[index]

            direction = next_coord[0] - self.coord[0], next_coord[1] - self.coord[1]
            if self.is_aggressive() and next_coord in block_coords:
                self.move(next_coord, 40)
            else:
                self.move(next_coord, 20)
            self.prev_direction = direction

    def draw(self, screen: pg.Surface, block_pixel_width: int, block_pixel_height: int):
        true_coord = self.get_true_coord()
        center = (
            true_coord[0] * block_pixel_width + block_pixel_width // 2,
            true_coord[1] * block_pixel_height + block_pixel_height // 2,
        )

        radius = block_pixel_width // 2

        if self.is_aggressive() and self.current_frame % 20 < 10:
            pg.draw.circle(
                screen,
                (0, 100, 255),
                center,
                radius,
            )
        else:
            pg.draw.circle(
                screen,
                (0, 255, 0),
                center,
                radius,
            )
