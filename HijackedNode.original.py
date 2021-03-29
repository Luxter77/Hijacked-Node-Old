#!/usr/bin/env python3
# coding: utf-8

# something something importing ssl multiple times
from gevent import monkey as curious_george

curious_george.patch_all(thread=False, select=False)
import grequests

from fake_useragent import UserAgent
import urllib.parse as urlparse
from bs4 import BeautifulSoup

from discord.channel import TextChannel
from discord.ext.commands import Bot
from discord import User

from tqdm.asyncio import tqdm as asynctqdm
from discord.ext import commands
from emoji import UNICODE_EMOJI
from tqdm.auto import tqdm
from pathlib import Path
import datetime as dt
import numpy as np
import unicodedata
import glob
import os
import subprocess
import sys
import re
import traceback
import json
import discord
import shutil
import asyncio
import typing
import pickle


class LogMe:
    """This is a  complicated logger I came up with.\n
    Feel free to insult me wilst readding it."""

    _std = {
        "LS": "|-----------------Log_ START-------------------|",
        "ES": "|-----------------ERR_ START-------------------|",
        "EE": "|------------------ERR_ END--------------------|",
        "LE": "|------------------Log_ END--------------------|",
        "!?": "Some unprinteable error happened...",
        "!!": "Ah for fucks sake something went horribly grong!",
    }

    def __init__(self, bot: Bot, config: CONF0):
        self.LogAdmin = set([bot.get_user(Admin) for Admin in config.LogAdmin])
        self.LogChan = set([bot.get_channel(Chan) for Chan in config.LogChan])

    async def __call__(self, st, err_: bool = False, tq: bool = True):
        if err_:
            print(self._std["ES"]) if (tq) else tqdm.write(self._std["ES"])
            print(st) if (tq) else tqdm.write(st)
            try:
                with self.bot.get_channel(self.LogChan) as Chan:
                    await Chan.send()
                    if self.LogAdmin:
                        await Chan.send(
                            " ".join([str(admin.mention) for admin in self.LogAdmin])
                        )
                    await Chan.send(st)
                    await Chan.send(self._std["EE"])
            except Exception:
                try:
                    with self.bot.get_channel(self.debug) as Chan:
                        await Chan.send(self._std["ES"])
                        try:
                            if self.LogAdmin:
                                await Chan.send(
                                    " ".join(
                                        [str(admin.mention) for admin in self.LogAdmin]
                                    )
                                )
                            await Chan.send(str(st))
                        except Exception:
                            if self.LogAdmin:
                                await Chan.send(
                                    " ".join(
                                        [str(admin.mention) for admin in self.LogAdmin]
                                    )
                                )
                            await Chan.send("Some unprinteable error happened...")
                        await Chan.send(self._std["EE"])
                except Exception:
                    _std = "Ah for hugs sake something went horribly grong! AGAIN"
                    print(_std) if (tq) else tqdm.write(_std)
            print(self._std["EE"]) if (tq) else tqdm.write(self._std["EE"])
        else:
            print(st) if (tq) else tqdm.write(st)
            try:
                with self.bot.get_channel(self.debug) as Chan:
                    await Chan.send(st)
            except Exception:
                try:
                    with self.bot.get_channel(self.debug) as Chan:
                        try:
                            try:
                                await Chan.send(st)
                            except Exception:
                                await Chan.send(str(type(st)))
                                await Chan.send(str(st))
                        except Exception:
                            await Chan.send(self._std["!?"])
                except Exception:
                    await Chan.send(self._std["LS"])
                    await self(self._std["!!"], True)
                    await Chan.send(self._std["LE"])

    def add_LogChan(self, Chan: TextChannel) -> None:
        self.LogChan.add(Chan)

    def del_LogChan(self, Chan: TextChannel) -> None:
        self.LogChan.remove(Chan)

    def add_LogAdmin(self, Admin: User) -> None:
        self.LogAdmin.add(Admin)

    def del_LogAdmin(self, Admin: User) -> None:
        self.LogAdmin.remove(Admin)


from base64 import standard_b64decode as de64
from discord import discord_Emoji
import random

# spoilers, its not funny
from hijackednode.funny import Pain

# Why do I keep doing this to myself
def saveConfig():
    try:
        pickle.dump(
            (
                CommandPrefix,
                TOKEN,
                PATH,
                DevLab,
                LogChan,
                LogAdmin,
                WeapList,
                SUPERUSER,
                UserExLixt,
                ChanExList,
                AllowEmoji,
                GildExList,
                WordExList,
                WordBanLst,
                DayList,
                DayChan,
                EmoteNest,
                StephLog,
            ),
            open("Config.pkl", "wb"),
        )
    except Exception:
        IAmIn = Pain(BaseException)  # Hug you Loop


