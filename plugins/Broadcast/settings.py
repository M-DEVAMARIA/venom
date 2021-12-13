#@crazybot filter bot v2 
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, FloodWait
from database.Settings_db import Database 
from plugins import VERIFY 
from info import ADMINS
db = Database()



@Client.on_message(filters.command(['settings']))
async def botsetting_info(client, message):
    chat_id = message.chat.id
    buttons = [[
            InlineKeyboardButton("open settings", callback_data=f"open({chat_id})")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text="hi, how are you ",
        parse_mode="html")
@Client.on_callback_query(filters.regex(r"open\((.+)\)"), group=2)
async def bot_info(bot, update: CallbackQuery):
    query_data = update.data
    chat_id = update.message.chat.id
    settings = await db.find_chat(int(chat_id))
    pm_file_chat  = settings["configs"].get("pm_fchat", False)
    buttons = [[
            InlineKeyboardButton("open settings", callback_data=f"inPM({pm_file_chat}|{chat_id})")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.edit_text( 
        reply_markup=reply_markup,
        text="hi, how are you ",
        parse_mode="html")
    
@Client.on_callback_query(filters.regex(r"inPM\((.+)\)"), group=2)
async def cb_pm_file(bot, update: CallbackQuery):
    """
    A Callback Funtion For Enabling Or Diabling File Transfer Through Bot PM
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in ADMINS.get(str(chat_id)):
        return

    value, chat_id = re.findall(r"inPM\((.+)\)", query_data)[0].split("|", 1)

    value = True if value=="True" else False
    
    if value:
        buttons= [
            [
                InlineKeyboardButton
                    (
                        "Disable ❎", callback_data=f"set(inPM|False|{chat_id}|{value})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "Back 🔙", callback_data=f"config({chat_id})"
                    )
            ]
        ]
    
    else:
        buttons =[
            [
                InlineKeyboardButton
                    (
                        "Enable ✅", callback_data=f"set(inPM|True|{chat_id}|{value})"
                    )
            ],
            [
                InlineKeyboardButton
                    (
                        "Back 🔙", callback_data=f"config({chat_id})"
                    )
            ]
        ]
    
    text=f"<i>This Config Will Help You To Enable/Disable File Transfer Through Bot PM Without Redirecting Them To Channel....</i>"
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
    
@Client.on_callback_query(filters.regex(r"set\((.+)\)"), group=2)
async def cb_set(bot, update: CallbackQuery):
    """
    A Callback Funtion Support For config()
    """
    global VERIFY
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in ADMINS.get(str(chat_id)):
        return

    action, val, chat_id, curr_val = re.findall(r"set\((.+)\)", query_data)[0].split("|", 3)

    try:
        val, chat_id, curr_val = float(val), int(chat_id), float(curr_val)
    except:
        chat_id = int(chat_id)
    
    if val == curr_val:
        await update.answer("New Value Cannot Be Old Value...Please Choose Different Value...!!!", show_alert=True)
        return
    
    prev = await db.find_chat(chat_id)

    accuracy = float(prev["configs"].get("accuracy", 0.80))
    max_pages = int(prev["configs"].get("max_pages"))
    max_results = int(prev["configs"].get("max_results"))
    max_per_page = int(prev["configs"].get("max_per_page"))
    pm_file_chat = True if prev["configs"].get("pm_fchat") == (True or "True") else False
    show_invite_link = True if prev["configs"].get("show_invite_link") == (True or "True") else False
    
    if action == "accuracy": # Scophisticated way 😂🤣
        accuracy = val
    
    elif action == "pages":
        max_pages = int(val)
        
    elif action == "results":
        max_results = int(val)
        
    elif action == "per_page":
        max_per_page = int(val)

    elif action =="showInv":
        show_invite_link = True if val=="True" else False

    elif action == "inPM":
        pm_file_chat = True if val=="True" else False
        

    new = dict(
        accuracy=accuracy,
        max_pages=max_pages,
        max_results=max_results,
        max_per_page=max_per_page,
        pm_fchat=pm_file_chat,
        show_invite_link=show_invite_link
    )
    
    append_db = await db.update_configs(chat_id, new)
    
    if not append_db:
        text="Something Wrong Please Check Bot Log For More Information...."
        await update.answer(text=text, show_alert=True)
        return
    
    text=f"Your Request Was Updated Sucessfully....\nNow All Upcoming Results Will Show According To This Settings..."
        
    buttons = [
        [
            InlineKeyboardButton
                (
                    "Back 🔙", callback_data=f"config({chat_id})"
                ),
            
            InlineKeyboardButton
                (
                    "Close 🔐", callback_data="close"
                )
        ]
    ]
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )
