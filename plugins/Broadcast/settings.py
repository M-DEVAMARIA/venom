#@crazybot filter bot v2 
import re
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, FloodWait 
from database.users_db import db
from database.connection_db import active_connection
from database.Settings_db import Database 
from plugins import VERIFY 
from info import ADMINS
#db = Database()

#db = {}

@Client.on_message(filters.command(['settings']))
async def botsetting_info(client, message):
    chat_id = message.chat.id
    userid = message.from_user.id
    chat_type = message.chat.type
    
    if chat_type == "private":
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Make sure I'm present in your group!!", quote=True)
                return
        else:
            await message.reply_text("I'm not connected to any groups!", quote=True)
            return
    elif chat_type in ["group", "supergroup"]:
        
    else:
        return
    st = await client.get_chat_member(chat_id, userid)
    if not (st.status == "creator") or (str(userid) in ADMINS):
        return
    buttons = [[
            InlineKeyboardButton("🔓 open settings", callback_data=f"open({chat_id})")
            ],[
            InlineKeyboardButton("👤 open in private", callback_data=f"open({chat_id})")
            ],[
            InlineKeyboardButton("✖️ Close", callback_data=f"close")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text="settings here you can coustimise venom ",
        parse_mode="html")
@Client.on_callback_query(filters.regex(r"open\((.+)\)"), group=2)
async def bot_info(bot, update: CallbackQuery):
    query_data = update.data
    chat = update.message.chat.id
    t = "hi"
    settings = await db.find_chat(int(chat))
    pm_file_chat  = settings["configs"].get("pm_fchat", False)
    imdb  = settings["configs"].get("imDb", False) 
    spell  = settings["configs"].get("spellcheck", False)
    advance  = settings["configs"].get("advance", False)
    autof  = settings["configs"].get("autofilter", False)
    cap = "single" if pm_file_chat else "Double"
    imd = "ON ✔️" if imdb else "OFF ✖️"
    spellc = "ON ✔️" if spell else "OFF ✖️"
    autoc = "ON ✔️" if autof else "OFF ✖️"
    
    buttons = [[
            
            InlineKeyboardButton("auto filter", callback_data=f"auto({autof}|{chat})"),
            InlineKeyboardButton("spell mode ", callback_data=f"spell({spell}|{advance}|{chat})")
            ],[
            InlineKeyboardButton("Button Mode ", callback_data=f"inPM({pm_file_chat}|{chat})"),
            InlineKeyboardButton("Imdb ", callback_data=f"imddb({imdb}|{chat})")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.edit_text( 
        reply_markup=reply_markup,
        text= f"<b>coustime your</b> {update.message.chat.title} <b>Group settings.</b>\n\nCurrent settings:\n\n⪼<b>Button:</b> {cap}\n\n⪼<b>Imdb:</b> {imd}\n\n⪼<b>Spelling mode:</b> {spellc}\n\n⪼<b>AutoFilter:</b> {autoc}",
        parse_mode="html")
    
@Client.on_callback_query(filters.regex(r"inPM\((.+)\)"), group=2)
async def buttons(bot, update: CallbackQuery):
    # button mode callback function
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in ADMINS:
        return

    value, chat_id = re.findall(r"inPM\((.+)\)", query_data)[0].split("|", 1)

    value = True if value=="True" else False
    
    if value:
        buttons= [[
                InlineKeyboardButton("DOUBLE ✔️", callback_data=f"set(inPM|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("Back 🔙", callback_data=f"open({chat_id})")
                ]] 
    else:
        buttons=[[
                InlineKeyboardButton("SINGLE  ✔️", callback_data=f"set(inPM|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("Back 🔙", callback_data=f"open({chat_id})")
                ]]
           
    text=f"<i>This Config Will Help You To Enable/Disable File Transfer Through Bot PM Without Redirecting Them To Channel....</i>" 
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
    
@Client.on_callback_query(filters.regex(r"imddb\((.+)\)"), group=2)
async def imdb_mode(bot, update: CallbackQuery):
    #imdb on / off calbackalback function
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in ADMINS:
        return

    value, chat_id = re.findall(r"imddb\((.+)\)", query_data)[0].split("|", 1)
    
    value = True if value=="True" else False
    if value:
        buttons= [[
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(imddb|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("Back 🔙", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✔", callback_data=f"set(imddb|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("Back 🔙", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<i>This Config Will Help You To Show Invitation Link Of All Active Chats Along With The Filter Results For The Users To Join.....</i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
@Client.on_callback_query(filters.regex(r"spell\((.+)\)"), group=2)
async def cb_show_invites(bot, update: CallbackQuery):
    #imdb on / off calback function
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in ADMINS:
        return

    value,values, chat_id = re.findall(r"spell\((.+)\)", query_data)[0].split("|", 2)
    
    value = True if value=="True" else False 
    act = "✅" if values=="True" else ""
    acts = "" if values=="True" else "✅"
    if value:
        buttons= [[
                InlineKeyboardButton("ON ✔", callback_data=f"set(spell|True|{chat_id}|{value})"),
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(spell|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton(f"advance {act}", callback_data=f"set(advance|True|{chat_id}|{values})"),
                InlineKeyboardButton(f"normal {acts}", callback_data=f"set(advance|False|{chat_id}|{values})")
                ],[
                InlineKeyboardButton("Back 🔙", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✔", callback_data=f"set(spell|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("Back 🔙", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<i>This Config Will Help You To Show Invitation Link Of All Active Chats Along With The Filter Results For The Users To Join.....</i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
@Client.on_callback_query(filters.regex(r"auto\((.+)\)"), group=2)
async def auto_filter(bot, update: CallbackQuery):
    #imdb on / off calback function
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in ADMINS:
        return

    value, chat_id = re.findall(r"auto\((.+)\)", query_data)[0].split("|", 1)
    
    value = True if value=="True" else False
    if value:
        buttons= [[
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(auto|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("Back 🔙", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✔", callback_data=f"set(auto|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("Back 🔙", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<i>This Config Will Help You To Show Invitation Link Of All Active Chats Along With The Filter Results For The Users To Join.....</i>"
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
    chat = update.message.chat.id
    user_id = update.from_user.id
    
    if user_id not in ADMINS :
        return

    action, val, chat_id, curr_val = re.findall(r"set\((.+)\)", query_data)[0].split("|", 3)

    try:
        val, chat_id, curr_val = float(val), int(chat_id), float(curr_val)
    except:
        chat_id = int(chat_id) #please check it in any error
    
    if val == curr_val:
        await update.answer("New Value Cannot Be Old Value...Please Choose Different Value...!!!", show_alert=True)
        return
    
    prev = await db.find_chat(chat)

    spellCheck = True if prev["configs"].get("spellcheck") == (True or "True") else False
    max_pages = int(prev["configs"].get("max_pages"))
    max_results = int(prev["configs"].get("max_results"))
    auto_Filter = True if prev["configs"].get("autofilter") == (True or "True") else False
    pm_file_chat = True if prev["configs"].get("pm_fchat") == (True or "True") else False
    imdb = True if prev["configs"].get("imDb") == (True or "True") else False
    advancespl = True if prev["configs"].get("advance") == (True or "True") else False
    
    if action == "spell": # Scophisticated way 😂🤣
        spellCheck= True if val=="True" else False
    
    elif action == "pages":
        max_pages = int(val)
        
    elif action == "results":
        max_results = int(val)
        
    elif action == "auto":
        auto_Filter = True if val=="True" else False

    elif action =="imddb":
        imdb = True if val=="True" else False

    elif action == "inPM":
        pm_file_chat = True if val=="True" else False  
    elif action == "advance":
        advancespl = True if val=="True" else False
        

    new = dict(
        spellcheck=spellCheck,
        max_pages=max_pages,
        max_results=max_results,
        autofilter=auto_Filter,
        pm_fchat=pm_file_chat,
        advance=advancespl,
        imDb=imdb
        
    )
    
    append_db = await db.update_configs(chat, new)
    
    if not append_db:
        text="Something Wrong Please Check Bot Log For More Information...."
        await update.answer(text=text, show_alert=True)
        return
    
    text=f"Your Request Was Updated Sucessfully....\nNow All Upcoming Results Will Show According To This Settings..."
        
    buttons = [
        [
            InlineKeyboardButton
                (
                    "Back 🔙", callback_data=f"open({chat_id})"
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
