import asyncio
import curses
import random
from tools import sleep


async def blink(canvas, row, column, symbol):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(random.randint(1, 20))
        canvas.border()
        canvas.refresh()

        canvas.addstr(row, column, symbol)
        await sleep(random.randint(1, 10))
        canvas.refresh()

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(random.randint(1, 10))
        canvas.refresh()

        canvas.addstr(row, column, symbol)
        await sleep(random.randint(1, 3))
        canvas.refresh()
