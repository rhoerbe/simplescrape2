import asyncio
import os
import sys
from dotenv import load_dotenv
from telegram import Bot, error

load_dotenv()


def main(message: str):
    asyncio.run(telegram_message(message))


async def telegram_message(message: str):
    # Obtain bot_token and chat_id from environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if bot_token and chat_id:
        #print(f"bot_token={bot_token}, chat_id={chat_id}")
        await call_bot(bot_token, chat_id, message)
    else:
        raise Exception("Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")


async def call_bot(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except error.BadRequest as e:
        print(f"\nError during Telegram send.message (chat_id = {chat_id})\n{str(e)}\n", file=sys.stderr)
