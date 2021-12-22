import asyncio
import re
import ast 
import pyrogram 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from utils import is_subscribed, get_poster, search_gagala, temp,Media, get_file_details, get_search_results, get_filter_results, get_file_details
from info import BUTTON, IMDB_TEMPLATE
from plugins.Filter.Pm_filter import SPELL_CHECK
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}


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
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    b = movie_
    await query.answer('Checking for Movie in database...')
    files = await get_filter_results(b)
    if not files:
        return await query.answer("not in not in my database", show_alert=True)
    message = query.message.reply_to_message or query.message
    if files:
        k = (movie_, files) 
        buttons = [
            [
                InlineKeyboardButton(
                    text=f"{file.file_size} {file.file_name}", callback_data=f'files#{file.file_id}'
                ),
            ]
            for file in files
        ]
    return await query.message.reply_text(text = f"<b>Here is What I Found In My Database For Your Query {b} ‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
     


                    