def _get_def_doc() -> str:
    "Get Documents folder"
    if os.name == "nt":
        import ctypes.wintypes

        buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
        ctypes.windll.shell32.SHGetFolderPathW(None, 5, None, 0, buf)
        return str(buf.value)
    else:
        import subprocess

        return subprocess.check_output(
            ["xdg-user-dir", "DOCUMENTS"], universal_newlines=True
        ).strip()


""" I'm unstoppable\n
I'm a Porsche with no brakes\n
I'm invincible\n
Yeah, I win every single game\n
I'm so powerful\n
I don't need batteries to play\n
I'm so confident, yeah, I'm unstoppable today\n
Unstoppable today, unstoppable today\n
Unstoppable today, yeah, I'm unstoppable today\n
Unstoppable today, unstoppable today\n
Unstoppable today, yeah, I'm unstoppable today\n"""

LogToFile = False
AllowEmoji = False

# Absolutely nessesary
CommandPrefix: str = "!"
TOKEN: str = ""
PATH: str = os.path.join(_get_def_doc(), "Hijacked-Node")
StephLog: str = ""

# Mix configs
DevLab: (list, str, set) = set()
LogChan: (list, str, set) = set()
LogAdmin: (list, str, set) = set()
SUPERUSER: (list, str, set) = set()
UserExLixt: (list, str, set) = set()
ChanExList: (list, str, set) = set()
GildExList: (list, str, set) = set()
WordExList: (list, str, set) = set()
WordBanLst: (list, str, set) = set()
DayList: (list, str, set) = set()
DayChan: (list, str, set) = set()
EmoteNest: (list, str, set) = set()

DayDict = {
    "We": os.path.join(PATH, "db", "img", "W.png"),
    "Th": os.path.join(PATH, "db", "img", "J.gif"),
    "Fr": os.path.join(PATH, "db", "img", "V.jpg"),
    "Sa": None,
    "Su": None,
    "Mo": None,
    "Tu": None,
}

WeapList = set(
    "Emojis",
    "Cringe",
    "A chainsaw",
    "Comnism",
    "Capitalism",
    "Anarchism",
    "Memes",
    "An informatic virus",
    "Yo' mama",
    "The BFG",
    "It's own guts",
    "My bare fists",
    "Extraneous furry imagery",
    "An orbital strike",
    "A rocket launcher",
    "A specially annoying kid with aspergers",
    "An assault rifle",
    "A Heaby machinegun",
    "It's own arms",
    "A nuclear bomb",
    "Puppies",
    "javascript",
    "Oracle®",
    "EvilCorp",
    "literally me",
    "A giantic book",
    "the power of God and anime",
)

