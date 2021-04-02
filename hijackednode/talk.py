from random import choice, randint
from .configuration import CONF0
from emoji import UNICODE_EMOJI
from copy import deepcopy
from typing import List
from glob import glob
import unicodedata
import asyncio
import json
import os
import re

# define FPCAMHHPC = "fuck pythonic code, all my homies hate pythonic code - this post was made by the perl gang"

async def trans(text, ptq) -> str:
    if os.name != "nt":  # windows bad linux good
        # FPCAMHHPC
        process = await asyncio.create_subprocess_exec(
            "apertium", ptq, "-u", stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)
        process.stdin.write(str(text).encode())
        text = (await process.communicate())[0].decode("utf-8")
        await process.stdin.close()
        await process.terminate()
    return text

async def trans_back(text: str, org: str = 'es'):
    if org == 'en':
        await trans(await trans(text, 'en-es'), 'es-en')
    elif org == 'es':
        await trans(await trans(text, 'es-en'), 'en-es')
    else:
        raise(Exception('LangNotSupportedError'))

class TextPipeLine:
    'The thing that chews all the text and stuff'

    TEXT_PATCHES = {
        "forward": [("(", ""), (")", ""), ("[", ""), ("]", ""), ("{", ""), ("}", ""), ("*", ""),
                    ("-", " "), ("\n", ". "), ("_", ""), (" :", ":"), (": ", ":"), (":", " : "),
                    ("; ", ";"), (" ;", ";"), (";", " ; "), (" ,", ","), (", ", ","), (",", " , "),
                    (" .", "."), (". ", "."), (".", " . "), (". . .", "..."), ("  ", " "), ("  ", " "),
                    ('1', '⣿'), ('2', '⣿'), ('3', '⣿'), ('4', '⣿'), ('5', '⣿'), ('6', '⣿'), ('7', '⣿'),
                    ('8', '⣿'), ('9', '⣿'), ('jsjs', 'jajaja'), ('jaja', 'jajaja')],
        "backward": [(" :", ":"), (" ;", ";"), (" , ", ", "), (" .", "."), (" i ", " Yo ")],
    }

    def __init__(self, config: CONF0):
        self.config: CONF0 = config
        self.CORPUS_TXT_PATH = os.path.join(config.PATH, "corpus.lst")

    def plex(self, text: str, direction: str = 'forward') -> str:
        # poor choice, but I don't care
        for patch in (self.TEXT_PATCHES[direction] + list(' ' + bw for bw in self.config.WordExList) + list(' ' + bw for bw in self.config.WordExList)):
            for x, y in patch:
                text = text.replace(x, y)
        return(re.sub("⣿", (lambda: str(randint(0, 9))), text))

    def checks(self, skala: str):
        if (len(skala.replace(" ", "")) / len(skala.split(" ")) <= 2) or (set(skala).isdisjoint(set(UNICODE_EMOJI))) or (set(skala).isdisjoint(set(self.config.WordBanLst))):
            return False
        else:
            for banned in self.config.PrefBanLst:
                if skala.startswith(banned):
                    return False
        return True

    async def load_from_discord_dump(self) -> List[str]:
        "It's a bad multilingual pun"
        # WARNING: you should set up a lock outside from this function
        with open(os.path.join(self.config.PATH, "DB", "parrot.json"), 'r') as corp_file:
            chat_log, proto_corp = json.load(corp_file), list()

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
        if self.config.StephLog:
            for steph in glob(os.path.join(self.config.PATH, "DB", "wsp", "*.lst")):
                with open(steph, "r", encoding="utf-8") as steph_file:
                    for line in (steph_file.readlines()):
                        line = line.lower()
                        if self.checks(line):
                            proto_corp += await self.parse_message(line)

        return(proto_corp)

    async def parse_message(self, text: str) -> List[str]:
        text = text.lower()

        for word in text.split(' '):
            if(len(word) > 14):
                text.replace(word, '')

        text = ((await self.plex(await trans_back(unicodedata.normalize("NFC", text)), 'forward')))  # FPCAMHHPC

        if not(text.endswith('.')):
            return(text.split())

        return(text.split() + ['.'])

class TalkBox:
    'This is where the magic happens'

    PULL_LOCK   = asyncio.Lock()  # Lock for pulling messages from discord servers
    TRANS_LOCK  = asyncio.Lock()  # Lock for trans_map AND all_text AND all_words AND chain
    CORPUS_LOCK = asyncio.Lock()  # Lock for the files on disk that hold the corpus

    def __init__(self, config: CONF0):
        self.config = config
        self.pipeline = TextPipeLine(config)
        os.makedirs(os.path.join(config.PATH, "DB"), exist_ok=True)
        self.reload_dict()

    def reload_dict(self) -> None:
        with self.TRANS_LOCK:
            self.all_text:  list = self.get_chat()
            self.all_words: list = list(set(self.all_text))
            self.trans_map: dict = {'ntw': self.all_words, 'wtn': dict((x, i,) for i, x in enumerate(self.all_words))}
        self.mk_chain()

    def get_chat(self) -> List[str]:
        try:
            with self.CORPUS_LOCK:
                chat = None  # Magic is supposed to happen here!
                return chat
        except FileNotFoundError:
            ...  # More magic to pull more things

    def mk_chain(self) -> None:
        with self.TRANS_LOCK:
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

        with self.TRANS_LOCK:
            self.chain = chain

    def until_word(self, end_word: str = '.', until: int = 15, max_length: int = 40, primer: str = False, init: list = False) -> str:
        # TODO: Move these hardcoded settings to the config file
        with self.TRANS_LOCK:
            chain = deepcopy(self.chain)
            trans_map = deepcopy(self.trans_map)

        if bool(primer) and not(init):
            sms = [trans_map['wtn'][primer]]
        elif bool(init):
            try:
                sms = [trans_map['wtn'][init[-1]]]
            except KeyError:
                sms = [trans_map['wtn'][choice(trans_map['ntw'])]]
        else:
            sms = [trans_map['wtn'][choice(trans_map['ntw'])]]

        while ((len(sms) < until) or (sms[-1] != trans_map['wtn'][end_word]) or not(len(sms) > max_length)):
            sms.append(choice(chain[sms[-1]]))

        sms = self.pipeline.plex(' '.join([trans_map['ntw'][word] for word in sms]), 'backward')

        if bool(init):
            sms = ' '.join(init) + " " + sms

        return(sms)
