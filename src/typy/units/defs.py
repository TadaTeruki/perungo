import pygame as pg


class Unit:
    coord: tuple[int, int]
    next_coord: tuple[int, int]

    current_frame: int
    duration: int

    def __init__(self, coord: tuple[int, int]):
        self.coord = coord
        self.next_coord = coord
        self.current_frame = 0
        self.duration = 1

    def get_4_directions(self):
        return [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

    def ready_to_move(self):
        return self.coord == self.next_coord

    def move(self, next: tuple[int, int], duration: int):
        self.next_coord = next
        self.duration = duration
        self.current_frame = 0

    def update_coords(self):
        if self.current_frame < self.duration:
            self.current_frame += 1
        else:
            self.coord = self.next_coord

    def get_true_coord(self):
        return (
            float(self.coord[0])
            + (self.next_coord[0] - self.coord[0]) * self.current_frame / self.duration,
            float(self.coord[1])
            + (self.next_coord[1] - self.coord[1]) * self.current_frame / self.duration,
        )

    def draw(self, screen: pg.Surface, block_pixel_width: int, block_pixel_height: int):
        pass

    def get_occupied_coords(self):
        if self.coord == self.next_coord:
            return [self.coord]
        return [self.coord, self.next_coord]


class MoveRequest:
    direction: tuple[int, int]
    current_coord: tuple[int, int]
    rejected: bool

    def __init__(self, direction: tuple[int, int], current_coord: tuple[int, int]):
        self.direction = direction
        self.current_coord = current_coord
        self.rejected = False

    def next_coord(self):
        next = (
            self.current_coord[0] + self.direction[0],
            self.current_coord[1] + self.direction[1],
        )
        return next

    def reject(self):
        self.rejected = True

    def applied(self):
        return not self.rejected
