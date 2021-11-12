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
async def start(bot, cmd):
    chat_id = cmd.from_user.id
    if not await db.is_user_exist(cmd.from_user.id): 
         await db.add_user(cmd.from_user.id, message.from_user.first_name)
         await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{message.from_user.first_name}](tg://user?id={message.from_user.id}) started @Maxbotassbot !!",
        )
 usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/start subinps"):
        if AUTH_CHANNEL:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await client.send_message(
                        chat_id=cmd.from_user.id,
                        text="Sorry Sir, You are Banned to use me.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                ident, file_id = cmd.text.split("_-_-_-_")
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="**Please Join My Updates Channel to use this Bot!**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Something went Wrong.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('Search again', switch_inline_query_current_chat=''),
                        InlineKeyboardButton('More Bots', url='https://t.me/subin_works/122')
                    ]
                    ]
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    elif len(cmd.command) > 1 and cmd.command[1] == 'subscribe':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ]
                ]
            )
        )
    else:
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
        chat_id=bot.chat.id,
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
async def stats(client, message):
    

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
        text=f"🕐Bot's Uptime: <code>{time_formatter(time.time() - start_uptime)}</code>", 
    
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
