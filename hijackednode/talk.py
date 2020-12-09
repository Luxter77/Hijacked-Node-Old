import subprocess
import asyncio
import pickle
import os

import numpy as np

from .configuration import CONF0
from tqdm.auto import tqdm
from . import logMe, config

'''
WARNING! ONLY LVL10+ SPAGHETTI COOKS ALLOWED FROM HERE ON OUT ON THIS FILE
'''

class TalkBox:
    'This is where the magic happens'

    __thingamagins__ = ['W_DB', 'wdict', 'Dictnry',
                        'W_DLOCK', 'corporae', 'IsSyncEd']
    sync_lock = asyncio.Lock()

    def __init__(self):

        self.corpus_file = os.path.join(config.PATH, "corpus.lst")
        os.makedirs(os.path.join(config.PATH, "DB"), exist_ok=True)

        self.corporae = [""]

        try:
            self.wdict = pickle.load(open(self.corpus_file + ".pkl", "rb"))

            self.Dictnry = {v: k for k, v in tqdm(self.wdict.items())}

            self.W_DB = dict()
        except Exception:
            self.wdict = self.Dictnry = self.W_DB = dict()

    def _make_pairs(corpus: list):
        for i in range(len(corpus) - 2):
            yield (corpus[i], corpus[i + 1])

    # MkbFunc
    async def build_chain(self):
        corpus = open(self.corpus_file, encoding="utf8").read().split(" ")
        W_D = dict()

        for W1, W2 in tqdm(self._make_pairs(corpus)):
            if W1 in W_D.keys():
                W_D[W1].append(W2)
            else:
                W_D[W1] = [W2]

        async with self.sync_lock:
            self.corpus = corpus
            self.W_D = W_D

    async def gen_text(self, llen: int = None, init: str = None, fromated: bool = False):
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
        except Exception:
            chain = [np.random.choice(self.corpus)]
            while self.Dictnry[chain[0]] in [";", ":", ",", "."]:
                chain = [np.random.choice(self.corpus)]
            while (len(chain) < llen) or (
                not (("." in self.Dictnry[chain[-1]]))
                and (len(chain) < np.random.randint(13, 17))
            ):
                chain.append(np.random.choice(self.W_DB[chain[-1]]))
        return chain

    async def transsBack(cunn: str, b: bool = True) -> str:
        if(os.name == "nt"):
            return(cunn)  # windows bad linux good
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
            return(conn)
