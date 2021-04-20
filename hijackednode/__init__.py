#!/usr/bin/env python3
# coding: utf-8

# WARNING! SPAGHETTI AHEAD!

import discord

from discord.ext.commands import Bot
from .configuration import CONF0
from .talk import TalkBox

from fake_useragent import UserAgent
from random import choice, randint
from typing import List

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


# INIT
config = CONF0()
bot = Bot(command_prefix=config.CommandPrefix, case_insensitive=True)
talkbox = TalkBox(config)


# BOT COMMANDS
@commands.cooldown(1, 120, commands.BucketType.user)
@bot.command(pass_context=True, name='pull_new_messages', description='Pulls all new messages from discord servers not already on database')
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
@bot.command(pass_context=True, name='imgSearch', description='Search for images online and send the first match')
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

@commands.cooldown(1, 10, commands.BucketType.guild)
@bot.command(pass_context=True, name='last_file', description='Get last file from upload server.')
async def last_file(ctx: commands.Context):
    # TODO: DOCUMENT THIS FUNCTION AND MAKE IT ACTUALLY PORTABLE
    if os.name == "nt":
        await ctx.send("Windows bad, Linux good")  # Windows bad, linux good
    else:
        nginx_dir = os.path.join(os.sep + "var", "log", "nginx")
        await ctx.send("Last modification date: " + str(dt.datetime.utcfromtimestamp(os.path.getmtime(os.path.join(nginx_dir, "data.txt"))).strftime("%Y-%m-%d %H:%M:%S") + " by: " + open(os.path.join(nginx_dir, "lastime.infopog")).read()), file=discord.File(os.path.join(nginx_dir, "data.txt")))

@commands.cooldown(2, 30, commands.BucketType.guild)
@bot.command(pass_context=True, name='ping', description='Checks ping between bot and discord server')
async def ping(ctx: commands.Context, times: int = 1):
    async with ctx.typing():
        t, t_ms, t_msg = '', [], (await ctx.send(content='Pong'))

        await t_msg.edit(content="Pong.")

        for _ in range(min(6, max(int(times), 1))):
            t_ms.append(t_msg.edited_at() - (dt.datetime.now().timestamp() / 1000))
            t += '.'
            await t_msg.edit(content="Pong" + t)

        await t_msg.edit(content=("Pong! Took: " + str(round(number=(sum(t_ms) / len(t_ms)), ndigits=3)) + "ms."))

@bot.command(pass_context=True, name='punch', description='Hurts <someone> using <something>')
async def punch(ctx: commands.Context, someone: discord.Member, *using):
    async with ctx.typing():
        if (bot.user == someone):
            await ctx.send(f"I obliterate {ctx.author.mention}" + ((' using: ' + ' '.join(using)) if bool(using) else (choice(config.WeapList) + '.')))
        else:
            if bool(someone):
                if ((ctx.author.id in config.SUPERUSER) or (ctx.guild.id in config.DevLab)):
                    await ctx.send(f"I obliterate {someone.mention}" + ((' using: ' + ' '.join(using)) if bool(using) else (choice(config.WeapList) + '.')))
                else:
                    await ctx.send(f"I punch {someone.mention}"      + ((' using: ' + ' '.join(using)) if bool(using) else ('.')))

@bot.command(pass_context=True, name='say', description='>Title')
async def say(ctx: commands.Context, *words):
    async with ctx.typing():
        await ctx.send(" ".join(words))

@bot.command(pass_context=True, name='talk', description='Generates something from the texts on database')
async def talk(ctx: commands.Context, *base):
    async with ctx.channel.typing():
        if len(base) == 1:
            await ctx.channel.send(await talkbox.until_word(primer=base[0]))
        else:
            await ctx.channel.send(await talkbox.until_word(init=base))

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
    print("[" + str(dt.datetime.now().timestamp()) + " ]")
    print(str(bot.user) + " Connected to:")
    for guild in bot.guilds:
        if guild.id in config.GildExList:
            continue
        print()
        print(" - [" + str(guild.id) + "]: " + str(guild.name) + ".")

        print("\t- [Text  Channels]: " + str(guild.name) + ".")
        for channel in guild.text_channels:
            if channel.id in config.ChanExList: continue
            print("\t\t- [" + str(channel.id) + "]: " + str(channel.name) + ".")

        print("\t- [Voice Channels]: " + str(guild.name) + ".")
        for channel in guild.voice_channels:
            if channel.id in config.ChanExList: continue
            print("\t\t- [" + str(channel.id) + "]: " + str(channel.name) + ".")

    print()
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
    main()  # RUN!
