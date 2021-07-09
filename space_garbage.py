import asyncio
import os
from curses_tools import draw_frame


def get_garbage_frames():
    garbage_frames = []
    filesnames = os.listdir("./space_garbage")
    for filename in filesnames:
        path = os.path.join("./space_garbage", filename)
        with open(path, "r") as file:
            garbage_frames.append(file.read())
    return garbage_frames


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
