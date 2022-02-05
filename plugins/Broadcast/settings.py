import re, asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, FloodWait 
from database.users_db import db
from database.connection_db import active_connection
from database.Settings_db import Database
from translation import Translation  
from info import ADMINS, FILLINGS
from plugins import VERIFY 

TEMPLATE ={}
IMDBTEMPLATE ={}

async def admins(bot, msg):
    grpid = await active_connection(str(msg.from_user.id)) if msg.message.chat.type=='private' else msg.message.chat.id
    st = await bot.get_chat_member(grpid , msg.from_user.id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(msg.from_user.id) in (ADMINS, grpid)):
        await update.answer("your are not group owner or admin", show_alert=True)
        return False 
    return True 

@Client.on_message(filters.command(['settings']))
async def botsetting_info(client, msg, call=False): 
    userid= msg.from_user.id
    grpid = await active_connection(str(userid))
    chat_type = msg.message.chat.type if call else msg.chat.type
    if chat_type == "private":
        if grpid is None:
            mssg= msg.message if call else msg
           return await mssg.err("I'm not connected to any groups! /connect to any groups")
        else:
           chat= grpid
    else:
        chat = msg.message.chat.id if call else msg.chat.id
    st = await client.get_chat_member(chat, msg.from_user.id)
    if not (st.status == "creator") or (st.status == "administrator") or (str(userid) in (ADMINS, grpid)):
        if call:
            return await msg.answer(f"your are not group owner or admin {userid}", show_alert=True)
        else: 
            k=await msg.reply_text("your not group owner or admin ")
            await asyncio.sleep(5)
            return await k.delete()
    msg = msg.message if call else msg
    settings = await db.find_chat(int(chat))
    pm_file_chat  = settings["configs"].get("pm_fchat", False)
    imdb  = settings["configs"].get("imDb", False) 
    spell  = settings["configs"].get("spellcheck", False)
    advance  = settings["configs"].get("advance", False)
    autof  = settings["configs"].get("autofilter", False)
    autodelete  = settings["configs"].get("delete", False)
    welcome  = settings["configs"].get("welcome", False)
    protect  = settings["configs"].get("protect", False)
    callback  = settings["configs"].get("callback", False)
    page = settings["configs"]["max_pages"]
    imdb_temp = settings["configs"]["imdb_template"]
    delete = settings["configs"]["delete_time"]
    cap = "Single" if pm_file_chat else "Double"
    imd = "ON ✅" if imdb else "OFF ❌"
    spellc = "ON ✅" if spell else "OFF ❌"
    autoc = "ON ✅" if autof else "OFF ❌"
    deletec = "ON ✅" if autodelete else "OFF ❌"
    wlcm = "ON ✅" if welcome else "OFF ❌"
    prot = "ON ✅" if protect else "OFF ❌"

    buttons = [[
            InlineKeyboardButton("Auto filter", callback_data=f"auto({autof}|{chat})"),
            InlineKeyboardButton("Spell mode ", callback_data=f"spell({spell}|{advance}|{chat})")
            ],[
            InlineKeyboardButton("Button Mode ", callback_data=f"inPM({callback}|{pm_file_chat}|{chat})"),
            InlineKeyboardButton("Imdb ", callback_data=f"imddb({imdb}|{chat})")
            ],[
            InlineKeyboardButton("Filter per page", callback_data=f"pages({page}|{chat})"),
            InlineKeyboardButton("Auto delete", callback_data=f"delete({delete}|{autodelete}|{chat})")
            ],[
            InlineKeyboardButton("welcome", callback_data=f"wlcm({welcome}|{chat})"),
            InlineKeyboardButton("protect content", callback_data=f"protect({protect}|{chat})")
            ],[
            InlineKeyboardButton("✖️ Close ✖️", callback_data=f"close")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    if call:
        await msg.edit_text(reply_markup=reply_markup,text= Translation.SETTINGS_TXT.format(msg.chat.title,autoc,deletec,cap,spellc,page,wlcm,prot,imd),parse_mode="html")
    else:
        await msg.reply_text(reply_markup=reply_markup,text= Translation.SETTINGS_TXT.format(msg.chat.title,autoc,deletec,cap,spellc,page,wlcm,prot,imd),parse_mode="html")
        
@Client.on_callback_query(filters.regex(r"open\((.+)\)"), group=2)
async def bot_info(client, message):
    await botsetting_info(client, message , message)
    
@Client.on_callback_query(filters.regex(r"inPM\((.+)\)"), group=2)
async def buttons(bot, update: CallbackQuery):
    #button mode callback function
    query_data = update.data
    if not await admin(bot, update): return
    value2, value, chat_id = re.findall(r"inPM\((.+)\)", query_data)[0].split("|", 2)

    value = True if value=="True" else False
    values = True if value2=="False" else False
    if value:
        buttons= [[
                InlineKeyboardButton("DOUBLE ✅", callback_data=f"set(inPM|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("Bot Pm ❌"if value2=="True" else "Bot Pm ✅" , callback_data=f"set(inPmcb|{values}|{chat_id}|{value2})")
                ],[
                InlineKeyboardButton("⬅️ Back ", callback_data=f"open({chat_id})")
                ]] 
    else:
        buttons=[[
                InlineKeyboardButton("SINGLE ✅", callback_data=f"set(inPM|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("Bot Pm ❌"if value2=="True" else "Bot Pm ✅" , callback_data=f"set(inPmcb|{values}|{chat_id}|{value2})")
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
    if not await admins(bot, update): return
    value, chat_id = re.findall(r"imddb\((.+)\)", update.data)[0].split("|", 1)
    settings = await db.find_chat(int(chat_id))
    imdb_temp = settings["configs"]["imdb_template"]
    
    value = True if value=="True" else False
    if value:
        buttons= [[
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(imddb|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("IMDB TEMPLATE", callback_data=f"k(k|k|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("default ✅" if imdb_temp=="None" else "default", callback_data=f"set(imdb_template|None|{chat_id}|{value})"),
                InlineKeyboardButton("custom"if imdb_temp=="None" else "custom ✅", callback_data=f"cimdb_template({chat_id}|k)")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✅", callback_data=f"set(imddb|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<i>Use Below Buttons to Imdb on/off and coustomize imdb template. </i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
@Client.on_callback_query(filters.regex(r"spell\((.+)\)"), group=2)
async def cb_show_invites(bot, update: CallbackQuery):
    
    if not await admins(bot, update): return
    
    value,values, chat_id = re.findall(r"spell\((.+)\)", update.data)[0].split("|", 2)
    prev = await db.find_chat(chat_id)
    custom = prev["configs"].get("spell_template")    
    value = True if value=="True" else False 
    act = "✅" if values=="True" else ""
    acts = "" if values=="True" else "✅"
    cact= ""if custom=="None" else "✅"
    if value:
        buttons= [[
                InlineKeyboardButton("ON ✅", callback_data=f"set(spell|True|{chat_id}|{value})"),
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(spell|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton(f"Advance {act}", callback_data=f"set(advance|True|{chat_id}|{values})"),
                InlineKeyboardButton(f"Normal {acts}"if custom=="None" else "Normal", callback_data=f"set(advance|False|{chat_id}|{values})"),
                InlineKeyboardButton(f"Custom {cact}"if values=="False" else "Custom", callback_data=f"custom_info({chat_id}|hi)")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
    else:
        buttons =[[
                InlineKeyboardButton("ON ✅", callback_data=f"set(spell|True|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
                    
    text=f"<i>Use Below Buttons to Spelling mode on/off and choose mode: advance/normal/custom.</i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="html"
    )
@Client.on_callback_query(filters.regex(r"auto\((.+)\)"), group=2)
async def auto_filter(bot, update: CallbackQuery):
    #auto filter on / off calback function
    if not await admins(bot, update): return 
    
    value, chat_id = re.findall(r"auto\((.+)\)", update.data)[0].split("|", 1)
    
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
    #page no set function
    if not await admins(bot, update): return 
    
    count, chat_id = re.findall(r"pages\((.+)\)", update.data)[0].split("|", 1)
    
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
    #auto delete on / off calback function
    if not await admins(bot, update): return
    
    count,value, chat_id = re.findall(r"delete\((.+)\)", update.data)[0].split("|", 2)
    value = True if value=="True" else False
    if value:
         buttons= [[ 
                InlineKeyboardButton("Off ✖️", callback_data=f"set(autodelete|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("🕑 Timer", callback_data="time")
                ],[
                InlineKeyboardButton("1 h ✅"if count=="3600" else "1 h" , callback_data=f"set(delete|3600|{chat_id}|{count})"),
                InlineKeyboardButton("3 h ✅"if count=="10080" else "3 h", callback_data=f"set(delete|7200|{chat_id}|{count})"),
                InlineKeyboardButton("5 h ✅"if count=="18000" else "5 h", callback_data=f"set(delete|10080|{chat_id}|{count})"),
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
    if not await admins(bot, update): return 
    
    value, chat_id = re.findall(r"wlcm\((.+)\)", update.data)[0].split("|", 1)
    prev = await db.find_chat(chat_id)
    st, cb = prev["configs"].get("custom_wlcm"), prev["configs"].get("custom_wlcm_button")
    value = True if value=="True" else False
    if value:
        buttons= [[
                InlineKeyboardButton(" OFF ❌", callback_data=f"set(wlcm|False|{chat_id}|{value})")
                ],[
                InlineKeyboardButton("MESSAGE", callback_data=f"ioo")
                ],[
                InlineKeyboardButton("DEFAULT ✅" if st=='None' else "DEFAULT", callback_data=f"set(custom_wlcm|None|{chat_id}|k)"),InlineKeyboardButton("CUSTOM" if st=='None' else "CUSTOM ✅", callback_data=f"custom_template({chat_id}|wlcm)")
                ],[
                InlineKeyboardButton("BUTTONS", callback_data=f"ioo")
                ],[
                InlineKeyboardButton("DEFAULT ✅" if cb=='None' else "DEFAULT", callback_data=f"set(custom_wlcm_button|None|{chat_id}|k)"), InlineKeyboardButton("CUSTOM" if cb=='None' else "CUSTOM ✅", callback_data=f"custom_button({chat_id}|wlcm)")
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
    #protect content on / off calbackalback function
    
    if not await admins(bot, update): return
    value, chat_id = re.findall(r"protect\((.+)\)", update.data)[0].split("|", 1)
    
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
    
@Client.on_callback_query(filters.regex(r"custom_info\((.+)\)"), group=2)
async def custom_info(bot, update: CallbackQuery):
    #custom info function
    if not await admins(bot, update): return 
    chat_id, i = re.findall(r"custom_info\((.+)\)", update.data)[0].split("|", 1)
    prev = await db.find_chat(chat_id)
    st, cb = prev["configs"].get("spell_template"), prev["configs"].get("custom_button")
    
    buttons= [[
                InlineKeyboardButton("MESSAGE", callback_data=f"ioo")
                ],[
                InlineKeyboardButton("DEFAULT ✅" if st=='None' else "DEFAULT", callback_data=f"set(spell_template|None|{chat_id}|k)"),InlineKeyboardButton("CUSTOM" if st=='None' else "CUSTOM ✅", callback_data=f"custom_template({chat_id}|k)")
                ],[
                InlineKeyboardButton("BUTTONS", callback_data=f"ioo")
                ],[
                InlineKeyboardButton("DEFAULT ✅" if cb=='None' else "DEFAULT", callback_data=f"set(custom_button|None|{chat_id}|k)"), InlineKeyboardButton("CUSTOM" if cb=='None' else "CUSTOM ✅", callback_data=f"custom_button({chat_id}|k)")
                ],[
                InlineKeyboardButton("⬅️ Back", callback_data=f"open({chat_id})")
                ]]
    text=f"<i>Use Below Buttons to set custom message and button</i>"
    reply_markup=InlineKeyboardMarkup(buttons) 
    await update.message.edit_text(text, reply_markup=reply_markup, parse_mode="html")
        
@Client.on_callback_query(filters.regex(r"custom_template\((.+)\)"),group=2)
async def custm_spell(bot, update: CallbackQuery):
    chat, mode  = re.findall(r"custom_template\((.+)\)", update.data)[0].split("|", 1)
    prev = await db.find_chat(chat)
    value = prev["configs"].get("custom_button") if mode=='button'  else prev["configs"].get("spell_template")
    if not await admins(bot, update): return
    text = "please send a custom message to set spell check message\n\nexample:-\n\n<code>hey,{name},i cant find movie with your search {search}</code>" if not mode=='wlcm' else "please send a custom message to set as your group welcome message\n\nexample:-\n\n<code>hey,{name}, welcome to {group}</code>"
    spell = await bot.ask(chat_id= update.from_user.id if update.message.chat.type=='private' else chat,text=text,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('❌ Close ', callback_data=f"cimdb_template({chat}|close)")]]))
    TEMPLATE[chat]= spell.text.html
    texts= f"<code>{spell.text}</code>\n\nconfirm to set this is custom message"
    cat = 'custom_wlcm' if mode=='wlcm' else 'spell_template'
    buttons =[[InlineKeyboardButton("Confirm ✅", callback_data=f"set({cat}|n|{chat}|not)")],[InlineKeyboardButton('❌ Cancel ', callback_data=f"cimdb_template({chat}|close)")]]
    reply_markup=InlineKeyboardMarkup(buttons) 
    await spell.reply_text(texts, reply_markup=reply_markup, parse_mode="html")
    return 

@Client.on_callback_query(filters.regex(r"cimdb_template\((.+)\)"),group=2 )
async def imdb_template(bot, update: CallbackQuery):
    if not await admins(bot, update): return
    chat, current = re.findall(r"cimdb_template\((.+)\)", update.data)[0].split("|", 1)
    prev = await db.find_chat(chat)
    value = prev["configs"].get("imdb_template")
    buttons =[[InlineKeyboardButton("Current", callback_data=f"cimdb_template({chat}|current)"), InlineKeyboardButton("Fillings", callback_data=f"cimdb_template({chat}|Fillings)")]]
    CLOSE =[[InlineKeyboardButton("✖️ close ✖️", callback_data=f"cimdb_template({chat}|close)")]]
    if current=="current":
        return await update.message.reply_text(f"Current:-\n\n{value}"if not value=='None' else "your are not using custom imdb template. your using default imdb template!", reply_markup=InlineKeyboardMarkup(CLOSE))
    if current=="Fillings":
        return await update.message.reply_text(FILLINGS, reply_markup=InlineKeyboardMarkup(CLOSE) )
    if current=="close":
        return await update.message.delete()
    spell = await bot.ask(chat_id=update.from_user.id if update.message.chat.type=='private' else chat,text="<b>please now send a custom imdb template for set as your group imdb template</b>\n\n<i>example:-</i>\n\n<code>🎞Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n📆 Year: <a href={url}/releaseinfo>{year}</a>\n🌟 Rating: <a href={url}/ratings>{rating}</a> / 10 (based on {votes} user ratings.)\n☀️ Languages : <code>{languages}</code>\n📀 RunTime: {runtime} Minutes\n📆 Release Info : {release_date}\n🎛 Countries : <code>{countries}</code></code>",reply_markup=InlineKeyboardMarkup(buttons))
    IMDBTEMPLATE[chat]=spell.text
    buttons =[[InlineKeyboardButton("Confirm ✅", callback_data=f"set(imdb_template|e|{chat}|{value})")],[InlineKeyboardButton('❌ Cancel ', callback_data=f"cimdb_template({chat}|close)")]]    
    await spell.reply_text(f"<code>{spell.text}</code>\n\nconfirm to set this is your group imdb template",reply_markup=InlineKeyboardMarkup(buttons) , parse_mode="html")
    return 

@Client.on_callback_query(filters.regex(r"custom_button\((.+)\)"),group=2)
async def custom_button(bot, update: CallbackQuery):
    chat, mode = re.findall(r"custom_button\((.+)\)", update.data)[0].split("|", 1)
    if not await admins(bot, update): return
    msg = await bot.ask(chat_id=update.from_user.id if update.message.chat.type=='private' else chat,text='send custom button using below Format\n\n<b>Note:</b>\n🛑 Buttons should be properly parsed as markdown format\n\n<b>FORMAT:</b>\n<code>[Venom][buttonurl:https://t.me/venom_moviebot]</code>\n', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('❌ Close ', callback_data=f"cimdb_template({chat}|close)")]]))
    TEMPLATE[chat]= msg.text.html
    cat = 'custom_wlcm_button' if mode=='wlcm' else 'custom_button'
    buttons =[[InlineKeyboardButton("Confirm ✅", callback_data=f"set({cat}|e|{chat}|l)")],[ InlineKeyboardButton('❌ Cancel ', callback_data=f"cimdb_template({chat}|close)")]] 
    await msg.reply_text(f'<code>{msg.text}</code>\n\npress confirm set this your custom button', reply_markup=InlineKeyboardMarkup(buttons), parse_mode="html")
    return 
    
@Client.on_callback_query(filters.regex(r"set\((.+)\)"), group=2)
async def cb_set(bot, update: CallbackQuery):
    # set to db 
    if not await admins(bot, update): return 
    
    action, val, chat_id, curr_val = re.findall(r"set\((.+)\)", update.data)[0].split("|", 3)

    try:
        val, chat_id, curr_val = float(val), int(chat_id), float(curr_val)
    except:
        chat_id = int(chat_id) #please check it in any error
    
    if val == curr_val:
        await update.answer("New Value Cannot Be Old Value...Please Choose Different Value...!!!", show_alert=True)
        return
    
    prev = await db.find_chat(chat_id)

    spellCheck = True if prev["configs"].get("spellcheck") == (True or "True") else False
    max_pages = int(prev["configs"].get("max_pages"))
    max_results = int(prev["configs"].get("max_results"))
    spell_template = prev["configs"].get("spell_template")
    custom_button = prev["configs"].get("custom_button")
    custom_wlcm_button = prev["configs"].get("custom_wlcm_button")
    custom_wlcm = prev["configs"].get("custom_wlcm")
    imdb_template = prev["configs"].get("imdb_template")
    auto_delete = True if prev["configs"].get("delete") == (True or "True") else False
    auto_delete_time = int(prev["configs"].get("delete_time"))
    auto_Filter = True if prev["configs"].get("autofilter") == (True or "True") else False
    pm_file_chat = True if prev["configs"].get("pm_fchat") == (True or "True") else False 
    callback = True if prev["configs"].get("callback") == (True or "True") else False 
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
    
    elif action == "inPmcb":
        callback = True if val=="True" else False
        
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
        
    elif action == "spell_template":
        spell_template  = TEMPLATE.get(chat_id) if not val=="None" else val
    
    elif action == "custom_wlcm":
        custom_wlcm  = TEMPLATE.get(chat_id) if not val=="None" else val
    
    elif action == "custom_button":
        custom_button  = TEMPLATE.get(chat_id) if not val=="None" else val
    
    elif action == "custom_wlcm_button":
        custom_wlcm_button  = TEMPLATE.get(chat_id) if not val=="None" else val
    
    elif action == "imdb_template":
        imdb_template = IMDBTEMPLATE.get(chat_id) if not val=="None" else val
        

    new = dict(
        spellcheck=spellCheck,
        max_pages=max_pages,
        max_results=max_results, 
        autofilter=auto_Filter,
        pm_fchat=pm_file_chat,
        callback=callback,
        delete = auto_delete,
        delete_time = auto_delete_time,
        advance=advancespl,
        protect=protect,
        welcome=welcome,
        custom_wlcm=custom_wlcm,
        spell_template=spell_template,
        custom_wlcm_button=custom_wlcm_button,
        imdb_template=imdb_template,
        custom_button=custom_button,
        imDb=imdb
        
    )
    
    append_db = await db.update_configs(chat_id, new)
    
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
