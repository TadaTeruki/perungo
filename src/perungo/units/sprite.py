import pygame as pg


class Sprite:
    images: list[pg.Surface]

    def __init__(
        self,
        sprite: list[list[int]],
        color_patterns: list[list[tuple[int, int, int]]],
        flip_x: bool = False,
        flip_y: bool = False,
    ):
        width = len(sprite[0])
        height = len(sprite)
        self.images = []

        for i in range(len(color_patterns)):
            image = pg.Surface((width, height))
            image.set_colorkey((255, 0, 0))

            for row_idx, row in enumerate(sprite):
                for col_idx, pixel in enumerate(row):
                    color = color_patterns[i][pixel]
                    image.set_at((col_idx, row_idx), color)

            image = pg.transform.flip(image, flip_x, flip_y)

            self.images.append(image)

    def draw(
        self,
        screen: pg.Surface,
        x: float,
        y: float,
        pattern: int,
        width: float,
        height: float,
    ):
        screen.blit(pg.transform.scale(self.images[pattern], (width, height)), (x, y))
