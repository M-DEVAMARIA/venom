import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.errors import FloodWait
from info import ADMINS
import os
from utils import save_file, temp
import pyromod.listen
logger = logging.getLogger(__name__)
lock = asyncio.Lock()
import re

@Client.on_message(filters.command(['index', 'indexfiles']) & filters.user(ADMINS))
async def index_files(bot, message):
    """Save channel or group files"""
    
        
    
    if lock.locked():
        await query.answer('Wait until previous process complete.')
    else:
        while True:
            last_msg = await bot.ask(text = "Forward me last message of a channel which I should save to my database.\n\nYou can forward posts from any public channel, but for private channels bot should be an admin in the channel.\n\nMake sure to forward with quotes (Not as a copy)", chat_id = message.from_user.id)
            try:
                last_msg_id = last_msg.forward_from_message_id
                if last_msg.forward_from_chat.username:
                    chat_id = last_msg.forward_from_chat.username
                else:
                    chat_id=last_msg.forward_from_chat.id
                await bot.get_messages(chat_id, last_msg_id)
                break
            except Exception as e:
                await last_msg.reply_text(f"This Is An Invalid Message, Either the channel is private and bot is not an admin in the forwarded chat, or you forwarded message as copy.\nError caused Due to <code>{e}</code>")
                continue
    
    msg = await message.reply('Processing...⏳')
    

    await msg.edit(
        "Starting Indexing",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('Cancel', url= f"https://t.me/Maxbotassbot?restart')]]
        )
    )
    
    await index_files_to_db(int(last_msg_id),chat_id, msg, bot)


async def index_files_to_db(last_msg_id,chat_id, msg, bot):
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    async with lock:
        try:
            total = last_msg_id + 1
            current = temp.CURRENT
            temp.CANCEL = False
            while current < total:
                if temp.CANCEL:
                    await msg.edit("Succesfully Cancelled")
                    break
                try:
                    message = await bot.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    message = await bot.get_messages(
                        chat,
                        current,
                        replies=0
                    )
                except Exception as e:
                    logger.exception(e)
                try:
                    for file_type in ("document", "video", "audio"):
                        media = getattr(message, file_type, None)
                        if media is not None:
                            break
                        else:
                            continue
                    media.file_type = file_type
                    media.caption = message.caption
                    aynav, vnay = await save_file(media)
                    if aynav:
                        total_files += 1
                    elif vnay == 0:
                        duplicate += 1
                    elif vnay == 2:
                        errors += 1
                except Exception as e:
                    if "NoneType" in str(e):
                        if message.empty:
                            deleted += 1
                        elif not media:
                            no_media += 1
                        logger.warning("Skipping deleted / Non-Media messages (if this continues for long, use /setskip to set a skip number)")     
                    else:
                        logger.exception(e)
                current += 1
                if current % 20 == 0:
                    can = [[InlineKeyboardButton('Cancel', url= f'https://t.me/Maxbotassbot/restart')]]
                    reply = InlineKeyboardMarkup(can)
                    await msg.edit_text(
                        text=f"Total messages fetched: <code>{current}</code>\nTotal messages saved: <code>{total_files}</code>\nDuplicate Files Skipped: <code>{duplicate}</code>\nDeleted Messages Skipped: <code>{deleted}</code>\nNon-Media messages skipped: <code>{no_media}</code>\nErrors Occured: <code>{errors}</code>",
                        reply_markup=reply)
        except Exception as e:
            logger.exception(e)
            await msg.edit(f'Error: {e}')
        else:
            await msg.edit(f'Succesfully saved <code>{total_files}</code> to dataBase!\nDuplicate Files Skipped: <code>{duplicate}</code>\nDeleted Messages Skipped: <code>{deleted}</code>\nNon-Media messages skipped: <code>{no_media}</code>\nErrors Occured: <code>{errors}</code>')
      
