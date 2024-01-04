import os

from bs4 import BeautifulSoup

from vabot.config import BaseConfig as cfg

class VabotDebug(object):    
    def search_with_bing(self):
        html = open(os.path.join(cfg.BASE_DIR, "response.html"), "r", encoding="UTF-8")
        

        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        try:
            contents = soup.find("div", attrs={"id": "b_wpt_data"}).get("data-sydctx")
            return contents
        except:
            contents = "Data Tidak Ditemukan"