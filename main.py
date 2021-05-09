import asyncio
import curses
import random
import time
from itertools import cycle

from curses_tools import draw_frame, get_frame_size, read_controls

STARS = ["+", "*", ".", ":"]
TIC_TIMEOUT = 0.1


async def fire(canvas, start_row, start_column, rows_speed=-0.3,
               columns_speed=0):
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def animate_spaceship(canvas, row, column):
    with open("./rocket_frame_1.txt", "r") as f:
        frame_1 = f.read()
    with open("./rocket_frame_2.txt", "r") as f:
        frame_2 = f.read()

    frame_rows, frame_columns = get_frame_size(frame_1)
    max_row, max_column = canvas.getmaxyx()
    frames = [frame_1, frame_1, frame_2, frame_2]
    for frame in cycle(frames):
        rows_direction, columns_direction, space_pressed = read_controls(
            canvas)

        if row + rows_direction + frame_rows < max_row and -1 \
                < row + rows_direction:
            row += rows_direction
        if column + columns_direction + frame_columns < max_column and 0 \
                < column + columns_direction:
            column += columns_direction

        draw_frame(canvas, row, column, frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, frame, negative=True)
        canvas.refresh()


async def blink(canvas, row, column, symbol):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for _ in range(20):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(random.randint(0, 10)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(random.randint(0, 10)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for _ in range(3):
            await asyncio.sleep(0)


def draw(canvas):
    canvas.nodelay(True)
    max_screen_y, max_screen_x = canvas.getmaxyx()
    columns_stars = [x for x in range(1, max_screen_x - 1)]
    rows_start = [y for y in range(1, max_screen_y - 1)]
    curses.curs_set(False)

    coroutines = [
        blink(canvas, random.choice(rows_start), random.choice(columns_stars),
              random.choice(STARS)) for j in range(100)]

    shot = fire(canvas, start_row=max_screen_y / 2,
                start_column=max_screen_x / 2)
    coroutines.append(shot)

    space_ship = animate_spaceship(canvas, row=max_screen_y / 2,
                                   column=max_screen_x / 2 - 2)
    coroutines.append(space_ship)

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
