import pygame as pg
from perungo.units.defs import Unit


class Wall(Unit):
    def draw(self, screen: pg.Surface, block_pixel_width: int, block_pixel_height: int):
        true_coord = self.get_true_coord()
        pg.draw.rect(
            screen,
            (0, 0, 255),
            pg.Rect(
                true_coord[0] * block_pixel_width,
                true_coord[1] * block_pixel_height,
                block_pixel_width,
                block_pixel_height,
            ),
        )
