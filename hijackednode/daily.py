import datetime as dt
import numpy as np
import traceback
import discord
import asyncio
import sys
import re
import os

from . import useful
from .configuration import CONF0


# I stole this for someone's™ gitist
async def bg():
    while True: await asyncio.sleep(12 * 60 * 60)

async def long_sleep(arg):
    task = asyncio.create_task(bg())
    try:
        await asyncio.sleep(arg)
    finally:
        task.cancel()


async def wednesday(config: CONF0, bot: discord.ext.commands.Bot):
    while True:
        day = config.DailyDict[dt.datetime.today().strftime("%A")[:2]]
        if day['enabled']:
            for chan in (await useful.parse_channel_container(config.DailyChan, bot=bot)):
                async with chan.typing():
                    await chan.send(content=day['msg'], file=discord.File(day['fle']))
        await long_sleep(60 * 60 * 24)
