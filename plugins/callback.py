import time
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from translation import Translation
from info import start_uptime, API_KEY
###_____________kanged from pm filter py___________#
from info import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, BUTTON

import re
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster

import random
BUTTONS = {}
BOT = {}

class Callback(object):
    
@Client.on_callback_query()
async def cb_handler(client, query):

    if query.data == "close":
        await query.message.delete()
        

    elif query.data == "about":   
        await query.message.edit_text(Translation.START_TXT.format(API_KEY), reply_markup=InlineKeyboardMarkup(
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