# I shamelessly stole this from _somewhere_ ( and I don't remember where lol)
# but it was open\n source and staff GPL-2 or GPL-3 at least :shrug:
async def bing_image(query, delta, config: CONF0):
    os.makedirs(os.path.join(config.PATH, "DB", "img", "ext", query), exist_ok=True)
    sys.setrecursionlimit(10000000)
    page_counter, link_counter, download_image_delta = 0, 0, 0
    while download_image_delta < delta:
        ua = UserAgent(verify_ssl=False)
        headers = {"User-Agent": ua.random}
        payload = (("q", str(query)), ("first", page_counter), ("adlt", False))
        source = grequests.get(
            "https://www.bing.com/images/async", params=payload, headers=headers
        ).content
        soup = BeautifulSoup(str(source).replace("\r", "").replace("\n", ""), "lxml")
        links = [
            json.loads(i.get("m").replace("\\", ""))["murl"]
            for i in soup.find_all("a", class_="iusc")
        ]
        await logMe("[%] Indexed: ```" + str(links) + "```")
        for a in soup.find_all("a", class_="iusc"):
            if download_image_delta >= delta:
                break
            iusc = json.loads(a.get("m").replace("\\", ""))
            link = iusc["murl"]
            download_image_delta += 1
            try:
                file_name = link.split("/")[-1]
                type = file_name.split(".")[-1]
                type = (type[:3]) if (len(type) > 3) else type
                if type.lower() == "jpe":
                    type = "jpeg"
                if type.lower() not in [
                    "jpeg",
                    "jfif",
                    "exif",
                    "tiff",
                    "gif",
                    "bmp",
                    "png",
                    "webp",
                    "jpg",
                ]:
                    type = "jpg"
                await logMe(
                    "[%] Downloading Image #"
                    + str(download_image_delta)
                    + " from: ```"
                    + str(link)
                    + "```"
                )
                try:
                    file_path = os.path.join(
                        config.PATH,
                        "DB",
                        "img",
                        "ext",
                        query,
                        "Scrapper_" + str(download_image_delta) + "." + str(type),
                    )
                    ua = UserAgent(verify_ssl=False)
                    headers = {"User-Agent": ua.random}
                    r = grequests.get(link, stream=True, headers=headers)
                    if r.status_code == 200:
                        with open(file_path, "wb") as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                    else:
                        await logMe(
                            "Image returned a " + str(r.status_code) + " error.", True
                        )
                    await logMe("[%] Downloaded File")
                except Exception as e:
                    download_image_delta -= 1
                    await logMe(
                        "[!] Issue Downloading: ```{}```[!] Error: {}".format(link, e),
                        True,
                    )
            except Exception as e:
                download_image_delta -= 1
                await logMe(
                    "[!] Issue getting: ```{}```[!] Error:: {}".format(link, e), True
                )
            link_counter += 1
        page_counter += 1
        if page_counter > 5:
            await logMe("[?] Exedeed max page count (5), ending prematurely")
            break
    await logMe("[%] Done. Downloaded {} images.".format(download_image_delta))


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
                    "Can't send [  "
                    + str(x)
                    + "  ]! from ["
                    + str(ctx.message.id)
                    + "]:```"
                    + str(ctx.message.content)
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


# init
# self.CommandPrefix, self.TOKEN, self.PATH, self.DevLab, self.LogChan, self.LogAdmin,
# self.WeapList, self.SUPERUSER, self.UserExLixt, self.ChanExList, self.AllowEmoji, self.GildExList,
# self.WordExList, self.WordBanLst, self.DayList, self.DayChan, self.EmoteNest, self.StephLog
bot = commands.Bot(command_prefix=config.CommandPrefix, case_insensitive=True)

# debug info
global debugTrigger
debugTrigger = False  # It prints stuff

os.makedirs(os.path.join(config.PATH, "DB"), exist_ok=True)
CORPUS_TXT_PATH = os.path.join(config.PATH, "DB", "corpus.lst")

# GLock
global W_DB, wdict, Dictnry, W_DLOCK, corporae, IsSyncEd

W_DLOCK = False
corporae = [""]
try:
    wdict = pickle.load(open(CORPUS_TXT_PATH + ".pkl", "rb"))
    Dictnry = {v: k for k, v in tqdm(wdict.items())}
    W_DB = {}
    IsSyncEd = True
except Exception:
    wdict, Dictnry, W_DB = {}, {}, {}
    IsSyncEd = False

# GenFuct
async def EMT(message):
    for emote in config.EmoteNest:
        for diff in emote[0]:
            for reply in emote[1]:
                if bool(re.search(diff, message.content.lower())):
                    await message.add_reaction(reply)


# I stole this for someone's™ gitist
async def long_sleep(arg):
    hours = 60 * 60

    async def bg():
        while True:
            await asyncio.sleep(12 * hours)

    task = asyncio.create_task(bg())
    try:
        await asyncio.sleep(arg)
    finally:
        task.cancel()


async def Wednesday():
    while True:
        await logMe("|----------- ItsWednesday Start ------------|")
        tday, tdayImg = config.DayList[dt.datetime.today.weekday()]
        if tday:
            for Chan in config.DayChan:
                async with bot.get_channel(Chan).typing():
                    await bot.get_channel(Chan).send(file=discord.File(tdayImg))
        await logMe("|----------- ItsWednesday End --------------|")
        await logMe("|>---------- Now Waiting a day ------------<|")
        await long_sleep(60 * 60 * 24)


# MkbFunc
async def DefPoint():
    def make_pairs(corpus):
        for i in range(len(corpus) - 2):
            yield (corpus[i], corpus[i + 1])

    corpus = open(CORPUS_TXT_PATH, encoding="utf8").read().split(" ")
    W_D = {}
    for W1, W2 in tqdm(make_pairs(corpus)):
        if W1 in W_D.keys():
            W_D[W1].append(W2)
        else:
            W_D[W1] = [W2]
    return (W_D, corpus)


