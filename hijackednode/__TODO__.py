import datetime as dt
import discord
import asyncio
import re
import os

from hijackednode.configuration import CONF0


# I stole this for someone's™ gitist
async def wednesday(config: CONF0, bot: discord.ext.commands.Bot):
    while True:
        today, today_img = config.DailyDict[dt.datetime.today.weekday()]
        if today:
            for chan in config.DailyChan:
                async with bot.get_channel(chan).typing():
                    await bot.get_channel(chan).send(file=discord.File(today_img))
        hours = 60 * 60
        async def bg():
            while True:
                await asyncio.sleep(12 * hours)
        task = asyncio.create_task(bg())
        try:
            await asyncio.sleep(arg)
        finally:
            task.cancel()
