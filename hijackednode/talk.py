from json.decoder import JSONDecodeError
from random import choice, randint

from .configuration import CONF0  # pylint: disable=relative-beyond-top-level
from concurrent.futures import ThreadPoolExecutor
from emoji import EMOJI_UNICODE_ENGLISH
from copy import deepcopy
from typing import List

import subprocess as sp
import unicodedata
import asyncio
import json
import os
import re

class TalkBoxError(Exception):
    ...  # Placeholder lol

# define FPCAMHHPC = "fuck pythonic code, all my homies hate pythonic code - this post was made by the perl gang"

def trans(text: str, ptq: str) -> str:
    if os.name != "nt":  # windows bad linux good
        # FPCAMHHPC
        process: sp.Popen = sp.Popen(["/usr/bin/apertium", ptq, "-u"], stdout=sp.PIPE, stdin=sp.PIPE)
        process.stdin.write(text.encode())
        text = process.communicate()[0].decode("utf-8")
    return text

def trans_back(text: str, org: str = 'es'):
    if org == 'en':
        return trans(trans(text, ptq='en-es'), ptq='es-en')
    elif org == 'es':
        return trans(trans(text, ptq='es-en'), ptq='en-es')
    else:
        raise(Exception('LangNotSupportedError'))

class TextPipeLine:
    'The thing that chews all the text and stuff'

    TEXT_PATCHES = {
        "forward": [("(", "",), (")", "",), ("[", "",), ("]", "",), ("{", "",), ("}", "",), ("*", "",), ('"', ''),
                    ("-", " ",), ("\n", ". ",), ("_", "",), (":", " : ",), (";", " ; ",), (",", " , ",),
                    (".", " . ",), ('  ', ' ',), ('  ', ' ',), (". . .", "...",), ('1', '⣿',), ('2', '⣿',),
                    ('3', '⣿',), ('4', '⣿',), ('5', '⣿',), ('6', '⣿',), ('7', '⣿',), ('8', '⣿',), ('9', '⣿',),
                    ('jsjs', 'jajaja',), ('jaja', 'jajaja',)],
        "backward": [(" :", ":",), (" ;", ";",), (" , ", ", ",), (" .", ".",), (" i ", " Yo ",)],
    }

    def __init__(self, config: CONF0):
        self.config: CONF0 = config

    def plex(self, text: str, direction: str = 'forward') -> str:
        # poor choice, but I don't care
        for x, y in (self.TEXT_PATCHES[direction]):
            text = text.replace(x, y)

        for patch in self.config.WordExList:
            text = text.replace(' ' + patch, '')
            text = text.replace(patch + ' ', '')
            text = text.replace(patch, '')

        if direction == 'backward':
            return re.sub("⣿", (lambda _: str(randint(0, 9))), text)
        else:
            return text

    def checks(self, skala: str) -> bool:
        if ((len(skala) < self.config.SkalaMinStrLen) or ((len(skala.replace(" ", "")) / len(skala.split(" "))) <= self.config.SkalaRatio) or (bool(re.search('[\u0400-\u04FF]', skala)) and self.config.RejectCyrillic) or not(set(skala).isdisjoint(set(EMOJI_UNICODE_ENGLISH.values()))) or not(set(skala).isdisjoint(set(self.config.WordBanLst)))):
            return False
        else:
            for banned in self.config.PrefBanLst:
                if skala.startswith(banned):
                    return False
        return True

    async def load_from_discord_dump(self) -> List[str]:
        "It's a bad multilingual pun"
        # WARNING: you should set up a lock outside from this function
        try:
            with open(os.path.join(self.config.PATH, "DB", "parrot", "parrot.json"), 'r') as corp_file:
                chat_log   = json.load(corp_file)
                proto_corp = list()
        except JSONDecodeError:
            try:
                with open(os.path.join(self.config.PATH, "DB", "parrot", "parrot.bkp.json"), 'r') as corp_file:
                    chat_log   = json.load(corp_file)
                    proto_corp = list()
            except FileNotFoundError:
                chat_log   = {'last_time': None}
            proto_corp = list()
        except FileNotFoundError:
            chat_log   = {'last_time': None}
            proto_corp = list()

        del chat_log['last_time']

        for server in chat_log:
            for channel in server:
                for message in channel:
                    message = str(message)
                    if self.checks(message):
                        proto_corp += await self.parse_message(message)
        return(proto_corp)

    async def load_from_steph_logs(self) -> List[str]:
        proto_corp = list()
        for steph_path in self.config.StephLogs:
            with open(steph_path, "r", encoding="utf-8") as steph_file:
                for line in steph_file.readlines():
                    line = line.lower()
                    if self.checks(line):
                        proto_corp += await self.parse_message(line)
        return(proto_corp)

    async def parse_message(self, text: str) -> List[str]:
        text = text.lower()

        for word in text.split(' '):
            if(len(word) > 14):
                text.replace(word, '')

        text = self.plex(unicodedata.normalize("NFC", text)).lower().split()  # FPCAMHHPC

        try:
            if (text[-1] == '.'):
                if (text[-2] == '.'):
                    if (text[-3] == '.'):
                        text = text[:-2]
                    else:
                        text = text[:-1]
            else:
                text = text + ['.']
        except IndexError:
            return [] # I pretend I do not see it

        if bool(text):
            return text
        else:
            return []

