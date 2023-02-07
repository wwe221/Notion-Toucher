import telegram as tel
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import asyncio
from dotenv import dotenv_values
import notion_touch as nt
config = dotenv_values(".env")

class TelegramBot:
    token = config.get("TELE_TOKEN")
    chat_id = config.get("TELE_CHAT_ID")
    bot = tel.Bot(token= token)
    def sendMessage(message):
        TelegramBot.bot.sendMessage(chat_id=TelegramBot.chat_id, text=message)
    def sendMsg(msg):
        TelegramBot.sendMessage(msg)

def echo(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    if message == "update":
        update.message.reply_text("Updating... Please Wait")
        reply = nt.stock_price_refresh()
    
    update.message.reply_text(reply)
    
updater = Updater(TelegramBot.token)
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.start_polling()
updater.idle()