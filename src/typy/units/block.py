import pygame as pg
from typy.units.defs import Unit


class Block(Unit):
    slide_direction: tuple[int, int]

    def __init__(self, coord: tuple[int, int]):
        super().__init__(coord)
        self.slide_direction = (0, 0)

    def draw(self, screen: pg.Surface, block_pixel_width: int, block_pixel_height: int):
        true_coord = self.get_true_coord()
        pg.draw.rect(
            screen,
            (40, 80, 160),
            pg.Rect(
                true_coord[0] * block_pixel_width,
                true_coord[1] * block_pixel_height,
                block_pixel_width,
                block_pixel_height,
            ),
        )

    def start_slide(self, direction: tuple[int, int]):
        self.slide_direction = direction

    def slide(
        self,
        direction: tuple[int, int],
        wall_coords: list[tuple[int, int]],
        block_coords: list[tuple[int, int]],
    ):
        if not self.ready_to_move():
            return

        next_coord = (self.coord[0] + direction[0], self.coord[1] + direction[1])
        if next_coord in wall_coords or next_coord in block_coords:
            self.slide_direction = (0, 0)
            return

        self.move(
            (self.coord[0] + direction[0], self.coord[1] + direction[1]),
            4,
        )
