import asyncio
import os
import random

from curses_tools import draw_frame


def get_trash_frames():
    frames = []
    filesnames = os.listdir("./space_garbage")
    for filename in filesnames:
        path = os.path.join("./space_garbage", filename)
        with open(path, "r") as file:
            frames.append(file.read())
    return frames


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas, columns):
    frames = get_trash_frames()
    while True:
        for i in range(random.randint(1, 50)):
            await asyncio.sleep(0)
        await fly_garbage(canvas, column=random.randint(1, columns - 20),
                          garbage_frame=random.choice(frames))
