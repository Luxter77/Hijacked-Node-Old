import subprocess
import asyncio
import os

import numpy as np

from hijackednode.configuration import CONF0
from hijackednode import tqdm
class TalkBox:
    'This is where the magic happens'
    def __init__(self, config: CONF0):

        self.CORPUS_TXT_PATH = os.path.join(config.PATH, "corpus.lst")
        os.makedirs(os.path.join(config.PATH, "DB"), exist_ok=True)


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
        return(conn)