import os
from pyrogram import filters, Client
from translation import Translation 
from utils import get_poster
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from info import IMDB_TEMPLATE


@Client.on_message(filters.command(['info']))
async def bot_info(client, message):
    
    await client.send_message(
        chat_id=message.chat.id,
       
        text=Translation.ABOUT_TXT,
        parse_mode="html")

@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == "private":
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or ""
        username = message.from_user.username
        dc_id = message.from_user.dc_id or ""
        await message.reply_text(
            f"<b>➲ First Name:</b> {first}\n<b>➲ Last Name:</b> {last}\n<b>➲ Username:</b> {username}\n<b>➲ Telegram ID:</b> <code>{user_id}</code>\n<b>➲ Data Centre:</b> <code>{dc_id}</code>",
            quote=True
        )#/EvaMaria/blob/master/plugins/misc.py#:~:text=setLevel(logging.ERROR)-,%40Client.on_message(filters.command(%27id%27)),),-elif%20chat_type%20in    
@Client.on_message(filters.command(["imdb", 'search']))
async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('Searching ImDB')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("No results Found")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await k.edit('Here is what i found on IMDb', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('Give me a movie / series Name')
     
@Client.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot: Client, query: CallbackQuery):
    i, movie = query.data.split('#')
    poster = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{poster.get('title')}",
                    url=imdb['url'],
                )
            ]
        ]
            
            if poster:
                cap = IMDB_TEMPLATE.format(title = poster['title'], url = poster['url'], year = poster['year'], genres = poster['genres'], plot = poster['plot'], rating = poster['rating'], languages = poster["languages"], runtime = poster["runtime"],  countries = poster["countries"], release_date = poster['release_date'],**locals())
                await message.reply_photo(photo=poster.get("poster"), caption= cap, reply_markup=InlineKeyboardMarkup(buttons))

