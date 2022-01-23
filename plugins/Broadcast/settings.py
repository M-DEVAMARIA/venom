#@crazybot filter bot v2 
import re, asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, FloodWait 
from database.users_db import db
from database.connection_db import active_connection
from database.Settings_db import Database
from translation import Translation
from plugins import VERIFY 
from info import ADMINS
#db = Database()

#db = {}


@Client.on_callback_query(filters.regex(r"open\((.+)\)"), group=2)
async def bot_info(client, message):
    await botsetting_info(client, message , message)
    
@Client.on_message(filters.command(['settings']))
async def botsetting_info(client, msg, call=False):   
    chat = msg.chat.id if not call else msg.message.chat.id
    userid = msg.from_user.id 
    
    st = await client.get_chat_member(chat, userid)
    if not (st.status == "creator") or (st.status == "administrator") or (str(userid) in ADMINS):
        if call:
            msg=msg.message
            return await msg.answer(f"your are not group owner or admin {userid}", show_alert=True)
        else: return print("your not admin")
    k = await settings_extract(msg.message if not call else msg)
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, p, q ,r, btns = k
    settings = await db.find_chat(int(chat))
    pm_file_chat  = settings["configs"].get("pm_fchat", False)#a
    imdb  = settings["configs"].get("imDb", False) #b
    spell  = settings["configs"].get("spellcheck", False)#c
    advance  = settings["configs"].get("advance", False)#d
    autof  = settings["configs"].get("autofilter", False)#e
    autodelete  = settings["configs"].get("delete", False)#f
    welcome  = settings["configs"].get("welcome", False)#g
    protect  = settings["configs"].get("protect", False)#h
    page = settings["configs"]["max_pages"]#i
    delete = settings["configs"]["delete_time"]#j
    cap = "Single" if pm_file_chat else "Double"#k
    imd = "ON ✅" if imdb else "OFF ❌"#l
    spellc = "ON ✅" if spell else "OFF ❌"#m
    autoc = "ON ✅" if autof else "OFF ❌"#n
    deletec = "ON ✅" if autodelete else "OFF ❌"#p
    wlcm = "ON ✅" if welcome else "OFF ❌"#q
    prot = "ON ✅" if protect else "OFF ❌"#r

    buttons = [[
            InlineKeyboardButton("Auto filter", callback_data=f"auto({e}|{chat})"),#e
            InlineKeyboardButton("Spell mode ", callback_data=f"spell({c}|{d}|{chat})")#c,d
            ],[
            InlineKeyboardButton("Button Mode ", callback_data=f"inPM({a}|{chat})"),#a
            InlineKeyboardButton("Imdb ", callback_data=f"imddb({b}|{chat})")#b
            ],[
            InlineKeyboardButton("Filter per page", callback_data=f"pages({page}|{chat})"),#i
            InlineKeyboardButton("Auto delete", callback_data=f"delete({delete}|{autodelete}|{chat})")#j,f
            ],[
            InlineKeyboardButton("welcome", callback_data=f"wlcm({welcome}|{chat})"),#g
            InlineKeyboardButton("protect content", callback_data=f"protect({protect}|{chat})")#h
            ],[
            InlineKeyboardButton("✖️ Close ✖️", callback_data=f"close")
    ]]
    reply_markup = InlineKeyboardMarkup(btns)
    if call:
        await msg.edit_text(reply_markup=reply_markup,text= Translation.SETTINGS_TXT.format(msg.chat.title,autoc,cap,spellc,page,deletec,wlcm,prot,imd),parse_mode="html")
    else:
        await msg.reply_text(reply_markup=reply_markup,text= Translation.SETTINGS_TXT.format(msg.chat.title,autoc,cap,spellc,page,deletec,wlcm,prot,imd),parse_mode="html")

