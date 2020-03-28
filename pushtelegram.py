import requests
from config import TELEGRAM_CREDENTIALS 
import telegram

def push_to_telegram(message, image_path):
    bot = telegram.Bot(TELEGRAM_CREDENTIALS["token"])
    print("Bot Initialized ..")
    # updates  =  bot.get_updates()
    print("Updates OK")
    bot.send_photo(chat_id=TELEGRAM_CREDENTIALS["channel_id"], photo=open(image_path, 'rb'), caption=message, parse_mode=telegram.ParseMode.MARKDOWN)
    print("Daily StatsPhoto Successfully Sent")
    return True


