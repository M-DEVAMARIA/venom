import asyncio
import re
import ast 
import pyrogram 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
from utils import is_subscribed, get_poster, search_gagala, temp,Media, get_file_details, get_search_results, get_filter_results, get_file_details
from info import IMDB_TEMPLATE
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

BUTTONS = {}


async def advancespellmode(message, single, imdbg, max_pages, delete, delete_time):
 #   search = []
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
    button = await custombutton(message)
    spf = await message.reply_text(
    text=f"<code>Sorry {message.from_user.mention},\n\n<b>I didn't get any files matches with {search}, maybe your spelling is wrong. try sending the proper movie name...</b></code>" if template=="None" else template.format(name=message.from_user.mention, search=search),
    reply_markup= button,#InlineKeyboardMarkup(
           # [[  
          #   InlineKeyboardButton("🔍 GOOGLE ", url=f'https://www.google.com/search?q={search}'),
          #   InlineKeyboardButton("IMDB 🔎", url=f'https://www.imdb.com/search?q={search}')
          #  ]]
       #  ),     
    parse_mode="html",
    reply_to_message_id=message.message_id)
    await asyncio.sleep(22)
    await spf.delete()
    return
   
async def custombutton(msg):
   # db = await db.find_chat(msg.chat.id)
    #buttons = db["settings"]["buttons"]
    button = []
    buttons = "venom - https://t.me/venom_moviebot"
    button.append(buttons)
    print(button)
    if not buttons:
        return False 
    name, url = buttons.split('-')
    if name and url:
         reply_markup=InlineKeyboardMarkup(
            [[  
             InlineKeyboardButton(f"{name}", url= url)
            ]])
         return reply_markup
    