def gen_text(end_word: str, until: int, max_length: int, primer: str, init: List[str], trans_map: dict, chain: dict, pipeline: TextPipeLine) -> str:
    if bool(randint(0, 1)):
        until += randint(0, 2)
    else:
        until = max(until - randint(0, 6), until)
    if bool(primer) and not(init):
        try:
            sms = [trans_map['wtn'][primer.lower()]]
        except KeyError:
            return(f'No conozco la palabra: "{primer}"')
    elif bool(init):
        try:
            sms = [trans_map['wtn'][init[-1].lower()]]
        except KeyError:
            sms = [trans_map['wtn'][choice(trans_map['ntw'])]]
    else:
        sms = [trans_map['wtn'][choice(trans_map['ntw'])]]
    while ((len(sms) < until) or (sms[-1] != trans_map['wtn'][end_word]) or not(len(sms) > max_length)):
        sms.append(choice(chain[sms[-1]]))

    sms = pipeline.plex(' '.join([trans_map['ntw'][word] for word in sms]), 'backward')

    if pipeline.config.TransBack:
        sms = trans_back(sms)

    if bool(init):
        sms = ' '.join(init[:-1]) + " " + sms
    return(' '.join(x for x in sms.split(' ') if bool(x)).lower().capitalize())

class TalkBox:
    'This is where the magic happens'

    PULL_LOCK   = asyncio.Lock()          # Lock for pulling messages from discord servers
    TRANS_LOCK  = asyncio.Lock()          # Lock for trans_map AND all_text AND all_words AND chain
    CORPUS_LOCK = asyncio.Lock()          # Lock for the files on disk that hold the corpus
    TREAD_POOL  = ThreadPoolExecutor(10)  # I am a bad person and so are you for using my code

    def __init__(self, config: CONF0):
        self.config: CONF0 = config
        self.pipeline = TextPipeLine(config)
        os.makedirs(os.path.join(config.PATH, "DB"), exist_ok=True)

    async def reload_dict(self) -> None:
        async with self.TRANS_LOCK:
            async with self.CORPUS_LOCK:
                self.all_text:  list = (await self.pipeline.load_from_steph_logs()) + (await self.pipeline.load_from_discord_dump())
            self.all_words: list = list(set(self.all_text))
            self.trans_map: dict = {'ntw': self.all_words, 'wtn': dict((x, i,) for i, x in enumerate(self.all_words))}
        await self.mk_chain()

    async def mk_chain(self) -> None:
        async with self.TRANS_LOCK:
            trans_map = deepcopy(self.trans_map)
        chain = dict()
        primer = trans_map['wtn'][trans_map['ntw'][0]]
        for word in self.all_text:  # pylint: disable=not-an-iterable # are you bucking kidding me pylint? thats a list! how can it be non iterable???
            word = trans_map['wtn'][word]
            try:
                chain[primer].append(word)
            except KeyError:
                chain[primer] = [word]
            finally:
                primer = word

        async with self.TRANS_LOCK:
            self.chain = chain

    async def until_word(self, end_word: str = '.', until: int = 5, max_length: int = 10, primer: str = False, init: List[str] = False) -> str:
        # TODO: Move these hardcoded settings to the config file
        async with self.TRANS_LOCK:
            chain = deepcopy(self.chain)
            trans_map = deepcopy(self.trans_map)

        # the ugliest thing you will ever see because I have no idea what am I doing but it seems to make program go fast so here we are
        # Todo: Actually understand what the heck did I do here
        return(await asyncio.wrap_future(self.TREAD_POOL.submit(gen_text, end_word=end_word, until=until, max_length=max_length, primer=primer, init=init, chain=chain, trans_map=trans_map, pipeline=self.pipeline)))

    def sync_until_word(self, end_word: str = '.', until: int = 5, max_length: int = 10, primer: str = False, init: List[str] = False) -> str:
        return(asyncio.run(self.until_word(end_word=end_word, until=until, max_length=max_length, primer=primer, init=init)))