async def settings_extract(msg):
    chat = msg.chat.id
    settings = await db.find_chat(int(chat))
    p  = settings["configs"].get("pm_fchat", False)
    i  = settings["configs"].get("imDb", False) 
    s  = settings["configs"].get("spellcheck", False)
    ad = settings["configs"].get("advance", False)
    af = settings["configs"].get("autofilter", False)
    da = settings["configs"].get("delete", False) 
    we = settings["configs"].get("welcome", False) 
    pr  = settings["configs"].get("protect", False)
    pa = settings["configs"]["max_pages"]
    de = settings["configs"]["delete_time"]
    ca = "Single" if p else "Double"
    im = "ON ✅" if i else "OFF ❌"
    sp = "ON ✅" if s else "OFF ❌"
    au = "ON ✅" if af else "OFF ❌"
    dc = "ON ✅" if da else "OFF ❌"
    wl = "ON ✅" if we else "OFF ❌"
    po = "ON ✅" if pr else "OFF ❌"
    buttons = [[
            InlineKeyboardButton("Auto filter", callback_data=f"auto({af}|{chat})"),#e
            InlineKeyboardButton("Spell mode ", callback_data=f"spell({s}|{ad}|{chat})")#c,d
            ],[
            InlineKeyboardButton("Button Mode ", callback_data=f"inPM({p}|{chat})"),#a
            InlineKeyboardButton("Imdb ", callback_data=f"imddb({i}|{chat})")#b
            ],[
            InlineKeyboardButton("Filter per page", callback_data=f"pages({pa}|{chat})"),#i
            InlineKeyboardButton("Auto delete", callback_data=f"delete({de}|{af}|{chat})")#j,f
            ],[
            InlineKeyboardButton("welcome", callback_data=f"wlcm({we}|{chat})"),#g
            InlineKeyboardButton("protect content", callback_data=f"protect({pr}|{chat})")#h
            ],[
            InlineKeyboardButton("✖️ Close ✖️", callback_data=f"close")
    ]]
    return p,i,s,ad,af,da,we,pr,pa,de,ca,im,sp,au,dc,wl,po, buttons
