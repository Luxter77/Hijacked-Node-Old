#!/usr/bin/env python3
# coding: utf-8

# WARNING! SPAGHETTI AHEAD!

import discord

from discord.ext.commands import Bot
from .configuration import CONF0
from .talk import TalkBox

from fake_useragent import UserAgent
from random import choice, randint
from typing import List, Optional

from tqdm.asyncio import tqdm as asynctqdm

from discord.ext import commands
from shutil import rmtree
from copy import deepcopy
import datetime as dt
import traceback
import glob
import json
import sys
import io
import os
import re

from .image import bing_image


# INIT
config = CONF0()
bot = Bot(command_prefix=config.CommandPrefix, case_insensitive=True)
talkbox = TalkBox(config)


# DEV-LAB ONLY COMMANDS
# these are for debugging and such
@bot.command(pass_context=True, name='dump_chain', description="DEBUG-ONLY: dumps markov chain and dictionary to a file!")
async def dump_chain(ctx: commands.Context, chain: bool = True, dictionary: bool = True, all_words: bool = False, all_text: bool = False, single_file: bool = False):
    async with talkbox.TRANS_LOCK:
        chain_     = deepcopy(talkbox.chain)
        trans_map_ = deepcopy(talkbox.trans_map)
        all_words_ = deepcopy(talkbox.all_words)
        all_text_  = deepcopy(talkbox.all_text)

    if single_file:
        da_file, data = io.StringIO(), dict()

        if chain:      data['chain']     = chain_
        if dictionary: data['trans_map'] = trans_map_
        if all_words:  data['all_words'] = all_words_
        if all_text:   data['all_text']  = all_text_

        json.dump(data, da_file, indent=4, sort_keys=True)

        da_file.close()

    else:
        if chain:
            chain_file = io.StringIO()
            json.dump(chain_, chain_file, indent=4, sort_keys=True)
            await ctx.send("Chain file:", file=discord.File(chain_file, f"chain.{str(dt.datetime.now().timestamp())}.txt"))
            chain_file.close()

        if dictionary:
            dict_file = io.StringIO()
            json.dump(trans_map_, chain_file, indent=4, sort_keys=True)
            await ctx.send("Dictionary file:", file=discord.File(chain_file, f"dictionary.{str(dt.datetime.now().timestamp())}.txt"))
            dict_file.close()

        if all_words:
            all_words_file = io.StringIO()
            json.dump(all_words_, all_words_file, indent=4, sort_keys=True)
            await ctx.send("Dictionary file:", file=discord.File(all_words_file, f"words.{str(dt.datetime.now().timestamp())}.txt"))
            all_words_file.close()

        if all_text:
            all_text_file = io.StringIO()
            json.dump(all_text_, all_text_file, indent=4, sort_keys=True)
            await ctx.send("Dictionary file:", file=discord.File(all_text_file, f"text.{str(dt.datetime.now().timestamp())}.txt"))
            all_text_file.close()


# BOT COMMANDS
@commands.cooldown(1, 120, commands.BucketType.default)
@bot.command(pass_context=True, name='pull_new_messages', description='Pulls all new messages from discord servers not already on database')
async def pull_new_messages(ctx: commands.Context):
    if (talkbox.CORPUS_LOCK.locked()):
        await ctx.send("I'm occupied doing something else right about now...")
        return()

    msg: discord.Message = await ctx.send('On it.')

    try:
        async with talkbox.CORPUS_LOCK:
            try:
                messages_all = json.load(open(os.path.join(config.PATH, "DB", "parrot", "parrot.json")))
            except json.JSONDecodeError:
                messages_all = json.load(open(os.path.join(config.PATH, "DB", "parrot", "parrot.bkp.json")))
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
                    if message.type == discord.MessageType.default and not(message.author.id in config.UserExLixt) and not(message.author.bot):
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
        json.dump(messages_all, open(os.path.join(config.PATH, "DB", "parrot", "parrot.json"),     "w"), indent=4, sort_keys=True)
        json.dump(messages_all, open(os.path.join(config.PATH, "DB", "parrot", "parrot.bkp.json"), "w"), indent=4, sort_keys=True)

    await msg.edit(content='One last thing...')

    await talkbox.reload_dict()

    await msg.edit(content='Synchronization done.')

@commands.cooldown(2, 15, commands.BucketType.user)
@bot.command(pass_context=True, name='img', description='Search for images online and send the first match')
async def img(ctx: commands.Context, amount: Optional[int] = 1, *query):
    async with ctx.message.channel.typing():
        query = ' '.join(query)
        await bing_image(query, amount, config)
        for x in glob.glob(os.path.join(config.PATH, "DB", "img", "ext", query, "Scrapper_*")):
            await ctx.send(file=discord.File(x))
        rmtree(os.path.join(config.PATH, "DB", "img", "ext", query), ignore_errors=True, onerror=None)

@commands.cooldown(2, 30, commands.BucketType.guild)
@bot.command(pass_context=True, name='ping', description='Checks ping between bot and discord server')
async def ping(ctx: commands.Context, times: int = 1):
    async with ctx.typing():
        t, t_ms, t_msg = '', [], (await ctx.send(content='Pong'))
        t_msg: discord.Message

        await t_msg.edit(content="Pong.")

        for _ in range(min(6, max(int(times), 1))):
            t_ms.append(t_msg.edited_at.timestamp() - (dt.datetime.now().timestamp()))
            t += '.'
            await t_msg.edit(content="Pong" + t)

        await t_msg.edit(content=("Pong! Took: " + str(round(number=(sum(t_ms) / (len(t_ms) * 1000)), ndigits=3)) + "ms."))

@bot.command(pass_context=True, name='punch', description='Hurts [someone] using [something]')
async def punch(ctx: commands.Context, someone: discord.Member, *something):
    async with ctx.typing():
        if (bot.user == someone):
            await ctx.send(f"I obliterate {ctx.author.mention} using: " + ((' '.join(something)) if bool(something) else (choice(config.WeapList) + '.')))
        else:
            if bool(someone):
                if ((ctx.author.id in config.SUPERUSER) or (ctx.guild.id in config.DevLab)):
                    await ctx.send(f"I obliterate {someone.mention} using: " + ((' '.join(something)) if bool(something) else (choice(config.WeapList) + '.')))
                else:
                    await ctx.send(f"I punch {someone.mention}" + ((' using: ' + ' '.join(something)) if bool(something) else ('.')))

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
    print()
    print(f"Ignoring exception in command {context.command}:")
    traceback.print_exception(type(exception), exception, exception.__traceback__)

    print(f"[message]: {context.message.content}")

    if bool(args):
        print(f"[args]: {args.__repr__()}")
    if bool(kwargs):
        print(f"[kwargs]: {kwargs.__repr__()}")
    print()

@bot.event
async def on_error(event_method, *args: list, **kwargs: dict):
    print()
    print(f" Ignoring exception in {event_method}")
    traceback.print_exc()
    if args:
        print(f"[args]: {args.__repr__()}")
    if kwargs:
        print(f"[kwargs]: {kwargs.__repr__()}")
    print()

@bot.event
async def on_ready():
    print(f"I am: [{str(os.getpid())}][{str(dt.datetime.now().timestamp())}]")
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
    if sys.argv[1:]:
        ...
    main()  # RUN!
