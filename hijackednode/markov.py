from itertools import chain
from random import choice
from typing import List

import asyncio

def pad_rol_win(seq, size: int = 3, start = None, end = None):
    its, size_ = [], 0

    for _ in range(size):
        its.append(chain((start for _ in range(size - size_)), iter(seq), (end for _ in range(size_))))
        size_ += 1

    while True:
        try:
            tmp = []
            for n in range(size):
                tmp.append(its[n].__next__())
            yield tuple(tmp)
        except StopIteration:
            yield tuple(end for _ in range(size))
            break

class MarkovChain:
    START_KEY = "__START_KEY__"
    END___KEY = "__END___KEY__"

    def __init__(self, order: int = None):
        self.chain: dict        = dict()
        self.order: int         = (order or 2)
        self.lock: asyncio.Lock = asyncio.Lock()

    def gen_chain(self, all_text: List[list]):
        chain = dict()
        for line in all_text:
            for window in pad_rol_win(line, size=(self.order + 1), start=self.START_KEY, end=self.END___KEY):
                try:
                    chain[window[:-1]].append(window[-1])
                except KeyError:
                    chain[window[:-1]] = [window[-1]]

        self.chain: dict = chain
        self.ready: bool = True

    def next_word(self, previous: List[str] = None) -> str:
        p_len = len(previous or [])
        if p_len > self.order:
            previous = list(self.START_KEY for _ in range(self.order - p_len)) + previous
        return choice(self.chain[previous])

    def gen_text(self, min: int = 5, max: int = 10, init: List[str] = None):
        if init:
            text = init[:-self.order]
        else:
            text = self.START_KEY
        while (len(text) > min) or ((text[-1] != self.END___KEY) and (len(text) < max)):
            text.append(self.next_word(text[-1], text[-2]))

        if text[-1] != self.END___KEY:
            text.append(self.END___KEY)

        text = ' '.join(text).replace(self.END___KEY, '.').replace(self.START_KEY, '').replace(' ', '')

        return [init[-self.order:]] + text