@Client.on_callback_query(filters.regex(r"inPM\((.+)\)"), group=2)
async def buttons(bot, update: CallbackQuery):
    # button mode callback function
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    st = await bot.get_chat_member(chat_id, user_id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(user_id) in ADMINS):
        return await update.answer("your are not group owner or admin", show_alert=True)

    value, chat_id = re.findall(r"inPM\((.+)\)", query_data)[0].split("|", 1)

    value = True if value=="True" else False
    
    if value:
        buttons= [[
                InlineKeyboardButton("DOUBLE ✅", callback_data=f"set(inPM|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back ", callback_data=f"open({chat_id})")
                ]] 
    else:
        buttons=[[
                InlineKeyboardButton("SINGLE ✅", callback_data=f"set(inPM|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
           
    text=f"<i>Use The Buttons Below To Select filename and  File Size Should Be Shown With Seperate Button or in Single button ... to </i>" 
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
    st = await bot.get_chat_member(chat_id, user_id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(user_id) in ADMINS):
        return await update.answer("your are not group owner or admin", show_alert=True)

    value, chat_id = re.findall(r"imddb\((.+)\)", query_data)[0].split("|", 1)
    
    value = True if value=="True" else False
    if value:
        buttons= [[
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(imddb|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✅", callback_data=f"set(imddb|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<i>Use Below Buttons to Imdb on/off. </i>"
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
    st = await bot.get_chat_member(chat_id, user_id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(user_id) in ADMINS):
        return await update.answer("your are not group owner or admin", show_alert=True)

    value,values, chat_id = re.findall(r"spell\((.+)\)", query_data)[0].split("|", 2)
    
    value = True if value=="True" else False 
    act = "✅" if values=="True" else ""
    acts = "" if values=="True" else "✅"
    if value:
        buttons= [[
                InlineKeyboardButton("ON ✅", callback_data=f"set(spell|True|{chat_id}|{value})"),
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(spell|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton(f"advance {act}", callback_data=f"set(advance|True|{chat_id}|{values})"),
                InlineKeyboardButton(f"normal {acts}", callback_data=f"set(advance|False|{chat_id}|{values})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✅", callback_data=f"set(spell|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<i>Use Below Buttons to Spelling mode on/off and choose mode: advance/normal.</i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
@Client.on_callback_query(filters.regex(r"auto\((.+)\)"), group=2)
async def auto_filter(bot, update: CallbackQuery):
    #auto filter on / off calback function
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    st = await bot.get_chat_member(chat_id, user_id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(user_id) in ADMINS):
        return await update.answer("your are not group owner or admin", show_alert=True)

    value, chat_id = re.findall(r"auto\((.+)\)", query_data)[0].split("|", 1)
    
    value = True if value=="True" else False
    if value:
        buttons= [[
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(auto|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✅", callback_data=f"set(auto|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<i>Use Below Buttons to Auto filter On/Off</i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
@Client.on_callback_query(filters.regex(r"pages\((.+)\)"), group=2)
async def filter_page(bot, update: CallbackQuery):
    #imdb on / off calback function
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    st = await bot.get_chat_member(chat_id, user_id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(user_id) in ADMINS):
        return await update.answer("your are not group owner or admin", show_alert=True)

    count, chat_id = re.findall(r"pages\((.+)\)", query_data)[0].split("|", 1)
    
    buttons= [[
                InlineKeyboardButton("5", callback_data=f"set(pages|5|{chat_id}|{count})"),
                InlineKeyboardButton("7", callback_data=f"set(pages|7|{chat_id}|{count})"),
                InlineKeyboardButton("10", callback_data=f"set(pages|10|{chat_id}|{count})")
                ],[
                InlineKeyboardButton("12", callback_data=f"set(pages|12|{chat_id}|{count})"),
                InlineKeyboardButton("15", callback_data=f"set(pages|15|{chat_id}|{count})"),
                InlineKeyboardButton("20", callback_data=f"set(pages|20|{chat_id}|{count})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
    
                    
    text=f"<i>Choose Your Desired 'Max Filter Count Per Page' For Every Filter Results Shown In group..</i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
@Client.on_callback_query(filters.regex(r"delete\((.+)\)"), group=2)
async def auto_delete(bot, update: CallbackQuery):
    #imdb on / off calback function
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    st = await bot.get_chat_member(chat_id, user_id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(user_id) in ADMINS):
        return await update.answer("your are not group owner or admin", show_alert=True)

    count,value, chat_id = re.findall(r"delete\((.+)\)", query_data)[0].split("|", 2)
    value = True if value=="True" else False
    if value:
         buttons= [[ 
                InlineKeyboardButton("Off ✖️", callback_data=f"set(autodelete|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("🕑 Timer", callback_data="time")
                ],[
                InlineKeyboardButton("1 h ✅"if count=="3600" else "1 h" , callback_data=f"set(delete|3600|{chat_id}|{count})"),
                InlineKeyboardButton("2 h ✅"if count=="7200" else "2 h", callback_data=f"set(delete|7200|{chat_id}|{count})"),
                InlineKeyboardButton("5 h ✅"if count=="10080" else "3 h", callback_data=f"set(delete|10080|{chat_id}|{count})"),
                InlineKeyboardButton("8 h ✅"if count=="28800" else "8 h", callback_data=f"set(delete|28800|{chat_id}|{count})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✔", callback_data=f"set(autodelete|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<b>Use below buttons to select auto delete messages send by venom after desired time</b>\n\n<i>Note:-\n bot only delete message send by user and venom. do not delete other bot messages</i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
@Client.on_callback_query(filters.regex(r"wlcm\((.+)\)"), group=2)
async def wlcm_mode(bot, update: CallbackQuery):
    #wlcm on / off calbackalback function
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    st = await bot.get_chat_member(chat_id, user_id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(user_id) in ADMINS):
        return await update.answer("your are not group owner or admin", show_alert=True)

    value, chat_id = re.findall(r"wlcm\((.+)\)", query_data)[0].split("|", 1)
    
    value = True if value=="True" else False
    if value:
        buttons= [[
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(wlcm|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✅", callback_data=f"set(wlcm|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<i>Use Below Buttons to welcome message on/off. </i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
@Client.on_callback_query(filters.regex(r"protect\((.+)\)"), group=2)
async def protect_mode(bot, update: CallbackQuery):
    #imdb on / off calbackalback function
    query_data = update.data
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    st = await bot.get_chat_member(chat_id, user_id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(user_id) in ADMINS):
        return await update.answer("your are not group owner or admin", show_alert=True)

    value, chat_id = re.findall(r"protect\((.+)\)", query_data)[0].split("|", 1)
    
    value = True if value=="True" else False
    if value:
        buttons= [[
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(protect|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✅", callback_data=f"set(protect|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<i>Use Below Buttons to protect content on/off. </i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
@Client.on_callback_query(filters.regex(r"set\((.+)\)"), group=2)
async def cb_set(bot, update: CallbackQuery):
    query_data = update.data
    chat = update.message.chat.id
    user_id = update.from_user.id
    st = await bot.get_chat_member(chat, user_id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(user_id) in ADMINS):
        return await update.answer("your are not group owner or admin", show_alert=True)

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
    auto_delete = True if prev["configs"].get("delete") == (True or "True") else False
    auto_delete_time = int(prev["configs"].get("delete_time"))
    auto_Filter = True if prev["configs"].get("autofilter") == (True or "True") else False
    pm_file_chat = True if prev["configs"].get("pm_fchat") == (True or "True") else False
    imdb = True if prev["configs"].get("imDb") == (True or "True") else False 
    protect = True if prev["configs"].get("protect") == (True or "True") else False 
    welcome = True if prev["configs"].get("welcome") == (True or "True") else False
    advancespl = True if prev["configs"].get("advance") == (True or "True") else False
    
    if action == "spell": # Scophisticated way 😂🤣
        spellCheck= True if val=="True" else False
    
    elif action == "pages":
        max_pages = int(val)
        
    elif action == "results":
        max_results = int(val)
        
    elif action == "autodelete":
        auto_delete = True if val=="True" else False
    
    elif action == "delete":
        auto_delete_time = int(val)
        
    elif action == "auto":
        auto_Filter = True if val=="True" else False

    elif action =="imddb":
        imdb = True if val=="True" else False

    elif action == "inPM":
        pm_file_chat = True if val=="True" else False 
        
    elif action == "advance":
        advancespl = True if val=="True" else False 
        
    elif action == "protect":
        protect = True if val=="True" else False 
        
    elif action == "wlcm":
        welcome = True if val=="True" else False
        

    new = dict(
        spellcheck=spellCheck,
        max_pages=max_pages,
        max_results=max_results, 
        autofilter=auto_Filter,
        pm_fchat=pm_file_chat,
        delete = auto_delete,
        delete_time = auto_delete_time,
        advance=advancespl,
        protect=protect,
        welcome=welcome,
        imDb=imdb
        
    )
    
    append_db = await db.update_configs(chat, new)
    
    if not append_db:
        text="This group was not in my database.please send command /start in group to add group in db. again you feel this issue send /refresh in group"
        await update.answer(text=text, show_alert=True)
        return
    
    text=f"<b>Your Request Was Updated Sucessfully....</b>"
        
    buttons = [
        [
            InlineKeyboardButton
                (
                    "⬅️ Back", callback_data=f"open({chat_id})"
                ),
            
            InlineKeyboardButton
                (
                    "✖️ Close ✖️", callback_data="close"
                )
        ]
    ]
    
    reply_markup=InlineKeyboardMarkup(buttons)
    
    await update.message.edit_text(
        text, reply_markup=reply_markup, parse_mode="html"
    )
