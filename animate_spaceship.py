import asyncio
from itertools import cycle
from tools import sleep
from curses_tools import draw_frame, get_frame_size, read_controls
from physics import update_speed
from fire import fire



async def animate_spaceship(canvas, row, column):
    with open("./rocket_frames/rocket_frame_1.txt", "r") as f:
        frame_1 = f.read()
    with open("./rocket_frames/rocket_frame_2.txt", "r") as f:
        frame_2 = f.read()

    row_speed = column_speed = 0


    frame_rows, frame_columns = get_frame_size(frame_1)
    max_row, max_column = canvas.getmaxyx()
    frames = [frame_1, frame_1, frame_2, frame_2]

    for frame in cycle(frames):
        rows_direction, columns_direction, space_pressed = read_controls(
            canvas)

        row_speed, column_speed = update_speed(
            row_speed, column_speed, rows_direction, columns_direction
        )

        if row + row_speed + frame_rows < max_row and -1 \
                < row + row_speed:
            row += row_speed
        if column + column_speed + frame_columns < max_column and 0 \
                < column + column_speed:
            column += column_speed * 3

        draw_frame(canvas, row, column, frame)
        await sleep()

        draw_frame(canvas, row, column, frame, negative=True)
        canvas.refresh()

