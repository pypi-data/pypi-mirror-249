from openai import OpenAI
from typing import Optional

import httpx
import os

from typing import Optional, Any
from httpx import Client
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from rich import print

from vabot.config import BaseConfig as cfg
from vabot.base import BaseChatBotAI

class ChatBotAI(BaseChatBotAI):
    def __init__(
        self, api_key: Optional[str] = None, organization_id: Optional[str] = None) -> None:
        self.api_key: Optional[str] = api_key
        self.engine: str = "text-davinci-003"
        self.model = ["gpt-3.5-turbo"]
        self.oganization_id = organization_id
        self.search_engine: list[str] = ["google", "bing"]
        self.client: Client = Client()
        self.openai: OpenAI = OpenAI(api_key=self.api_key, organization=self.oganization_id)