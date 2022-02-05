import os 
from asyncio import sleep as rest
from database.users_db import db
from pyrogram import filters, Client
from translation import Translation 
from utils import get_poster
from plugins.Filter.Spell_filter import parse_buttons
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from info import IMDB_TEMPLATE, BROADCAST_CHANNEL as LOG_CHANNEL

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, cmd):
    if not await db.get_chat(cmd.chat.id):
        total=await bot.get_chat_members_count(cmd.chat.id)
        channel_id = cmd.chat.id
        group_id = cmd.chat.id
        title = cmd.chat.title
        await db.add_chat(cmd.chat.id, cmd.chat.title)
        await bot.send_message(LOG_CHANNEL, Translation.GROUP_LOG.format(cmd.chat.title,cmd.chat.id,total,"Unknown"))
        
    set=await db.find_chat(cmd.chat.id) 
    if set:
        try:
           w, msg = set["configs"]["welcome"], set["configs"]["custom_wlcm"]
           btn = parse_buttons(set["configs"]["custom_wlcm_button"])
           if not w: return
        except:
           pass
    for u in cmd.new_chat_members:
        try:
            k = await cmd.reply(text=f"<b>Hey , {u.mention},\nWelcome to {cmd.chat.title}</b>" if msg=='None' else msg.format(name=u.mention, group=cmd.chat.title)), reply_markup='None' if btn=='None' else InlineKeyboardMarkup(btn))
        except:
            return 
        if k:
           try:
             await rest(30)
             await k.delete(True)
             return
           except Exception as e:
             return print(f"error in auto delete message {e}")

@Client.on_message(filters.command(['info']))
async def bot_info(client, message):
    
    await client.send_message(
        chat_id=message.chat.id,
       
        text=Translation.ABOUT_TXT,
        parse_mode="html")

@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    user_id = message.chat.id
    first = message.from_user.first_name
    last = message.from_user.last_name or ""
    username = message.from_user.username
    dc_id = message.from_user.dc_id or ""
    if chat_type == "private": 
        await message.reply_text(
            f"<b>➲ First Name:</b> {first}\n<b>➲ Last Name:</b> {last}\n<b>➲ Username:</b> {username}\n<b>➲ Telegram ID:</b> <code>{user_id}</code>\n<b>➲ Data Centre:</b> <code>{dc_id}</code>",
            quote=True 
        )
    if chat_type in ["group", "supergroup"]:
         k = ""
         k+= f"<b>➲ User ID:</b> <code>{message.from_user.id}</code>\n<b>➲ Chat ID:</b> <code>{message.chat.id}</code>\n"
            
         if message.reply_to_message:
            k+= f"<b>➲ Replied User ID:</b> <code>{message.reply_to_message.from_user.id if message.reply_to_message.from_user else 'Anonymous'}</code>"
         await message.reply_text(
             k,
             quote=True
         )
            
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
     
@Client.on_callback_query(filters.regex(r'imdb'))
async def imdb_callback(bot: Client, query: CallbackQuery):
    i, movie = query.data.split('#')
    poster = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{poster.get('title')}",
                    url=poster['url'],
                )
            ]
        ]
  
    if poster:
        await query.message.reply_photo(photo=poster.get("poster"), caption= f"**🎬 Title:**{poster.get('title')}\n**🎭 Genres:** {poster.get('genres')}\n**📆 Year:** <a href={poster['url']}/releaseinfo>{poster.get('year')}</a>\n**🌟Rating:** <a href={poster['url']}/ratings>{poster.get('rating')}</a> / 10\n**" , reply_markup=InlineKeyboardMarkup(btn))
    await query.message.delete()
