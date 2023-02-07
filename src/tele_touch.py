import telegram as tel
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import asyncio
from dotenv import dotenv_values
import notion_touch as nt

config = dotenv_values(".env")
token:str = config.get("TELE_TOKEN")
chat_id:str = config.get("TELE_CHAT_ID")

def echo(update: Update, context: CallbackContext) -> None:
    message = update.message.text
    if message == "update":        
        reply = nt.stock_price_refres()
    update.message.reply_text(reply)
    
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def get_command(update, context):
    show_list = []
    show_list.append(InlineKeyboardButton("update", callback_data="update")) 
    # show_list.append(InlineKeyboardButton("add", callback_data="add"))
    show_list.append(InlineKeyboardButton("cancel", callback_data="cancel"))
    show_markup = InlineKeyboardMarkup(build_menu(show_list, len(show_list) - 1)) # make markup
    update.message.reply_text("무엇을 할까요", reply_markup=show_markup)

def callback_get(update: Update, context: CallbackContext):
    selected = update.callback_query.data
    print("callback - " + selected)
    if selected == "update":        
        edit_context_message(update, context, "Updating... Please Wait")
        replyMsg = nt.stock_price_refresh()
        edit_context_message(update, context, replyMsg)
    else:
        edit_context_message(update, context, "{}이(가) 선택되었습니다".format(selected))
            
def edit_context_message(update, context, new_text):
    context.bot.edit_message_text(
            text=new_text,
            chat_id=update.callback_query.message.chat_id,
            message_id=update.callback_query.message.message_id
        )

get_handler = CommandHandler('get', get_command)
updater = Updater(token)
updater.dispatcher.add_handler(get_handler)
updater.dispatcher.add_handler(CallbackQueryHandler(callback_get))
dispatcher = updater.dispatcher
dispatcher.add_handler(MessageHandler(Filters.text, echo))
updater.start_polling()
updater.idle()