import pygame as pg
from typy.units.defs import Unit, MoveRequest


class Player(Unit):
    def draw(self, screen: pg.Surface, block_pixel_width: int, block_pixel_height: int):
        true_coord = self.get_true_coord()
        pg.draw.circle(
            screen,
            (255, 0, 0),
            (
                true_coord[0] * block_pixel_width + block_pixel_width // 2,
                true_coord[1] * block_pixel_height + block_pixel_height // 2,
            ),
            block_pixel_width // 2,
        )

    def request_move(self):
        if not self.ready_to_move():
            return

        keys = pg.key.get_pressed()
        direction = (0, 0)
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            direction = (-1, 0)
        elif keys[pg.K_RIGHT] or keys[pg.K_d]:
            direction = (1, 0)
        elif keys[pg.K_UP] or keys[pg.K_w]:
            direction = (0, -1)
        elif keys[pg.K_DOWN] or keys[pg.K_s]:
            direction = (0, 1)

        request = MoveRequest(direction, self.coord)
        return request

    def apply_move_request(self, request: MoveRequest):
        self.move(request.next_coord(), 10)
