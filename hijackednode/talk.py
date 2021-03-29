from hijackednode.configuration import CONF0
from random import choice, randint
from copy import deepcopy
from typing import List
import asyncio
import os
import re


class TalkBox:
    'This is where the magic happens'

    PATCHES = {
        "forward": [("(", ""), (")", ""), ("[", ""), ("]", ""), ("{", ""), ("}", ""), ("*", ""),
                    ("-", " "), ("\n", ". "), ("_", ""), (" :", ":"), (": ", ":"), (":", " : "),
                    ("; ", ";"), (" ;", ";"), (";", " ; "), (" ,", ","), (", ", ","), (",", " , "),
                    (" .", "."), (". ", "."), (".", " . "), (". . .", "..."), ("  ", " "), ("  ", " ")],
        "backward": [(" :", ":"), (" ;", ";"), (" , ", ", "), (" .", "."), (" i ", " Yo ")],
    }

    TRANS_LOCK  = asyncio.Lock()  # Lock for trans_map AND all_text AND all_words AND chain
    CORPUS_LOCK = asyncio.Lock()  # Lock for the files on disk that hold the corpus

    def __init__(self, config: CONF0):

        self.CORPUS_TXT_PATH = os.path.join(config.PATH, "corpus.lst")
        os.makedirs(os.path.join(config.PATH, "DB"), exist_ok=True)
        self.load_dict()

    def reload_dict(self):
        with self.TRANS_LOCK:
            self.all_text  = self.get_chat()
            self.all_words = list(set(self.all_text))
            self.trans_map = {'ntw': self.all_words, 'wtn': dict((x, i,) for i, x in enumerate(self.all_words))}
        self.mk_chain()

    def get_chat(self) -> List[str]:
        try:
            with self.CORPUS_LOCK:
                chat = None  # Magic is supposed to happen here!
                return chat
        except FileNotFoundError:
            ...  # More magic to pull more things

    def mk_chain(self):
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

        sms = self._plex(' '.join([trans_map['ntw'][word] for word in sms]), 'backward')
        sms = re.sub("⣿", (lambda: str(randint(0, 9))), sms)

        if bool(init):
            sms = ' '.join(init) + " " + sms

        return(sms)

    def _plex(self, text: str, direction: str = 'forward') -> str:
        for patch in self.PATCHES[direction]:
            for x, y in patch:
                text = text.replace(x, y)
            return(text)

    def _skala_checks(self, skala: str):
        if (len(skala.replace(" ", "")) / len(skala.split(" ")) <= 2) or (set(skala).isdisjoint(set(UNICODE_EMOJI))) or (set(skala).isdisjoint(set(self.config.WordBanLst))):
            return True
        else:
            for nono in self.config.PrefBanLst:
                if skala.startswith(nono):
                    return True
        return False

    def _pipeline(self, skala: str) -> str:
        ...