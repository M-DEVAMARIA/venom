import os
#sys for restart the bot
import sys
import asyncio, time
import logging
import random
from database.users_db import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from pyrogram import Client, filters
from info import ADMINS, BROADCAST_CHANNEL, PHOTO, start_uptime
from translation import Translation 
logger = logging.getLogger(__name__)
LOG_CHANNEL = BROADCAST_CHANNEL
#===================Start Function===================#
@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    chat_id = message.from_user.id
    if not await db.is_user_exist(message.from_user.id): 
         await db.add_user(message.from_user.id, message.from_user.first_name)
         await client.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @Maxbotassbot !!",
        )
    buttons = [[
        InlineKeyboardButton('📜 Support Group', url='https://t.me/DxHelpDesk'),
        InlineKeyboardButton('Update Channel ♻️', url='https://t.me/DX_Botz')
        ],[
        InlineKeyboardButton('💡 inline mode', switch_inline_query_current_chat=''),
        InlineKeyboardButton('String Session 🎻', url ='https://replit.com/@JijinR/PyroSessionString?v=1')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await client.send_photo(
        photo=random.choice(PHOTO),
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        caption=Translation.START_TXT,
        parse_mode="html")

 #==================about Function====================#
@Client.on_message(filters.command(['about']))
async def bot_info(client, message):
    buttons = [[
            InlineKeyboardButton('Update Channel', url='https://t.me/subin_works'),
            InlineKeyboardButton('Source Code', url='https://github.com/subinps/Media-Search-bot')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=Translation.ABOUT_TXT,
        parse_mode="html")
    
 #==================restart Function====================#

@Client.on_message(filters.private & filters.command(['restart']))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>Trying to restarting.....</i>"
    )
    await asyncio.sleep(2)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)

#qq feature____________#
@Client.on_message(filters.private & filters.command(['stats']))
async def stats(Client, message):
    

    text=f"<b><u>🤖Bot's Status</u></b>\n"
    text+=f"\n🕐Bot's Uptime: <code>{time_formatter(time.time() - start_uptime)}</code>\n"
    text+=f"\nBot Funtion: <b><>Auto Filter & Manual Filters</b>"

    buttons = [[
         InlineKeyboardButton("🔙 Back", url= f"https://t.me/mdmovies"),
         InlineKeyboardButton("Close 🔐", url= f"https://t.me/mdmovieses")
         ]]    
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=🕐Bot's Uptime: <code>{time_formatter(time.time() - start_uptime)}</code>, hh
    
        parse_mode="html")


def time_formatter(seconds: float) -> str:
    """ 
    humanize time 
    """
    minutes, seconds = divmod(int(seconds),60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s") if seconds else "")
    return tmp
