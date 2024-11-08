import pygame as pg
from typy.units.defs import Unit, MoveRequest


class Player(Unit):
    walk_front_direction: tuple[int, int]
    body_front_direction: tuple[int, int]

    def __init__(self, coord: tuple[int, int]):
        super().__init__(coord)
        self.walk_front_direction = (0, 0)
        self.body_front_direction = (0, 1)

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

    def update_front_direction(self):
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

        if direction != (0, 0):
            self.body_front_direction = direction

        self.walk_front_direction = direction

    def request_move(self):
        if not self.ready_to_move():
            return
        if self.walk_front_direction == (0, 0):
            return
        request = MoveRequest(self.walk_front_direction, self.coord)
        return request

    def get_facing_coord(self):
        return (
            self.coord[0] + self.body_front_direction[0],
            self.coord[1] + self.body_front_direction[1],
        )

    def apply_move_request(self, request: MoveRequest):
        self.move(request.next_coord(), 10)
