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
    score: int
    cleared: bool
    gameover: bool

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
        self.score = 0
        self.cleared = False
        self.gameover = False

    def get_units(self):
        return self.walls + self.enemies + [self.player] + self.blocks

    def get_occupied_coords_by_walls(self):
        walls = [wall.get_occupied_coords() for wall in self.walls]
        return [coord for wall in walls for coord in wall]

    def get_occupied_coords_by_blocks(self):
        blocks = [block.get_occupied_coords() for block in self.blocks]
        return [coord for block in blocks for coord in block]

    def draw_units(self, screen: pg.Surface, update_coords: bool):
        for unit in self.get_units():
            unit.draw(screen, self.block_pixel_width, self.block_pixel_height)
            if update_coords:
                unit.update_coords()

    def draw(self, screen: pg.Surface):
        screen.fill((20, 20, 20))

        wall_coords = self.get_occupied_coords_by_walls()
        block_coords = self.get_occupied_coords_by_blocks()

        if self.gameover:
            self.draw_units(screen, False)

            font = pg.font.Font(None, self.block_pixel_height)
            text = font.render("GAME OVER", True, (255, 255, 255))
            screen.blit(
                text,
                (
                    screen.get_width() // 2 - self.block_pixel_width * 2,
                    screen.get_height() // 2,
                ),
            )
            return

        self.player.update_front_direction()
        player_req = self.player.request_move()

        movable_block_indices: list[int] = []
        if player_req:
            if player_req.next_coord() in wall_coords:
                player_req.reject()

            for i, block in enumerate(self.blocks):
                if player_req.next_coord() != block.coord:
                    continue

                block_next_coord = (
                    block.coord[0] + player_req.direction[0],
                    block.coord[1] + player_req.direction[1],
                )
                in_wall = block_next_coord in wall_coords
                in_block = block_next_coord in block_coords
                if not in_wall and not in_block:
                    movable_block_indices.append(i)
                else:
                    player_req.reject()

        if player_req and player_req.applied():
            self.player.apply_move_request(player_req)
            for i in movable_block_indices:
                self.blocks[i].start_slide(player_req.direction)
        elif self.player.ready_to_move():
            keys = pg.key.get_pressed()
            if keys[pg.K_RETURN]:
                for i, block in enumerate(self.blocks):
                    if self.player.get_facing_coord() == block.coord:
                        block.start_breaking()

        for enemy in self.enemies:
            enemy.walk(wall_coords, block_coords)

        enemy_indices_to_remove: list[int] = []
        for block in self.blocks:
            if block.broken():
                continue
            for i, enemy in enumerate(self.enemies):
                if block.overlap(enemy):
                    if block.sliding():
                        enemy_indices_to_remove.append(i)
                        block.add_enemy()
                    else:
                        block.start_breaking()
            carried_enemies = block.slide(
                block.slide_direction, wall_coords, block_coords
            )
            self.score += int(pow(carried_enemies, 1.8)) * 100
            block.update_break()

        self.blocks = [block for block in self.blocks if not block.broken()]
        self.enemies = [
            enemy
            for i, enemy in enumerate(self.enemies)
            if i not in enemy_indices_to_remove
        ]

        if any(
            self.player.coord in enemy.get_occupied_coords() for enemy in self.enemies
        ):
            self.gameover = True
            self.player.die()

        if (
            self.enemies == []
            and [block for block in self.blocks if block.sliding()] == []
        ):
            self.cleared = True

        self.draw_units(screen, True)

        if self.cleared and not self.gameover:
            font = pg.font.Font(None, self.block_pixel_height)
            text = font.render("YOU WIN!", True, (255, 255, 255))
            screen.blit(
                text,
                (
                    screen.get_width() // 2 - self.block_pixel_width * 1.5,
                    screen.get_height() // 2,
                ),
            )

        font = pg.font.Font(None, int(self.block_pixel_height))
        text = font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        screen.blit(text, (self.block_pixel_width, self.block_pixel_height / 3))
        font = pg.font.Font(None, int(self.block_pixel_height / 2.0))
        text = font.render(
            "[ARROW KEY] TO MOVE & PUSH BLOCKS/ [ENTER KEY] TO BREAK",
            True,
            (255, 255, 255),
        )
        screen.blit(
            text,
            (self.block_pixel_width, screen.get_height() - self.block_pixel_height / 2),
        )


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
