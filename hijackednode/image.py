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