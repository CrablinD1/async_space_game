import curses
import random
import time

from space_garbage import fly_garbage
from animate_spaceship import animate_spaceship
from blink_stars import blink
from fire import fire

STARS = ["+", "*", ".", ":"]
TIC_TIMEOUT = 0.1


def draw(canvas):
    canvas.nodelay(True)
    max_screen_y, max_screen_x = canvas.getmaxyx()
    columns_stars = [x for x in range(1, max_screen_x - 1)]
    rows_start = [y for y in range(1, max_screen_y - 1)]
    curses.curs_set(False)

    stars = [
        blink(canvas, random.choice(rows_start), random.choice(columns_stars),
              random.choice(STARS)) for _ in range(100)]

    shot = fire(canvas, start_row=max_screen_y / 2,
                start_column=max_screen_x / 2)

    space_ship = animate_spaceship(canvas, row=max_screen_y / 2,
                                   column=max_screen_x / 2 - 2)

    with open("./space_garbage/duck.txt", "r") as f:
        garb_1 = f.read()
    with open("./space_garbage/hubble.txt", "r") as f:
        garb_2 = f.read()
    with open("./space_garbage/lamp.txt", "r") as f:
        garb_3 = f.read()

    garbage_frames = [garb_1, garb_2, garb_3]
    # space_garbate = fly_garbage(canvas, column=10, garbage_frame=garb_1)
    garbage = [
        fly_garbage(canvas, column=random.randint(0, max_screen_x), garbage_frame=random.choice(garbage_frames))
    ]
    coroutines = [*stars, shot, space_ship, *garbage]

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines) == 0:
            break
        canvas.border()
        canvas.refresh()
        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
