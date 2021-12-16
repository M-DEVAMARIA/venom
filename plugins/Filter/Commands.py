import os, re
import base64
#sys for restart the bot
import sys
import asyncio, time
import logging
import random
from plugins.__init__ import CAPTION, CALCULATE_TEXT, CALCULATE_BUTTONS, START_BTN
from utils import Media, get_file_details, get_size, time_formatter, temp
from database.users_db import db
from pyrogram.types import Message, User, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from pyrogram import Client, filters
from info import ADMINS, BROADCAST_CHANNEL, PHOTO, start_uptime, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
from translation import Translation 
from pyrogram import StopPropagation
from pyrogram.errors import UserNotParticipant
logger = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
#from database.Settings_db import Database
LOG_CHANNEL = BROADCAST_CHANNEL
OWNER_ID = "1411070838"
DB_CHANNEL_ID = os.environ.get("DB_CHANNEL_ID",'-100')
#dbs = Database
IS_PRIVATE = os.environ.get("IS_PRIVATE",False) 

#===================Start Function===================#
@Client.on_message(filters.command("start"))
async def gstart(bot, cmd): 
    if cmd.chat.type in ['group', 'supergroup']:
        buttons = [
            [
                InlineKeyboardButton('🤖VENOM Updates', url='https://t.me/joinchat/MtD0j4FOqbFmYmE1')
            ],
            [
                InlineKeyboardButton('ℹ️ Help', url=f"https://t.me/venom_moviebot?start=help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await cmd.reply(Translation.START_TXT.format(cmd.chat.title), reply_markup=reply_markup)
        await asyncio.sleep(2) 
        if not await db.get_chat(cmd.chat.id):
            total=await bot.get_chat_members_count(cmd.chat.id)
            channel_id = cmd.chat.id
            group_id = cmd.chat.id
            title = cmd.chat.title
            await db.add_chat(cmd.chat.id, cmd.chat.title)
       
            await bot.send_message(
                LOG_CHANNEL, 
                f"#NEWGROUP: \n\nNew group =  [{cmd.chat.title}] id={cmd.chat.id} members = [{total}] started @{temp.U_NAME} !!",)
      
        return 
    
    if not await db.is_user_exist(cmd.from_user.id): 
        await db.add_user(cmd.from_user.id, cmd.from_user.first_name)
        await bot.send_message(
            LOG_CHANNEL,
            f"#NEWUSER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started @{temp.U_NAME} !!",
        ) 
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/start subinps"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
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
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=CAPTION
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
        return await start(bot, cmd)
else:

           
        await cmd.reply_photo(
        photo=random.choice(PHOTO), 
        caption=Translation.START_TXT.format(cmd.from_user.first_name),
        parse_mode="html",
        reply_markup= START_BTN)
        
#===================file store start =================#
#@Client.on_message(filters.command(['start']))
async def start(c, m):
    if len(m.command) > 1: # sending the stored file
        try:
            m.command[1] = await decode(m.command[1])
        except:
            pass

        if 'batch_' in m.command[1]: 
            cmd, chat_id, message = m.command[1].split('_')
            string = await c.get_messages(int(chat_id), int(message)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(message))
        
            
            if string.empty:
                owner = await c.get_users(int(OWNER_ID))
                return await m.reply_text(f"🥴 Sorry bro your file was deleted by file owner or bot owner\n\nFor more help contact my owner 👉 {owner.mention(style='md')}")
            message_ids = (await decode(string.text)).split('-')
            for msg_id in message_ids:
                msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))

                if msg.empty:
                    owner = await c.get_users(int(OWNER_ID))
                    return await m.reply_text(f"🥴 Sorry bro your file was deleted by file owner or bot owner\n\nFor more help contact my owner 👉 {owner.mention(style='md')}")

                await msg.copy(m.from_user.id)
                await asyncio.sleep(1)
            return

        chat_id, msg_id = m.command[1].split('_')
        msg = await c.get_messages(int(chat_id), int(msg_id)) if not DB_CHANNEL_ID else await c.get_messages(int(DB_CHANNEL_ID), int(msg_id))

        if msg.empty:
            return await send_msg.edit(f"🥴 Sorry bro your file was deleted by file owner or bot owner\n\nFor more help contact my owner 👉 {owner.mention(style='md')}")
        
        caption = f"{msg.caption.markdown}\n\n\n" if msg.caption else ""
        
        await msg.copy(m.from_user.id, caption=caption)
    

 #==================about Function====================#
@Client.on_message(filters.command(['about']))
async def bot_info(client, message):
    buttons = [[
            InlineKeyboardButton("🤖 Venom UPDATES", url=f"https://t.me/joinchat/EOI9s4lc00cyOTI1")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text=Translation.ABOUT_TXT,
        parse_mode="html")
    
 #==================restart Function====================#

@Client.on_message(filters.command('restart')& filters.user(ADMINS))
async def restart(client, message):
    msg = await message.reply_text(
        text="<i>Trying to restarting.....</i>"
    )
    await asyncio.sleep(2)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)

#qq feature____________#
@Client.on_message(filters.command('stats') & filters.user(ADMINS))
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
        text=f"🕐Bot's Uptime: <code>{time_formatter(time.time() - start_uptime)}</code>\n",
        

        parse_mode="html")

 #_______________logs__________________#

@Client.on_message(filters.command('logger') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))
    

@Client.on_message((filters.command(["report"]) | filters.regex("@admins") | filters.regex("@admin")) & filters.group)
async def report(bot, message):
    if message.reply_to_message:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        admins = await bot.get_chat_members(chat_id=chat_id, filter="administrators")
        success = False
        report = f"Reporter : {mention} ({reporter})" + "\n"
        report += f"Message : {message.reply_to_message.link}"
        for admin in admins:
            try:
                reported_post = await message.reply_to_message.forward(admin.user.id)
                await reported_post.reply_text(
                    text=report,
                    chat_id=admin.user.id,
                    disable_web_page_preview=True
                )
                success = True
            except:
                pass
        if success:
            await message.reply_text("**Reported to Admins!**")

#________________________________calculator____________________#
@Client.on_message(filters.command(["calc", "calculate", "calculator"]))
async def calculate(bot, update):
    await update.reply_text(
        text=CALCULATE_TEXT,
        reply_markup=CALCULATE_BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )
       
async def decode(base64_string):
    base64_bytes = base64_string.encode("ascii")
    string_bytes = base64.b64decode(base64_bytes) 
    string = string_bytes.decode("ascii")
    return string
