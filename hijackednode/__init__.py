#!/usr/bin/env python3
# coding: utf-8

# WARNING! SPAGHETTI AHEAD!

import discord

from discord.ext.commands import Bot
from .configuration import CONF0
from .talk import TalkBox

config = CONF0()
bot = Bot(command_prefix=config.CommandPrefix, case_insensitive=True)
talkbox = TalkBox(config)

from random import choice, randint
from fake_useragent import UserAgent

from tqdm.asyncio import tqdm as asynctqdm

from discord.ext import commands
from tqdm.auto import tqdm
import datetime as dt
import glob
import json
import os
import re

from .image import bing_image

async def pull_new_messages(last_time: dt.datetime = None):
    with talkbox.CORPUS_LOCK:
        messages_all = dict()
        try:
            with open(os.path.join(config.PATH, "DB", "parrot.json"), "rb") as parrot:
                messages_all = json.load(parrot)
            last_time = dt.datetime.fromtimestamp(messages_all.pop('last_time'))
        except json.JSONDecodeError:
            with open(os.path.join(config.PATH, "DB", "parrot.bkp.json"), "rb") as parrot:
                messages_all = json.load(parrot)
            last_time = dt.datetime.fromtimestamp(messages_all.pop('last_time'))
        except FileNotFoundError:
            pass  # starting from scratch

        for guild in tqdm(bot.guilds):
            if guild.id in config.GildExList:
                continue
            messages_all[str(guild.id)] = dict()
            for channel in tqdm(guild.text_channels):
                if channel.id in config.ChanExList:
                    continue
                try:
                    async for message in asynctqdm(channel.history(limit=None, oldest_first=True, after=last_time)):
                        if message.type == discord.MessageType.default and not (message.author.id in config.UserExLixt):
                            try:
                                messages_all[str(guild.id)][str(channel.id)].append(message.content)
                            except Exception:
                                try:
                                    messages_all[str(guild.id)][str(channel.id)] = [message.content]
                                except Exception:
                                    messages_all[str(guild.id)] = {str(channel.id): [message.content]}
                except Exception:
                    pass  # This usually means that we cant read that channel; oh well, just pass

        messages_all['last_time'] = dt.datetime.now().timestamp()

        with open(os.path.join(config.PATH, "DB", "parrot.json"), "rb") as parrot:
            json.dump(messages_all, parrot)
        with open(os.path.join(config.PATH, "DB", "parrot.bkp.json"), "rb") as parrot:
            json.dump(messages_all, parrot)

# BOT COMMANDS

@commands.cooldown(2, 15, commands.BucketType.user)
@bot.command(pass_context=True)
async def imgSearch(ctx: commands.Context, *args):
    async with ctx.message.channel.typing():
        if len(args) == 0:
            q, n = "Cursed Image Meme", 1
        elif len(args) == 1:
            q, n = "".join(args), 1
        else:
            # OH GOD THIS IS PAINFUL
            try:
                n, is_first = int(args[0]), True
            except Exception:
                is_first = False

            try:
                n, is_last = (int(args[-1]), True) if not (is_first) else (1, False)
            except Exception:
                is_last = False

            if not(is_last) and not(is_first):
                n, q = 1, str(" ".join(args))
            else:
                q = str(" ".join(args[:-1])) if (is_last) else str(" ".join(args[1:]))

        await bing_image(q, n, config)

        for x in glob.glob(os.path.join(config.PATH, "DB", "img", "ext", q, "Scrapper_*")):
            await ctx.send(file=discord.File(x))
            os.remove(str(x))
            os.rmdir(os.path.join(config.PATH, "DB", "img", "ext", q))


# Discord Comm
@bot.command(pass_context=True)
async def last_file(ctx):
    if os.name == "nt":
        await ctx.send("Windows bad, Linux good")  # Windows bad, linux good
    else:
        await ctx.send("Last modification date: " + str(dt.datetime.utcfromtimestamp(os.path.getmtime(os.path.join("var", "log", "nginx", "data.txt"))).strftime("%Y-%m-%d %H:%M:%S") + " by: " + str(open(os.path.join("var", "log", "nginx", "lastime.infopog")).read())))
        await ctx.send(file=discord.File(os.path.join("var", "log", "nginx", "data.txt")))

@bot.command(pass_context=True)
async def ping(ctx):
    async with ctx.typing():
        t_msg = await ctx.send("Pong!")
        t_ms = str(
            round((t_msg.created_at.timestamp() - dt.datetime.now().timestamp()) / 1000)
        )
        await t_msg.edit(content="Pong! Took: " + t_ms + "ms.")


@bot.command(pass_context=True)
async def punch(ctx, *args):
    async with ctx.typing():
        if ("node" in args[1:]) or bool(re.search(str(bot.user.id), "".join(args))):
            await ctx.send("Not gonna happen mate.")
        else:
            to = " ".join(args) if (len(args) > 0) else ctx.author.mention
            await ctx.send("I obliterate " + to + " using: " + choice(config.WeapList) if ((ctx.author.id in config.SUPERUSER) or (ctx.guild.id in config.DevLab)) else ("I punch: " + " ".join(args) + "."))

@bot.command(pass_context=True)
async def say(ctx, *args):
    async with ctx.typing():
        await ctx.send(" ".join(args))

@bot.command(pass_context=True)
async def talk(message, line_len: commands.Greedy[int] = None, init: str = False):
    if bool(init):
        init = init.split(' ')
    async with message.channel.typing():
        await message.channel.send(await talkbox.until_word(until=line_len, init=init))

@bot.event
async def on_ready():
    await talkbox.reload_dict()

def main():
    bot.run(config.TOKEN)

if __name__ == '__main__':
    main()
