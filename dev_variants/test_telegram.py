from telegram import Bot


def send_multi_line_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    # Using the HTML mode to allow formatting of the message
    bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')


if __name__ == "__main__":
    # Replace 'YOUR_BOT_TOKEN' with the actual token you obtained from the BotFather
    bot_token = 'YOUR_BOT_TOKEN'

    # Replace 'YOUR_CHAT_ID' with the chat ID of the user or group you want to send the message to
    chat_id = 'YOUR_CHAT_ID'

    # Multi-line message with HTML formatting
    message = """
    This is a multi-line message sent from a Python script.
    """

    send_multi_line_message(bot_token, chat_id, message)
