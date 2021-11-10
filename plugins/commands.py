import os
#sys for restart
import sys
import asyncio
import logging
import random
from database.users_db import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from info import ADMINS, BROADCAST_CHANNEL
from translation import Translation
logger = logging.getLogger(__name__)
LOG_CHANNEL = BROADCAST_CHANNEL
#===================Start Function===================#
@Client.on_message(filters.private & filters.command(['start']))
async def start(bot, message):
    await db.add_user(chat_id)
        await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @{BOT_USERNAME} !!",
        )
    buttons = [[
        InlineKeyboardButton('📜 Support Group', url='https://t.me/DxHelpDesk'),
        InlineKeyboardButton('Update Channel ♻️', url='https://t.me/DX_Botz')
        ],[
        InlineKeyboardButton('💡 inline mode', switch_inline_query_current_chat=''),
        InlineKeyboardButton('String Session 🎻', url ='https://replit.com/@JijinR/PyroSessionString?v=1')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await message.reply_text(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=Translation.START_TXT,
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
