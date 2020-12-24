from .image import bing_image
import asyncio
import datetime as dt
import glob
import os
import pickle
import re
import subprocess
import traceback
import sys
import unicodedata

import discord
import numpy as np
from discord import Game, Message
from discord.ext import commands
from discord.ext.commands import Bot, Context
from emoji import UNICODE_EMOJI
from tqdm.asyncio import tqdm as asynctqdm
from tqdm.auto import tqdm

from .talk import talkbox, TalkBox
from .configuration import CONF0
from .daily import wednesday
from .logger import LogMe

config = CONF0()
bot = Bot(command_prefix=config.CommandPrefix, case_insensitive=True)
logMe = LogMe(config=config, bot=bot)


@commands.cooldown(2, 15, commands.BucketType.user)
@bot.command(pass_context=True)
async def imgSearch(ctx: Context, *args):
    async with ctx.message.channel.typing():
        if len(args) == 0:
            q = "Cursed Image Meme"
            n = 1
        elif len(args) == 1:
            q = "".join(args)
            n = 1
        else:
            # OH GOD THIS IS PAINFUL
            isFirts, isLast = None, None
            try:
                n, isFirts = int(args[0]), True
            except Exception:
                isFirts = False
            try:
                n, isLast = (
                    int(args[-1]), True) if not (isFirts) else (1, False)
            except Exception:
                isLast = False
            if not (isLast) and not (isFirts):
                n, q = 1, str(" ".join(args))
            else:
                q = str(" ".join(args[:-1])
                        ) if (isLast) else str(" ".join(args[1:]))
        await bing_image(q, n, config)
        for x in glob.glob(
            os.path.join(config.PATH, "DB", "img", "ext", q, "Scrapper_*")
        ):
            try:
                await ctx.send(file=discord.File(x))
            except Exception:
                await logMe(
                    "Can't send [  " + str(x)
                    + "  ]! from [" + str(ctx.message.id)
                    + "]:```" + str(ctx.message.content)
                    + "```",
                    True,
                )
            try:
                os.remove(str(x))
            except Exception:
                await logMe("Could'n delete [ " + str(x) + "]", True)
        try:
            os.rmdir(os.path.join(config.PATH, "DB", "img", "ext", q))
        except Exception as e:
            await logMe(e, True)


# Discord Comm
@bot.command(pass_context=True)
async def getLastFrom(ctx: Context):
    if os.name == "nt":
        await logMe("Windows bad, linux good")  # Windows bad, linux good
    else:
        try:
            await ctx.send(
                "Last modification date: "
                + str(
                    dt.datetime.utcfromtimestamp(
                        os.path.getmtime(os.path.join(
                            "var", "log", "nginx", "data.txt"))
                    ).strftime("%Y-%m-%d %H:%M:%S")
                    + " by: "
                    + str(
                        open(os.path.join("var", "log",
                                          "nginx", "lastime.infopog")).read()
                    )
                )
            )
            await ctx.send(
                file=discord.File(os.path.join(
                    "var", "log", "nginx", "data.txt"))
            )
        except FileNotFoundError:
            await ctx.send('No new file!')


@bot.command(pass_context=True, hidden=True)
async def Tree(ctx: Context):
    if config.DevLab:
        if (ctx.guild == config.DevLab[0]) or (ctx.author.id in config.SUPERUSER):
            line = str(
                subprocess.check_output(
                    ["tree"] + [] + [config.PATH], stderr=subprocess.STDOUT
                )
                .decode(sys.stdout.encoding)
                .strip()
            )
            for x in [line[i:i + 1994] for i in range(0, len(line), 1994)]:
                await ctx.send("```" + x + "```")
        else:
            await ctx.send("Noy You, Not here, Not now.")


@bot.command(pass_context=True)
async def ReSyncDict(ctx: Context):
    global talkbox
    await talkbox.pull_messages()


@bot.command(pass_context=True)
async def rebuildDict(ctx: Context):
    global talkbox
    await talkbox.rebuild_dictionary()


@bot.command(pass_context=True)
async def reloadDict(ctx: Context):
    global talkbox
    await talkbox.build_chain()


@bot.command(pass_context=True)
async def ping(ctx: Context):
    async with ctx.typing():
        t_msg = await ctx.send("Pong!")
        t_ms = str(
            round((t_msg.created_at.timestamp() -
                   dt.datetime.now().timestamp()) / 1000)
        )
        await t_msg.edit(content="Pong! Took: " + t_ms + "ms.")


