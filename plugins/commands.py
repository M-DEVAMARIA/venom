import os
import asyncio
import logging
import random
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from info import ADMINS
from translation import Translation
logger = logging.getLogger(__name__)

#===================Start Function===================#
@Client.on_message(filters.private & filters.command(['start']))
async def start(client, message):
    buttons = [[
        InlineKeyboardButton('📜 Support Group', url='https://t.me/DxHelpDesk'),
        InlineKeyboardButton('Update Channel ♻️', url='https://t.me/DX_Botz')
        ],[
        InlineKeyboardButton('💡 SouceCode', url='https://github.com/Jijinr/Frwdit-V2'),
        InlineKeyboardButton('String Session 🎻', url ='https://replit.com/@JijinR/PyroSessionString?v=1')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
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
