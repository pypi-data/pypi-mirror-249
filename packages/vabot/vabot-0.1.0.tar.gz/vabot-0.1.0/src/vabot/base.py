# BASE VABOT

import httpx
import os

from typing import Optional, Any
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from rich import print

from vabot.config import BaseConfig as cfg

ua = UserAgent()

class BaseChatBotAI(object):
    def search_with_bing(self, query: str):
        url: str = "https://www.bing.com/"
        params: dict[str, Any] = {
            "q": query,
            "form": "QBLH",
            "sp": -1,
            "ghc": 1,
            "lq": 0,
            "pq": query,
            "sc": "11-14",
            "qs": "n",
            "sk": "",
            "cvid": "990C10F11D944BCDA403229F51D97078",
            "ghsh": 0,
            "ghacc": 0,
            "ghpl": "",
        }
        headers: dict[str, Any] = {
            "User-Agent": ua.edge
        }
        search_url = url + "search"
        response = httpx.get(search_url, params=params, headers=headers)
        print("Process URL: {}".format(response.url))

        # get response
        f = open(os.path.join(cfg.BASE_DIR, "response.html"), "w+", encoding="UTF-8")
        f.write(response.text)
        f.close()

        soup: BeautifulSoup = BeautifulSoup(response.text, "html.parser")

        try:
            contents = soup.find("div", attrs={"id": "b_wpt_data"}).get("data-sydctx")
            return contents
        except:
            contents = "Data Tidak Ditemukan"
            return contents