import asyncio
import time
import curses
import random
from itertools import cycle

from curses_tools import draw_frame, read_controls, get_frame_size
from animate_spaceship import get_rocket_frames
from space_garbage import get_garbage_frames, fly_garbage
from physics import update_speed
from fire import fire
from tools import sleep

TIC_TIMEOUT = 0.1
SCREEN_WIDE, SCREEN_HEIGHT = 0, 0
COROUTINES = []
STAR = '*+:.'


async def blink(canvas, row, column, symbol):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(random.randint(1, 21))

        canvas.addstr(row, column, symbol)
        await sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(5)

        canvas.addstr(row, column, symbol)
        await sleep(3)


async def control_spaceship(canvas, rocket_frames, row, column):
    rocket_height, rocket_wide = get_frame_size(rocket_frames[0])
    rocket_frames = cycle(rocket_frames)
    row_speed = column_speed = 0

    while True:
        rocket_frame = next(rocket_frames)
        rows_direction, columns_direction, space_pressed = read_controls(
            canvas)
        if space_pressed:
            COROUTINES.append(fire(canvas, row - 1, column + rocket_wide // 2))
        row_speed, column_speed = update_speed(row_speed, column_speed,
                                               rows_direction,
                                               columns_direction)
        row += row_speed
        column += column_speed

        if column <= 1 or column >= SCREEN_WIDE - rocket_wide:
            column -= column_speed
        if row <= 1 or row >= SCREEN_HEIGHT - rocket_height:
            row -= row_speed
        draw_rocket(canvas, rocket_frame, row, column)
        await asyncio.sleep(0)


async def fill_orbit_with_garbage(canvas, garbage_frames):
    while True:
        COROUTINES.append(
            fly_garbage(canvas, random.randint(1, SCREEN_WIDE - 1),
                        random.choice(garbage_frames)))
        await sleep(15)


def draw_rocket(canvas, rocket_frame, row, column):
    draw_frame(canvas, row, column, rocket_frame)
    canvas.refresh()
    draw_frame(canvas, row, column, rocket_frame, negative=True)


def draw(canvas):
    rocket_frames = get_rocket_frames()
    garbage_frames = get_garbage_frames()

    for column in range(100):
        star_row = random.randint(1, SCREEN_HEIGHT - 1)
        star_column = random.randint(1, SCREEN_WIDE - 1)
        star_type = random.choice(STAR)
        COROUTINES.append(blink(canvas, star_row, star_column, star_type))
    COROUTINES.extend([
        fill_orbit_with_garbage(canvas, garbage_frames),
        control_spaceship(canvas, rocket_frames, SCREEN_HEIGHT // 2,
                          SCREEN_WIDE // 2)
    ])

    canvas.nodelay(True)
    while True:
        for coroutine in COROUTINES.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                COROUTINES.remove(coroutine)
            if len(COROUTINES) == 0:
                break

        time.sleep(TIC_TIMEOUT)


if __name__ == '__main__':
    screen = curses.initscr()
    curses.curs_set(False)
    curses.update_lines_cols()
    SCREEN_HEIGHT, SCREEN_WIDE = screen.getmaxyx()
    curses.wrapper(draw)
