import pygame as pg
from typy.stage import load_stage, get_coords_of_number
import random


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


class Block(Unit):
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


class GameState:
    player: Player
    enemies: list[Enemy]
    blocks: list[Block]
    walls: list[Wall]
    stage_width: int
    stage_height: int
    block_pixel_width: int
    block_pixel_height: int

    def __init__(self, stage: list[list[int]], screen: pg.Surface):
        self.stage = stage
        self.stage_width = len(stage[0])
        self.stage_height = len(stage)
        self.block_pixel_width = screen.get_width() // self.stage_width
        self.block_pixel_height = screen.get_height() // self.stage_height
        self.player = Player(get_coords_of_number(stage, 2)[0])
        self.enemies = [Enemy(coord) for coord in get_coords_of_number(stage, 3)]
        self.blocks = [Block(coord) for coord in get_coords_of_number(stage, 1)]
        self.walls = [Wall(coord) for coord in get_coords_of_number(stage, 4)]

    def get_units(self):
        return [self.player] + self.enemies + self.blocks + self.walls

    def get_occupied_coords_by_walls(self):
        walls = [wall.get_occupied_coords() for wall in self.walls]
        return [coord for wall in walls for coord in wall]

    def get_occupied_coords_by_blocks(self):
        blocks = [block.get_occupied_coords() for block in self.blocks]
        return [coord for block in blocks for coord in block]

    def draw(self, screen: pg.Surface):
        screen.fill((20, 20, 20))

        wall_coords = self.get_occupied_coords_by_walls()
        block_coords = self.get_occupied_coords_by_blocks()

        for enemy in self.enemies:
            enemy.walk(wall_coords, block_coords)

        for unit in self.get_units():
            unit.draw(screen, self.block_pixel_width, self.block_pixel_height)
            unit.update_coords()


def main():
    pg.init()
    screen = pg.display.set_mode((450, 450))
    pg.display.set_caption("Perungo")

    stage = load_stage()

    game_state = GameState(stage, screen)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
        game_state.draw(screen)
        pg.display.flip()
        pg.time.delay(1000 // 60)


if __name__ == "__main__":
    main()
