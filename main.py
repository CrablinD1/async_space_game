import curses
import random
import time
import asyncio
from tools import sleep

from space_garbage import fill_orbit_with_garbage
from animate_spaceship import animate_spaceship
from blink_stars import blink
from fire import fire
from curses_tools import read_controls

STARS = ["+", "*", ".", ":"]
TIC_TIMEOUT = 0.1


def draw(canvas):
    loop = asyncio.get_event_loop()
    canvas.nodelay(True)
    max_screen_y, max_screen_x = canvas.getmaxyx()
    columns_stars = [x for x in range(1, max_screen_x - 1)]
    rows_start = [y for y in range(1, max_screen_y - 1)]
    curses.curs_set(False)

    for n in range(100):
        loop.create_task(blink(canvas, random.choice(rows_start),
                               random.choice(columns_stars),
                               random.choice(STARS)))

    for i in range(5):
        loop.create_task(fill_orbit_with_garbage(canvas, max_screen_x))

    loop.create_task(animate_spaceship(canvas, row=max_screen_y / 2,
                                       column=max_screen_x / 2 - 2))

    #loop.create_task(fire(canvas, start_row=max_screen_y / 2, start_column=max_screen_x / 2))
    loop.run_forever()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
