import asyncio
from itertools import cycle

from curses_tools import draw_frame, get_frame_size, read_controls


async def animate_spaceship(canvas, row, column):
    with open("./rocket_frames/rocket_frame_1.txt", "r") as f:
        frame_1 = f.read()
    with open("./rocket_frames/rocket_frame_2.txt", "r") as f:
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
