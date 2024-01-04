# instance for bot
import telebot
from telebot.async_telebot import AsyncTeleBot

from vabot.config import BaseConfig as cfg
from vabot.chatbot import ChatBotAI

bot = AsyncTeleBot(token=cfg.TELEGRAM_API_KEY) # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    await bot.reply_to(message, """\
Hi there, I am EchoBot.
I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
""")


# command for bot
@bot.message_handler(commands=['search'])
async def search_command(message):
    search = ChatBotAI(api_key=cfg.API_KEY, organization_id=cfg.ORGANIZATION_ID)
    query = message.text.replace("search", "")
    await bot.reply_to(message, search.search_with_bing(query=query))