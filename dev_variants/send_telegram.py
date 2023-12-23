import asyncio
import os
from telegram import Bot


def main(message: str):
    asyncio.run(telegram_message())


async def telegram_message():
    # Obtain bot_token and chat_id from environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')

    # Multi-line message with HTML formatting
    message = """
https://www.willhaben.at//iad/immobilien/d/mietwohnungen/wien/wien-1140-penzing/wohnung-nahe-allianz-stadion-750037868/
    """

    if bot_token and chat_id:
        print(f"bot_token={bot_token}, chat_id={chat_id}")
        await call_bot(bot_token, chat_id, message)
    else:
        print("Please set the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID environment variables.")


async def call_bot(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    await bot.send_message(chat_id=chat_id, text=message)


if __name__ == "__main__":
    main()