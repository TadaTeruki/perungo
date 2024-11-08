import pygame as pg


def main():
    pg.init()
    screen = pg.display.set_mode((800, 600))
    pg.display.set_caption("Typy")

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return
        screen.fill((100, 250, 250))
        pg.draw.circle(screen, (250, 100, 100), (400, 300), 100)
        pg.display.flip()


if __name__ == "__main__":
    main()