def UntilPoint(W_DB, corpus, llen, init):
    try:
        llen = abs(llen)
        if llen > 200:
            llen = 200
    except Exception:
        llen = np.random.randint(5, 7)
    global Dictnry
    try:
        chain = [init] if (init) else [np.random.choice(corpus)]
        while Dictnry[chain[0]] in [";", ":", ",", "."]:
            chain = [np.random.choice(corpus)]
        while (len(chain) < llen) or (
            not (("." in Dictnry[chain[-1]]))
            and (len(chain) < np.random.randint(13, 17))
        ):
            chain.append(np.random.choice(W_DB[chain[-1]]))
    except Exception:
        chain = [np.random.choice(corpus)]
        while Dictnry[chain[0]] in [";", ":", ",", "."]:
            chain = [np.random.choice(corpus)]
        while (len(chain) < llen) or (
            not (("." in Dictnry[chain[-1]]))
            and (len(chain) < np.random.randint(13, 17))
        ):
            chain.append(np.random.choice(W_DB[chain[-1]]))
    return chain


async def transsBack(cunn, b=True):
    if os.name == "nt":
        return cunn  # windows bad linux good
    else:
        process = await asyncio.create_subprocess_exec(
            "apertium",
            ("en-es" if (b) else "es-en"),
            "-u",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=subprocess.PIPE,
        )  # fuck pythonic code, all my hommies hate pythonic code - this post was made by the perl gang
        process.stdin.write(str(cunn).encode())
        conn, err_ = await process.communicate()
        if err_:
            await logMe(err_, True)
        del err_
        conn = conn.decode("utf-8")
        await process.stdin.close()
        await process.terminate()
        return conn


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
            for x in [line[i : i + 1994] for i in range(0, len(line), 1994)]:
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
    global IsSyncEd
    if IsSyncEd:
        IsSyncEd = False

        def chPref(skalaline: str):
            for BND in config.PrefBanLst:
                if skalaline.startswith(BND):
                    return True
            return False

        def chLeen(skalaline: str):
            return (
                True
                if (len(skalaline.replace(" ", "")) / len(skalaline.split(" ")) <= 2)
                else False
            )

        def chEmoj(skalaline: str):
            return True if (set(skalaline).isdisjoint(set(UNICODE_EMOJI))) else False

        def chWBan(skalaline: str):
            return (
                True if (set(skalaline).isdisjoint(set(config.WordBanLst))) else False
            )

        await logMe("Rebuilding Dictionary")
        msg = await ctx.send("Rebuilding Dictionary") if (fox) else None
        protocorp, outstring = [], ""
        await msg.edit(content="Loading Parrot Files...") if (fox) else None
        for pkl in glob.glob(os.path.join(config.PATH, "DB", "parrot.*.pkl")):
            with open(pkl, "rb") as pikl:
                for skala in tqdm(pickle.load(pikl)):
                    skala = str(skala).lower()
                    if chPref(skala):
                        continue
                    if chLeen(skala):
                        continue
                    if chEmoj(skala):
                        continue
                    if chWBan(skala):
                        continue
                    for EW in config.WordExList:
                        skala = skala.replace(EW, "")
                    protocorp.append(skala)
        protocorp = [
            await transsBack(unicodedata.normalize("NFC", protoline))
            for protoline in tqdm(protocorp)
        ]
        if config.StephLog:
            await msg.edit(content="Loading STEPH-LOG Files...") if (fox) else None
            for StephFile in glob.glob(os.path.join(config.PATH, "DB", "wsp", "*.lst")):
                with open(StephFile, "r", encoding="utf-8") as skalafile:
                    for skala in tqdm(skalafile.readlines()):
                        skala = str(skala).lower()
                        if chPref(skala):
                            continue
                        if chLeen(skala):
                            continue
                        if chEmoj(skala):
                            continue
                        if chWBan(skala):
                            continue
                        for EW in config.WordExList:
                            skala = skala.replace(EW, "")
                        protocorp.append(skala)
        await msg.edit(content="Prosesing Messages...") if (fox) else None
        outstring = unicodedata.normalize(
            "NFC",
            " ".join(protocorp)
            .replace("*", "")
            .replace("_", "")
            .replace("(", "")
            .replace(")", "")
            .replace("; ", ";")
            .replace(" ;", ";")
            .replace(";", " ; ")
            .replace(": ", ":")
            .replace(" :", ":")
            .replace(":", " : ")
            .replace(", ", ",")
            .replace(" ,", ",")
            .replace(",", " , ")
            .replace(". ", ".")
            .replace(" .", ".")
            .replace(".", " . ")
            .replace(". . .", "...")
            .replace("-", " ")
            .replace("\n", ". ")
            .replace("  ", " ")
            .replace("  ", " ")
            .replace("  ", " ")
            .replace("  ", " ")
            .replace("*", "")
            .replace("_", "")
            .replace("(", "")
            .replace("(", ")")
            .replace("; ", ";")
            .replace(" ;", ";")
            .replace(";", " ; ")
            .replace(": ", ":")
            .replace(" :", ":")
            .replace(":", " : ")
            .replace(", ", ",")
            .replace(" ,", ",")
            .replace(",", " , ")
            .replace(". ", ".")
            .replace(" .", ".")
            .replace(".", " . ")
            .replace(". . .", "...")
            .replace(". . .", "...")
            .replace(". .", "."),
        ).split()  # One heck of a line
        for x in tqdm(range(len(outstring) - 1, 0, -1)):
            try:
                int(outstring[x])
                outstring[x] = len(str(outstring[x])) * "⣿"
            except Exception:
                if re.search("jsjs", outstring[x]) or re.search("jaja", outstring[x]):
                    outstring[x] = "jajaja"
            if len(str(outstring[x])) > 14:
                del outstring[x]
        currentmaxcount, config.tokendic = -1, {}
        open(CORPUS_TXT_PATH, "w", encoding="utf8").close()
        with open(CORPUS_TXT_PATH, "a", encoding="utf8") as oufilestring:
            for word in tqdm(outstring):
                if word in config.tokendic:
                    oufilestring.write(str(config.tokendic[word]) + " ")
                else:
                    currentmaxcount = currentmaxcount + 1
                    config.tokendic[word] = str(currentmaxcount)
                    oufilestring.write(str(config.tokendic[word]) + " ")
        open(CORPUS_TXT_PATH + ".pkl", "w").close()
        with open(CORPUS_TXT_PATH + ".pkl", "wb") as x:
            pickle.dump(config.tokendic, x)
        await msg.edit(content="Database Rebuilded!") if (fox) else None
        await reloadDict(ctx, fox=fox)
        IsSyncEd = True
    else:
        ctx.send("Another database job is running at this time...")


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


