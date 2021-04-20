# TODO: MAKE THIS NON BLOKING

from fake_useragent import FakeUserAgent
from bs4 import BeautifulSoup
from time import time

from .configuration import CONF0

import requests
import shutil
import json
import sys
import os

sys.setrecursionlimit(10000)

# I shamelessly stole this from _somewhere_ ( and I don't remember where lol)
# but it was open\n source and staff GPL-2 or GPL-3 at least :shrug:
async def bing_image(query: str, delta: int, config: CONF0):
    os.makedirs(os.path.join(config.PATH, "DB", "img", "ext", query), exist_ok=True)

    p_counter, l_counter, d_delta = 0, 0, 0
    ua = FakeUserAgent(verify_ssl=False)

    while (d_delta < delta):
        headers, payload = {"User-Agent": ua.random}, {"q": query, "first": p_counter, "adlt": False}
        soup = BeautifulSoup(requests.get("https://www.bing.com/images/async", params=payload, headers=headers).content, "lxml")

        for a in soup.find_all("a", class_="iusc"):
            if d_delta >= delta:
                break

            iusc = json.loads(a.get("m").replace("\\", ""))

            d_delta += 1

            try:
                type = iusc["murl"].split("/")[-1].split(".")[-1]

                # I have no idea
                type = (type[:3]) if (len(type) > 3) else type

                if type.lower() == "jpe":
                    type = "jpeg"
                if type.lower() not in ["jpeg", "jfif", "exif", "tiff", "gif", "bmp", "png", "webp", "jpg"]:
                    type = "jpg"

                try:
                    file_path = os.path.join(config.PATH, "DB", "img", "ext", query, f"Scrapper_{str(d_delta)}_{str(round(time()))}." + str(type))
                    headers = {"User-Agent": ua.random}
                    r = requests.get(iusc["murl"], stream=True, headers=headers)
                    if r.status_code == 200:
                        with open(file_path, "wb") as f:
                            r.raw.decode_content = True
                            shutil.copyfileobj(r.raw, f)
                except Exception:
                    d_delta -= 1

            except Exception:
                pass  # lol
            l_counter += 1
        p_counter += 1
        if p_counter > 5:
            break
