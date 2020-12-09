from emoji import UNICODE_EMOJI
import datetime as dt
import numpy as np
import unicodedata
import subprocess
import discord
import pickle
import glob
import sys
import os
import re

from tqdm.asyncio import tqdm as asynctqdm
from discord.ext import commands
from tqdm.auto import tqdm

from ... import bot, config, logMe
from ...image import bing_image

@commands.cooldown(2, 15, commands.BucketType.user)
@bot.command(pass_context=True)
async def imgSearch(ctx: commands.Context, *args):
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
                n, isLast = (int(args[-1]), True) if not (isFirts) else (1, False)
            except Exception:
                isLast = False
            if not (isLast) and not (isFirts):
                n, q = 1, str(" ".join(args))
            else:
                q = str(" ".join(args[:-1])) if (isLast) else str(" ".join(args[1:]))
        await bing_image(q, n)
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
async def getLastFrom(ctx):
    if os.name == "nt":
        await logMe("Windows bad, linux good")  # Windows bad, linux good
    else:
        await ctx.send(
            "Last modification date: "
            + str(
                dt.datetime.utcfromtimestamp(
                    os.path.getmtime(os.path.join("var", "log", "nginx", "data.txt"))
                ).strftime("%Y-%m-%d %H:%M:%S")
                + " by: "
                + str(
                    open(os.path.join("var", "log", "nginx", "lastime.infopog")).read()
                )
            )
        )
        await ctx.send(
            file=discord.File(os.path.join("var", "log", "nginx", "data.txt"))
        )


@bot.command(pass_context=True, hidden=True)
async def Tree(ctx):
    if config.DevLab:
        if (ctx.guild == config.DevLab[0]) or (ctx.author.id in config.SUPERUSER):
            line = str(
                subprocess.check_output(
                    ["tree"] + [] + [config.PATH], stderr=subprocess.STDOUT
                )
                .decode(sys.stdout.encoding)
                .strip()
            )
            for x in [line[i: i + 1994] for i in range(0, len(line), 1994)]:
                await ctx.send("```" + x + "```")
        else:
            await ctx.send("Noy You, Not here, Not now.")


@bot.command(pass_context=True)
async def ReSyncDict(ctx=None, fox=True):
    global IsSyncEd
    if IsSyncEd or not (fox):
        try:
            IsSyncEd = False
            await logMe("Updating message database!")
            msg = (
                await ctx.send("Downloading new messages from Discord server...")
                if (fox)
                else None
            )

            def PPATH(noww):
                return str(
                    os.path.join(
                        config.PATH, "DB", "parrot." + str(noww.timestamp()) + ".pkl"
                    )
                )

            async def lastTimeR():
                try:
                    with open(
                        os.path.join(config.PATH, "DB", "lasttime.pkl"), "rb"
                    ) as lasttimme:
                        return pickle.load(lasttimme)
                except Exception:
                    await bot.change_presence(
                        activity=discord.Game(name="Initializing database...")
                    )
                    return None

            def lastTimeW(noww):
                with open(
                    os.path.join(config.PATH, "DB", "lasttime.pkl"), "wb"
                ) as lasttimme:
                    pickle.dump(noww, lasttimme)

            await bot.change_presence(
                activity=discord.Game(name="Updating database...")
            )
            noww = dt.datetime.now()
            messages_all = []
            for guild in tqdm(bot.guilds):
                if guild.id in config.GildExList:
                    pass
                await logMe(
                    "Now processing: " + str(guild.name) + " (" + str(guild.id) + ")",
                    False,
                    False,
                )
                for channel in tqdm(guild.text_channels):
                    if channel.id in config.ChanExList:
                        pass
                    try:
                        await logMe(
                            " - Now Processing: "
                            + str(channel.name)
                            + " ("
                            + str(channel.id)
                            + ")",
                            False,
                            False,
                        )
                        async for message in asynctqdm(
                            channel.history(
                                limit=None, oldest_first=True, after=await lastTimeR()
                            )
                        ):
                            if message.type == discord.MessageType.default and not (
                                message.author.id in config.UserExLixt
                            ):
                                messages_all.append(message.content)
                    except Exception as err_:
                        await logMe(
                            "For some reason I can't access ["
                            + str(channel.id)
                            + "]("
                            + str(channel.name)
                            + ") in ["
                            + str(guild.id)
                            + "]("
                            + str(guild.name)
                            + ")",
                            True,
                            False,
                        )
                        await logMe(err_, True, False)
            with open(PPATH(noww), "wb") as parrot_pkl:
                pickle.dump(messages_all, parrot_pkl)
            lastTimeW(noww)
            await msg.edit(content="Files dumped to disk!") if (fox) else None
            IsSyncEd = True
            await rebuildDict(ctx, fox=fox)
            IsSyncEd = True
        except Exception as err_:
            IsSyncEd = True
            raise err_
        finally:
            IsSyncEd = True
    else:
        ctx.send("The syncronization job is already running!")


@bot.command(pass_context=True)
async def rebuildDict(ctx, fox=True):
    ...

@bot.command(pass_context=True)
async def reloadDict(ctx, override=False, fox=True):
    async def _reloadDict(ctx, override=False, fox=True):
        await bot.change_presence(
            activity=discord.Game(name="Loading new dictionary files...")
        )
        msg = await ctx.send("Reloading dictionary files...") if (fox) else None
        await logMe("Reloading Dictionary files")
        global W_DLOCK, W_DB, wdict, Dictnry, corporae
        W_DLOCK = False
        wdict = pickle.load(open(CORPUS_TXT_PATH + ".pkl", "rb"))
        Dictnry = {v: k for k, v in wdict.items()}
        W_DB, corporae = await DefPoint()
        W_DLOCK = True
        await msg.edit(content="Dictionaries reloaded!") if (fox) else None

    if fox:
        async with ctx.typing():
            await _reloadDict(ctx, override, fox)
    else:
        await _reloadDict(ctx, override, fox)
    await bot.change_presence(activity=discord.Game(name="Complex Numbers"))


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
            "I obliterate " + to + " using: " + np.random.choice(config.WeapList)
            if (ewap)
            else ("I punch: " + " ".join(args) + ".")
        )


@bot.command(pass_context=True)
async def say(ctx, *args):
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
async def talk(message, llen: commands.Greedy[int] = None, *, init: str = None):
    async with message.channel.typing():
        global W_DB, corporae, Dictnry
        sms = (
            " ".join(
                Dictnry[str(word)] for word in UntilPoint(W_DB, corporae, llen, init)
            )
            .replace(" ;", ";")
            .replace(" :", ":")
            .replace(" .", ".")
            .replace(" ,", ",")
        )
        sms = " ".join(str(await transsBack(sms, True)).split())

        def repl_fun(match):
            return str(np.random.randint(0, 9))

        sms = re.sub("⣿", repl_fun, sms).replace(" i ", " Yo ")
        if sms.startswith("i "):
            sms = re.sub("^i ", "yo ", sms, flags=re.M)
        sms = sms.lower().capitalize()
        print(sms)
        if W_DLOCK:
            await message.channel.send(sms)
