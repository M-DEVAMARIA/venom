import time
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from translation import Translation
from info import start_uptime


@Client.on_callback_query()
async def cb_handler(client, query):

    if query.data == "close":
        await query.message.delete()
        

    elif query.data == "about":   
        await query.message.edit_text(Translation.START_TXT.format(BOT_USERNAME, DEV_USERNAME, DEV_NAME, BOT_USERNAME), reply_markup=InlineKeyboardMarkup(
               [
                   [
                         InlineKeyboardButton("📦 Source", callback_data="source"),
                         InlineKeyboardButton("Dev 🤠", callback_data="devmuhammed")
                   ],
                   [
                         InlineKeyboardButton("🏕️ Home", callback_data="start"),
                         InlineKeyboardButton("Close 🗑️", callback_data="close")
                   ]
               ]
           )
       )
