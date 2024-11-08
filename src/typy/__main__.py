import pygame as pg
from typy.stage import load_stage, get_coords_of_number
from typy.units.block import Block
from typy.units.enemy import Enemy
from typy.units.player import Player
from typy.units.wall import Wall


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
        return self.blocks + self.walls + self.enemies + [self.player]

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

        player_req = self.player.request_move()

        movable_block_indices: list[int] = []
        if player_req:
            if player_req.next_coord() in wall_coords:
                player_req.reject()

            for i, block in enumerate(self.blocks):
                if player_req.next_coord() == block.coord:
                    block_next_coord = (
                        block.coord[0] + player_req.direction[0],
                        block.coord[1] + player_req.direction[1],
                    )
                    if (
                        block_next_coord not in wall_coords
                        and block_next_coord not in block_coords
                    ):
                        movable_block_indices.append(i)
                    else:
                        player_req.reject()

        if player_req and player_req.applied():
            self.player.apply_move_request(player_req)
            for i in movable_block_indices:
                self.blocks[i].start_slide(player_req.direction)

        for enemy in self.enemies:
            enemy.walk(wall_coords, block_coords)

        for block in self.blocks:
            block.slide(block.slide_direction, wall_coords, block_coords)

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