@bot.command(pass_context=True)
async def punch(ctx: Context, *args):
    async with ctx.typing():
        ewap = (
            True
            if ((ctx.author.id in config.SUPERUSER) or (ctx.guild.id in config.DevLab))
            else False
        )
        if bool(
            re.search("node", "".join(args))
            or bool(re.search(str(bot.user.id), "".join(args)))
        ):
            await ctx.send("Not gonna happen mate.")
            return ()
        to = " ".join(args) if (len(args) > 0) else ctx.author.mention
        await ctx.send(
            "I obliterate " + to + " using: " +
            np.random.choice(config.WeapList)
            if (ewap)
            else ("I punch: " + " ".join(args) + ".")
        )


@bot.command(pass_context=True)
async def say(ctx: Context, *args):
    async with ctx.typing():
        await ctx.send(" ".join(args))
        await logMe(
            "`` "
            + str(ctx.author.mention)
            + " ``: ```"
            + str(ctx.message.content)
            + "```"
        )
        if ctx.author in config.SUPERUSER:
            await ctx.message.delete()


@bot.command(pass_context=True)
async def talk(message: Message, llen: commands.Greedy[int] = None, *, init: str = None):
    async with message.channel.typing():
        
        sms = await talkbox.gen_text(llen=llen, init=init)
        if(sms):
            await message.channel.send(sms)
        else:
            msg = await message.channel.send('I am kind of bussy right now, please wait \'til I finish with this')
            asyncio.sleep(3)
            msg.delete()


@bot.event
async def on_command_error(context: Context, exception: Exception):
    print("|--------------- ERR_ START ----------------|")
    print("Ignoring exception in command {}:".format(
        context.command), file=sys.stderr)
    traceback.print_exception(type(exception), exception,
                              exception.__traceback__,
                              file=sys.stderr)
    print("|---------------- ERR_ END -----------------|")
    try:
        await logMe(context.message.content)
    except Exception:
        await logMe(exception, True)


@bot.event
async def on_error(event_method, *args, **kwargs):
    try:
        await logMe(" ``` " + str(event_method) + " ``` ", True)
        await logMe(" ``` " + traceback.format_exc() + " ``` ", True)
    except Exception:
        print("|--------------- ERR_ START ----------------|")
        print(" Ignoring exception in {}".format(event_method),
              file=sys.stderr)
        traceback.print_exc()
        print("|----------------- ERR_ END -----------------|")

@bot.event
async def on_message(message: Message):
    for emote in config.EmoteNest:
        for diff in emote[0]:
            for reply in emote[1]:
                if bool(re.search(diff, message.content.lower())):
                    await message.add_reaction(reply)
    if message.author != bot.user:
        await bot.process_commands(message)
        cont = message.content.lower()
        await talk(message, True) if (
            not (cont.startswith("--"))
            and not (cont.startswith("/"))
            and not (cont.startswith("!"))
            and not (cont.startswith("$"))
            and bool(re.search("node", cont))
        ) else None


@bot.event
async def on_ready():
    # logMe.prime()
    await logMe("|---------------doBootUp-st-----------------|")
    await logMe("|Not really an error, but rather an exploit.|", True)
    await logMe("|-------------------------------------------|")
    await bot.change_presence(activity=Game(name="Waking Up..."))
    await logMe("[ " + str(dt.datetime.now().timestamp()) + " ]")
    await logMe(str(bot.user) + " Is connected to:")
    await logMe("|-------------------------------------------|")
    for guild in bot.guilds:
        await logMe(" - [" + str(guild.id) + "]: " + str(guild.name) + ".")
    await logMe("|-------------------------------------------|")
    await logMe("|         Bootup Sequence complete          |")
    await bot.change_presence(activity=Game(name="Complex Numbers"))
    global talkbox  # EX DEE
    talkbox = TalkBox(config=config, bot=bot, logMe=logMe)
    # asyncio.create_task(wednesday(config=config, bot=bot))
    asyncio.create_task(talkbox.pull_messages())
    await logMe("|-------------- doBootUp End ---------------|")

def main(cla = {}):
    bot.run(config.TOKEN)

if __name__=='__main__':
    main()
