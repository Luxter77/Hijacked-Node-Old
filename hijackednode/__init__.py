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
import datetime as dt
import traceback
import glob
import json
import sys
import os
import re

from .image import bing_image

# BOT COMMANDS
@commands.cooldown(1, 120, commands.BucketType.user)
@bot.command(pass_context=True)
async def pull_new_messages(ctx: commands.Context):
    if (talkbox.CORPUS_LOCK.locked()):
        await ctx.send("I'm occupied right about now.")
    else:
        msg: discord.Message = await ctx.send('On it.')

        try:
            async with talkbox.CORPUS_LOCK:
                try:
                    messages_all = json.load(open(os.path.join(config.PATH, "DB", "parrot.json")))
                except json.JSONDecodeError:
                    messages_all = json.load(open(os.path.join(config.PATH, "DB", "parrot.bkp.json")))
            last_time = dt.datetime.fromtimestamp(messages_all.pop('last_time'))
        except FileNotFoundError:
            messages_all = dict()  # starting from scratch
            last_time = None

        now = dt.datetime.now()

        messages_all['last_time'] = now.timestamp()

        for guild in bot.guilds:
            if guild.id in config.GildExList:
                continue
            for channel in guild.text_channels:
                if channel.id in config.ChanExList:
                    continue
                try:
                    async for message in asynctqdm(channel.history(limit=None, oldest_first=True, after=last_time, before=now), leave=False):
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

        await msg.edit(content='Just a sec...')

        async with talkbox.CORPUS_LOCK:
            json.dump(messages_all, open(os.path.join(config.PATH, "DB", "parrot.json"),     "w"), indent=4, sort_keys=True)
            json.dump(messages_all, open(os.path.join(config.PATH, "DB", "parrot.bkp.json"), "w"), indent=4, sort_keys=True)

        await msg.edit(content='One last thing...')

        await talkbox.reload_dict()

        await msg.edit(content='Synchronization done.')

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
async def last_file(ctx: commands.Context):
    if os.name == "nt":
        await ctx.send("Windows bad, Linux good")  # Windows bad, linux good
    else:
        await ctx.send("Last modification date: " + str(dt.datetime.utcfromtimestamp(os.path.getmtime(os.path.join("var", "log", "nginx", "data.txt"))).strftime("%Y-%m-%d %H:%M:%S") + " by: " + str(open(os.path.join("var", "log", "nginx", "lastime.infopog")).read())))
        await ctx.send(file=discord.File(os.path.join("var", "log", "nginx", "data.txt")))

@bot.command(pass_context=True)
async def ping(ctx: commands.Context):
    async with ctx.typing():
        t_msg = await ctx.send("Pong!")
        t_ms = str(round((t_msg.created_at.timestamp() - dt.datetime.now().timestamp()) / 1000))
        await t_msg.edit(content="Pong! Took: " + t_ms + "ms.")


@bot.command(pass_context=True)
async def punch(ctx: commands.Context, *args):
    async with ctx.typing():
        if ("node" in args[1:]) or bool(re.search(str(bot.user.id), "".join(args))):
            await ctx.send("Not gonna happen mate.")
        else:
            to = " ".join(args) if (len(args) > 0) else ctx.author.mention
            await ctx.send("I obliterate " + to + " using: " + choice(config.WeapList) if ((ctx.author.id in config.SUPERUSER) or (ctx.guild.id in config.DevLab)) else ("I punch: " + " ".join(args) + "."))

@bot.command(pass_context=True)
async def say(ctx: commands.Context, *args):
    async with ctx.typing():
        await ctx.send(" ".join(args))

@bot.command(pass_context=True)
async def talk(ctx: commands.Context, init: str = False):
    if bool(init):
        init = init.split(' ')
    async with ctx.channel.typing():
        await ctx.channel.send(await talkbox.until_word(init=init))

# BOT EVENTS
@bot.event
async def on_command_error(context: commands.Context, exception: Exception, *args: list, **kwargs: dict):
    print(file=sys.stderr)
    print(f"Ignoring exception in command {context.command}:", file=sys.stderr)
    traceback.print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    print(f"[message]: {context.message.content}", file=sys.stderr)

    if args:
        print(f"[args]: {args.__repr__()}", file=sys.stderr)
    if kwargs:
        print(f"[kwargs]: {kwargs.__repr__()}", file=sys.stderr)
    print(file=sys.stderr)

@bot.event
async def on_error(event_method, *args: list, **kwargs: dict):
    print(file=sys.stderr)
    print(f" Ignoring exception in {event_method}", file=sys.stderr)
    traceback.print_exc()
    if args:
        print(f"[args]: {args.__repr__()}", file=sys.stderr)
    if kwargs:
        print(f"[kwargs]: {kwargs.__repr__()}", file=sys.stderr)
    print(file=sys.stderr)


@bot.event
async def on_ready():
    print("[ " + str(dt.datetime.now().timestamp()) + " ]")
    print(str(bot.user) + " Connected to:")
    for guild in bot.guilds:
        print(" - [" + str(guild.id) + "]: " + str(guild.name) + ".")
    await bot.change_presence(activity=discord.Game(name="Waking up..."))
    await talkbox.reload_dict()
    await bot.change_presence(activity=discord.Game(name="Complex Numbers"))

@bot.event
async def on_message(message: discord.Message):
    for emote in config.EmoteNest:
        for diff in emote[0]:
            for reply in emote[1]:
                if bool(re.search(diff, message.content.lower())):
                    await message.add_reaction(reply)
    if message.author != bot.user:
        await bot.process_commands(message)
        cont = message.content.lower()
        if (not (cont.startswith("--")) and not (cont.startswith("/")) and not (cont.startswith("!")) and not (cont.startswith("$")) and bool(re.search("node", cont))):
            await talk(message)

def main():
    bot.run(config.TOKEN)

if __name__ == '__main__':
    main()
