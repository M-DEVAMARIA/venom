import asyncio
import re
import ast 
import pyrogram 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters 
from database.users_db import db
from utils import is_subscribed, get_poster, search_gagala, temp,Media, get_file_details, get_search_results, get_filter_results, get_file_details, list_to_str
from typing import Tuple, List, Optional
from info import IMDB_TEMPLATE
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


BUTTONS = {}
BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)]\[buttonurl:/{0,2}(.+?)(:same)?])")


async def advancespellmode(message, single, imdbg, max_pages, delete, delete_time):
    search = message.text
    user = message.from_user.id 
    search = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)", "", search, flags=re.IGNORECASE)
    search = search.strip()
    movies = await get_poster(search, bulk=True)
    if not movies:
        return await message.reply_text(f"i couldn't find anything with {search}")
    btn = [
            [
              InlineKeyboardButton(
              text=f"{movie.get('title')}",
              callback_data=f"spolling#{user}#{single}#{imdbg}#{max_pages}#{delete}#{delete_time}#{movie.movieID}",
              )
             ]
             for movie in movies
          ]
    btn.append([InlineKeyboardButton(text="close", callback_data=f'spolling#{user}#close_spellcheck#i#i#i#i#')])
    k =await message.reply_text(f"hey {message.from_user.mention},\n\nI couldn't find anything related to thatDid you mean any one of these?", reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(22)
    await k.delete()
    return 

async def normalspellmode(message, template):
    search = message.text
    info = await db.find_chat(message.chat.id)
    button = info["configs"]["custom_button"]
    buttons = parse_buttons(button)
    reply_button = None#InlineKeyboardMarkup(buttons) if buttons!='[]' else InlineKeyboardMarkup([[InlineKeyboardButton("🔍 GOOGLE ", url=f'https://www.google.com/search?q={search}'), InlineKeyboardButton("IMDB 🔎", url=f'https://www.imdb.com/search?q={search}')]])
    spf = await message.reply_text(
    text=f"<code>Sorry {button} {message.from_user.mention},\n\n<b>I didn't get any files matches with {search}, maybe your spelling is wrong. try sending the proper movie name...</b></code>" if template=="None" else template.format(name=message.from_user.mention, search=search),
    reply_markup=reply_button,
    parse_mode="html",
    reply_to_message_id=message.message_id)
    await asyncio.sleep(22)
    await spf.delete()
    return 


def parse_buttons(text):
    buttons =[]
    for match in BTN_URL_REGEX.finditer(text):
        n_escapes = 0
        to_check = match.start(1) - 1
        while to_check > 0 and text[to_check] == "\\":
            n_escapes += 1
            to_check -= 1

        if n_escapes % 2 == 0:
            if bool(match.group(4)) and buttons:
                buttons[-1].append(InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(3).replace(" ", "")))
            else:
                buttons.append([InlineKeyboardButton(
                    text=match.group(2),
                    url=match.group(3).replace(" ", ""))])
    return buttons

