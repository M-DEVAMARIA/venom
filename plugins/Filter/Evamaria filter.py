import asyncio
import re
import ast 
import pyrogram 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from utils import is_subscribed, get_poster, search_gagala, temp,Media, get_file_details, get_search_results, get_filter_results, get_file_details
from info import BUTTON, IMDB_TEMPLATE

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}
SPELL_CHECK = {}

#@Client.on_message(filters.group & filters.text & ~filters.edited & filters.incoming)
#async def give_filter(client,message):
        #await auto_filter(client, message)   
@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("okDa", show_alert=True)
    if movie_  == "close_spellcheck":
        return await query.message.delete()
    
    await query.answer('Checking for Movie in database...')
    files = await get_filter_results(movie_)
    message = query.message.reply_to_message or query.message
    if files:
        k = (movie_, files) 
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
        buttons.append(
            [InlineKeyboardButton(text="🗓 1/1",callback_data="pages")]
        )
    
           await query.message.reply_text(text = f"<b>Here is What I Found In My Database For Your Query {search} ‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
     


                    
