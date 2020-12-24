import datetime as dt
import unicodedata
import subprocess
import asyncio
import pickle
import glob
import sys
import os
import re

import numpy as np

from tqdm.asyncio import tqdm as asynctqdm
from discord import Game, MessageType
from discord.ext.commands import Bot
from emoji import UNICODE_EMOJI
from tqdm.auto import tqdm


from .useful import transsBack, repl_fun
from .configuration import CONF0
from .logger import LogMe

'''
WARNING! ONLY LVL40+ SPAGHETTI COOKS ALLOWED FROM HERE ON OUT ON THIS FILE
'''


class TalkBox:
    'This is where the magic happens'

    __thingamagins__ = ['W_DB', 'wdict', 'Dictnry',
                        'W_DLOCK', 'corporae', 'IsSyncEd']
    sync_lock = asyncio.Lock()

    def __init__(self, config: CONF0, bot: Bot, logMe: LogMe):
        self.config = config
        self.bot = bot
        self.logMe = logMe
        os.makedirs(os.path.join(self.config.PATH, "DB"), exist_ok=True)
        self.wdict = self.Dictnry = self.W_DB = dict()
        try:
            self.corpus_file = os.path.join(self.config.PATH, "corpus.lst")
            self.corpus = open(
                self.corpus_file, encoding="utf8").read().split(" ")
            self.wdict = pickle.load(open(self.corpus_file + ".pkl", "rb"))
            for k, v in tqdm(self.wdict.items()):
                self.Dictnry[v] = k
        except FileNotFoundError:
            asyncio.create_task(self.pull_messages())

    def _make_pairs(self, corpus: list):
        for i in range(len(corpus) - 2):
            yield (corpus[i], corpus[i + 1])

    def lastTimeW(self, noww):
        with open(
                os.path.join(self.config.PATH, "parrot", "lasttime.pkl"), "wb") as lasttimme:
            pickle.dump(noww, lasttimme)

    def chPref(self, skalaline: str):
        for start in self.config.PrefBanLst:
            if(skalaline.startswith(start)):
                return(True)

    def chLeen(self, skalaline: str):
        if (len(skalaline.replace(" ", "")) / len(skalaline.split(" ")) <= 2):
            return(True)

    def chEmoj(self, skalaline: str):
        if (set(skalaline).isdisjoint(set(UNICODE_EMOJI))):
            return(True)

    def chWBan(self, skalaline: str):
        if (set(skalaline).isdisjoint(set(self.config.WordBanLst))):
            return(True)

    async def gen_text(self, llen: int = None, init: str = None, formated: bool = False) -> str:
        if not(self.sync_lock.locked()):
            llen = 200 if((llen > 200) and llen) else (
                llen if(llen) else np.random.randint(5, 7))
            try:
                chain = [init] if (init) else [np.random.choice(self.corpus)]
                while self.Dictnry[chain[0]] in [";", ":", ",", "."]:
                    chain = [np.random.choice(self.corpus)]
                while (len(chain) < llen) or (
                    not (("." in self.Dictnry[chain[-1]])
                         ) and (len(chain) < np.random.randint(13, 17))
                ):
                    chain.append(np.random.choice(self.W_DB[chain[-1]]))
            except KeyError:
                chain = [np.random.choice(self.corpus)]
                while self.Dictnry[chain[0]] in [";", ":", ",", "."]:
                    chain = [np.random.choice(self.corpus)]
                while (len(chain) < llen) or (
                    not (("." in self.Dictnry[chain[-1]]))
                    and (len(chain) < np.random.randint(13, 17))
                ):
                    chain.append(np.random.choice(self.W_DB[chain[-1]]))
            sms = (" ".join(self.Dictnry[str(word)] for word in chain)
                   .replace(" ;", ";").replace(" :", ":")
                   .replace(" .", ".").replace(" ,", ","))

            sms = " ".join(str(await transsBack(sms, True)).split())

            sms = re.sub("⣿", repl_fun, sms).replace(" i ", " Yo ")

            if sms.startswith("i "):
                sms = re.sub("^i ", "yo ", sms, flags=re.M)

            sms = sms.lower().capitalize()
            return(sms)
        else:
            return('')

    async def build_chain(self, fromFile: bool = True):
        async with self.sync_lock:
            if(fromFile):
                self.corpus = open(
                    self.corpus_file, encoding="utf8").read().split(" ")
            W_D = dict()
            for W1, W2 in tqdm(self._make_pairs(corpus=self.corpus)):
                if W1 in W_D.keys():
                    W_D[W1].append(W2)
                else:
                    W_D[W1] = [W2]
            self.W_DB = W_D

    async def pull_messages(self):
        async with self.sync_lock:
            await self.logMe("Updating message database!")

            def PPATH(noww):
                return str(os.path.join(self.config.PATH, "parrot", "parrot." + str(noww.timestamp()) + ".pkl"))

            async def lastTimeR():
                try:
                    with open(os.path.join(self.config.PATH, "parrot", "lasttime.pkl"), "rb") as lasttimme:
                        return pickle.load(lasttimme)
                except Exception:
                    await self.bot.change_presence(activity=Game(name="Initializing database..."))
                    return(None)

            await self.bot.change_presence(activity=Game(name="Updating database..."))
            noww = dt.datetime.now()
            messages_all = []
            for guild in tqdm(self.bot.guilds):
                if guild.id in self.config.GildExList:
                    continue
                await self.logMe(
                    "Now processing: " +
                    str(guild.name) + " (" + str(guild.id) + ")",
                    False,
                    False,
                )
                for channel in tqdm(guild.text_channels):
                    if channel in self.config.ChanExList:
                        continue
                    try:
                        await self.logMe(
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
                            if message.type == MessageType.default and not (
                                message.author.id in self.config.UserExLixt
                            ):
                                messages_all.append(message.content)
                    except Exception as err_:
                        await self.logMe(
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
                        await self.logMe(err_, True, False)
            with open(PPATH(noww), "wb") as parrot_pkl:
                pickle.dump(messages_all, parrot_pkl)
            self.lastTimeW(noww)
        await self.rebuild_dictionary()

    async def rebuild_dictionary(self):
        async with self.sync_lock:
            await self.logMe("Rebuilding Dictionary")
            protocorp, outstring = [], ""
            for pkl in glob.glob(os.path.join(self.config.PATH, "parrot", "parrot.*.pkl")):
                with open(pkl, "rb") as pikl:
                    for skala in tqdm(pickle.load(pikl)):
                        skala = str(skala).lower()
                        if self.chPref(skala) or self.chLeen(skala) or self.chEmoj(skala) or self.chWBan(skala):
                            continue
                        for EW in self.config.WordExList:
                            skala = skala.replace(EW, "")
                        protocorp.append(skala)
            protocorp = [
                await transsBack(unicodedata.normalize("NFC", protoline))
                for protoline in tqdm(protocorp)
            ]
            if self.config.StephLog:
                for StephFile in glob.glob(os.path.join(self.config.PATH, "wsp", "*.lst")):
                    with open(StephFile, "r", encoding="utf-8") as skalafile:
                        for skala in tqdm(skalafile.readlines()):
                            skala = str(skala).lower()
                            if self.chPref(skala) or self.chLeen(skala) or self.chEmoj(skala) or self.chWBan(skala):
                                continue
                            for EW in self.config.WordExList:
                                skala = skala.replace(EW, "")
                            protocorp.append(skala)
            outstring = unicodedata.normalize(
                "NFC",
                " ".join(protocorp).replace(
                    "*", "").replace("_", "").replace("(", "")
                .replace(")", "").replace("; ", ";").replace(" ;", ";").replace(";", " ; ")
                .replace(": ", ":").replace(" :", ":").replace(":", " : ").replace(", ", ",")
                .replace(" ,", ",").replace(",", " , ").replace(". ", ".").replace(" .", ".")
                .replace(".", " . ").replace(". . .", "...").replace("-", " ").replace("\n", ". ")
                .replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
                .replace("*", "").replace("_", "").replace("(", "").replace("(", ")").replace("; ", ";")
                .replace(" ;", ";").replace(";", " ; ").replace(": ", ":").replace(" :", ":")
                .replace(":", " : ").replace(", ", ",").replace(" ,", ",").replace(",", " , ")
                .replace(". ", ".").replace(" .", ".").replace(".", " . ").replace(". . .", "...")
                .replace(". . .", "...").replace(". .", ".")).split()  # One heck of a line
            for x in tqdm(range(len(outstring) - 1, 0, -1)):
                try:
                    int(outstring[x])
                    outstring[x] = len(str(outstring[x])) * "⣿"
                except Exception:
                    if re.search("jsjs", outstring[x]) or re.search("jaja", outstring[x]):
                        outstring[x] = "jajaja"
                if len(str(outstring[x])) > 14:
                    del outstring[x]
            currentmaxcount, tokendic = -1, {}
            open(self.corpus_file, "w", encoding="utf8").close()
            with open(self.corpus_file, "a", encoding="utf8") as oufilestring:
                for word in tqdm(outstring):
                    if word in tokendic:
                        oufilestring.write(str(tokendic[word]) + " ")
                    else:
                        currentmaxcount = currentmaxcount + 1
                        tokendic[word] = str(currentmaxcount)
                        oufilestring.write(str(tokendic[word]) + " ")
            open(self.corpus_file + ".pkl", "w").close()
            with open(self.corpus_file + ".pkl", "wb") as x:
                pickle.dump(tokendic, x)
            await self.bot.change_presence(activity=Game(name="Loading new dictionary files..."))
            await self.logMe("Reloading dictionary files")
            self.wdict = tokendic
            self.Dictnry = {v: k for k, v in tokendic.items()}
            await self.bot.change_presence(activity=Game(name="Complex Numbers"))
        await self.build_chain(fromFile=False)


talkbox = None