@bot.event
async def on_command_error(context, exception):
    print("|--------------- ERR_ START ----------------|")
    print("Ignoring exception in command {}:".format(context.command), file=sys.stderr)
    traceback.print_exception(
        type(exception), exception, exception.__traceback__, file=sys.stderr
    )
    print("|---------------- ERR_ END -----------------|")
    try:
        await logMe(context.message.content)
    except Exception:
        None
    try:
        await logMe(exception, True)
    except Exception:
        None


@bot.event
async def on_error(event_method, *args, **kwargs):
    try:
        await logMe(" ``` " + str(event_method) + " ``` ", True)
        await logMe(" ``` " + traceback.format_exc() + " ``` ", True)
    except Exception:
        print("|--------------- ERR_ START ----------------|")
        print(" Ignoring exception in {}".format(event_method), file=sys.stderr)
        traceback.print_exc()
        print("|----------------- ERR_ END -----------------|")


@bot.event
async def on_message(message):
    await EMT(message)
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


async def doBootUp():  # spagget
    global logMe
    logMe = LogMe(bot, config)

    async def sec():
        await logMe("[ " + str(dt.datetime.now().timestamp()) + " ]")
        await logMe(str(bot.user) + " Is connected to:")
        await logMe("|-------------------------------------------|")
        for guild in bot.guilds:
            await logMe(" - [" + str(guild.id) + "]: " + str(guild.name) + ".")
        await logMe("|-------------------------------------------|")
        await ReSyncDict(fox=False)
        await logMe("|         Bootup Sequence complete          |")
        await bot.change_presence(activity=discord.Game(name="Complex Numbers"))
        # asyncio.create_task(Wednesday())

    await logMe("|---------------doBootUp-st-----------------|")
    await logMe("|Not really an error, but rather an exploit.|", True)
    await logMe("|-------------------------------------------|")
    await bot.change_presence(activity=discord.Game(name="Waking Up..."))
    if config.LogChan:
        async with bot.get_channel(config.LogChan[0]).typing():
            await sec()
    else:
        await sec()
    await logMe("|-------------- doBootUp End ---------------|")


@bot.event
async def on_ready():
    await doBootUp()


