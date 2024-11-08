import pygame as pg
from typy.units.defs import Unit


class Block(Unit):
    slide_direction: tuple[int, int]
    break_count: int
    max_break_count: int
    enemies_num_carrying: int

    def __init__(self, coord: tuple[int, int]):
        super().__init__(coord)
        self.slide_direction = (0, 0)
        self.break_count = 0
        self.max_break_count = 20
        self.enemies_num_carrying = 0

    def draw(self, screen: pg.Surface, block_pixel_width: int, block_pixel_height: int):
        true_coord = self.get_true_coord()

        broken_prop = float(self.break_count) / float(self.max_break_count)
        rect = pg.Rect(
            true_coord[0] * block_pixel_width,
            true_coord[1] * block_pixel_height,
            block_pixel_width,
            block_pixel_height,
        )
        color = (40, 80, 220)
        if self.break_count > 0:
            if self.break_count == self.max_break_count:
                return
            pg.draw.rect(
                screen,
                color,
                rect,
                int(float(block_pixel_width) * 0.5 * (1.0 - broken_prop)),
            )
        else:
            pg.draw.rect(screen, color, rect)

        if self.enemies_num_carrying > 0:
            rect_width = int(block_pixel_width * 0.3)
            rect_height = int(block_pixel_height * 0.3)
            if self.slide_direction[1] != 0:
                rect_width = int(block_pixel_width * 1.2)
            if self.slide_direction[0] != 0:
                rect_height = int(block_pixel_height * 1.2)

            rect_center_x = self.slide_direction[0] * block_pixel_width * 0.5 + 0.5
            rect_center_y = self.slide_direction[1] * block_pixel_height * 0.5 + 0.5

            rect_x = block_pixel_width * 0.5 - rect_width * 0.5 + rect_center_x
            rect_y = block_pixel_height * 0.5 - rect_height * 0.5 + rect_center_y

            pg.draw.rect(
                screen,
                (0, 255, 0),
                pg.Rect(
                    true_coord[0] * block_pixel_width + rect_x,
                    true_coord[1] * block_pixel_height + rect_y,
                    rect_width,
                    rect_height,
                ),
            )

    def add_enemy(self):
        self.enemies_num_carrying += 1

    def start_slide(self, direction: tuple[int, int]):
        self.slide_direction = direction

    def slide(
        self,
        direction: tuple[int, int],
        wall_coords: list[tuple[int, int]],
        block_coords: list[tuple[int, int]],
    ):
        if not self.ready_to_move():
            return 0

        next_coord = (self.coord[0] + direction[0], self.coord[1] + direction[1])
        if next_coord in wall_coords or next_coord in block_coords:
            self.slide_direction = (0, 0)
            carried = self.enemies_num_carrying
            self.enemies_num_carrying = 0
            return carried

        self.move(
            (self.coord[0] + direction[0], self.coord[1] + direction[1]),
            4,
        )

        return 0

    def sliding(self):
        return self.slide_direction != (0, 0)

    def start_breaking(self):
        if self.break_count > 0:
            return
        self.break_count += 1

    def broken(self):
        return self.break_count == self.max_break_count

    def update_break(self):
        if self.break_count > 0 and self.break_count < self.max_break_count:
            self.break_count += 1
