# (c) @mdadmin2
from info import AUTH_CHANNEL, IMDB_TEMPLATE, AUTH_USERS, CUSTOM_FILE_CAPTION, AUTH_GROUPS, start_uptime, IMDB, P_TTI_SHOW_OFF, BROADCAST_CHANNEL as LOG_CHANNEL
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re, time, asyncio
import re
import ast
import pyrogram 
from plugins.__init__ import CALCULATE_TEXT, CALCULATE_BUTTONS, CAPTION, START_BTN, HELP
from translation import Translation 
from plugins.Broadcast import index_files, botsetting_info
from pyrogram.errors import UserNotParticipant, FloodWait, ChatAdminRequired
from database.connection_db import active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from utils import Media, get_filter_results, get_file_details, is_subscribed, get_poster, time_formatter, temp, search_gagala
from database.users_db import db 
from database.filters_db import del_all, find_filter, get_filters 
from .Spell_filter import advancespellmode, normalspellmode
import random
BUTTONS = {}
BOT = {}
SPELL_CHECK = {}
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
BUTTONS1 = InlineKeyboardMarkup([[InlineKeyboardButton('⇚back', callback_data="help")]])
BUTTONS2 = InlineKeyboardMarkup([[InlineKeyboardButton('⇚back', callback_data="help")]])


    
@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        leng = ("total_len")
        google = "https://telegra.ph/file/5c6a4fea12bd4a42d690d.mp4"
        
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"checksub#{file_id}")]
                    )
        else:
            k= await message.reply_video(
            video=google, 
            caption=f"""
Hey {message.from_user.mention},
<b>I couldn't find</b><code> {search}</code><b>? The spelling of the requested movie may not be correct...
So you go to google or imdb and check the spelling of the movie you want.</b>""",
            reply_markup=InlineKeyboardMarkup(
                      [[
                      InlineKeyboardButton("🔍 GOOGLE ", url=f'https://www.google.com/search?q={search}'),
                      InlineKeyboardButton("IMDB 🔎", url=f'https://www.imdb.com/search?q={search}')
                      ]]
                  ),     
            parse_mode="html",
            reply_to_message_id=message.message_id)
            await asyncio.sleep(30)
            await k.delete()
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
            data = BUTTONS[keyword]
            buttons = data['buttons'][0].copy()

            buttons.append(
               [InlineKeyboardButton(text="Next page ⏩",callback_data=f"next_0_{keyword}_{search}")]
            )    
            buttons.append(
               [InlineKeyboardButton(text=f"🗓 1/{data['total']}",callback_data="pages"), InlineKeyboardButton(text=f"🗑️", callback_data="close"), InlineKeyboardButton(text="All", callback_data=f"spcheck#{search}#{message.from_user.id}")]
             )
        else:
            query = search
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="🗓 1/1",callback_data="pages"), InlineKeyboardButton(text=f"🗑️", callback_data="close"), InlineKeyboardButton(text="All", callback_data=f"spcheck#{search}#{message.from_user.id}")]
            )
            
        imdb=await get_poster(search)
        if imdb:
           try:
              cap = IMDB_TEMPLATE.format(title = imdb['title'], url = imdb['url'], year = imdb['year'], genres = imdb['genres'], plot = imdb['plot'], rating = imdb['rating'], languages = imdb["languages"], runtime = imdb["runtime"], countries = imdb["countries"], release_date = imdb['release_date'],**locals())
              await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
           except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
              pic = imdb.get('poster')
              poster = pic.replace('.jpg', "._V1_UX360.jpg")
              await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
           except Exception as e:
              await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(buttons))
        else:
              await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search}</b>", reply_markup=InlineKeyboardMarkup(buttons))
        return 
        
@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming, group=0)
async def give_filter(client, message): 
    group_id = message.chat.id
    name = message.text
    set = await db.find_chat(group_id)
    delete = set["configs"]["delete"]
    delete_time = set["configs"]["delete_time"]
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                          k=await message.reply_text(reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            k=await message.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                    elif btn == "[]":
                        k=await message.reply_cached_media(
                            fileid,
                            caption=reply_text or ""
                        )
                    else:
                        button = eval(btn) 
                        k=await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button)
                        )
                    if delete:
                       await asyncio.sleep(int(delete_time))
                       try:
                          await k.delete(True)
                          await message.delete(True)
                       except Exception as e:
                          return logger.exception(e)
                except Exception as e:
                    logger.exception(e)
                break 
                
    else:
        await group(client, message)   

      
           
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          


@Client.on_callback_query(filters.regex(r"^spolling"))
async def advantage_spoll_choker(bot, query):
    _, user, single, imdb, max_pages, delete, delete_time, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("This not for you", show_alert=True)
    if movie_  == "close_spellcheck":
        return await query.message.delete()
    own = query.from_user.id
    db = await get_poster(query=movie_, id=True)
    b, year= db['title'], db['year']
    b = b.replace("- IMDb", "")
    files = await get_filter_results(b)
    if not files:
        await query.message.edit(f"{b} not found in my database", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f"Request To Add {b} ✅", callback_data=f'request#{b}#{year}')]]))
        return
    message = query.message.reply_to_message or query.message
    chat = message.chat.id
    spell = (b, files)
    if files:
        await query.answer('Checking for Movie in database...')
        try:
          await group(bot, query, spell)
        except:
          await group(bot, query, spell)
                               
@Client.on_callback_query(filters.regex(r"^spcheck"))
async def givess_filter(client: Client, query):
  
    ident, file_id, user = query.data.split("#")
    if int(user) != 0 and query.from_user.id != int(user): 
         return await query.answer("This is not for you ! request your own movie", show_alert=True)
    files = await get_filter_results(file_id)
    if files:
         await query.answer("Sending all files to your pm ! check your pm", show_alert=True)
         for file in files:
            file_id = file.file_id
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
               
                try:  
                    await client.send_cached_media(
                          chat_id=query.from_user.id,
                          file_id=file_id,
                          caption=f_caption,
                          reply_markup=CAPTION,
                          )
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    print(f"Floodwait of {e.x} sec.")
                    await client.send_cached_media(
                          chat_id=query.from_user.id,
                          file_id=file_id,
                          caption=f_caption,
                          reply_markup=CAPTION,
                          )
                except Exception as e:
                    logger.exception(e)
                    return
@Client.on_callback_query(filters.regex(r"^next"))
async def nextfilter(client: Client, query):
            ident, index, keyword, search = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ Back Page", callback_data=f"back_{int(index)+1}_{keyword}_{search}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🗓 {int(index)+2}/{data['total']}", callback_data="pages"), InlineKeyboardButton(text=f"🗑️", callback_data="close"), InlineKeyboardButton(text="All", callback_data=f"spcheck#{search}#{query.from_user.id}")]
                )
                
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ Back Page", callback_data=f"back_{int(index)+1}_{keyword}_{search}"),InlineKeyboardButton("Next Page ⏩", callback_data=f"next_{int(index)+1}_{keyword}_{search}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🗓 {int(index)+2}/{data['total']}", callback_data="pages"), InlineKeyboardButton(text=f"🗑️", callback_data="close"), InlineKeyboardButton(text="All", callback_data=f"spcheck#{search}#{query.from_user.id}")]
                )
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
    
                return

@Client.on_callback_query(filters.regex(r"^back"))                         
async def backfilter(client: Client, query):
            ident, index, keyword, search = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("Next Page ⏩", callback_data=f"next_{int(index)-1}_{keyword}_{search}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🗓 {int(index)}/{data['total']}", callback_data="pages"),InlineKeyboardButton(text=f"🗑️", callback_data="close"), InlineKeyboardButton(text="All", callback_data=f"spcheck#{search}#{query.from_user.id}")]
                )
                
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ Back Page", callback_data=f"back_{int(index)-1}_{keyword}_{search}"),InlineKeyboardButton("Next Page ⏩", callback_data=f"next_{int(index)-1}_{keyword}_{search}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"🗓 {int(index)}/{data['total']}", callback_data="pages"), InlineKeyboardButton(text=f"🗑️", callback_data="close"), InlineKeyboardButton(text="All", callback_data=f"spcheck#{search}#{query.from_user.id}")]
                )
                
                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass 
    if not (clicked == typed):
        return await query.answer("This is not for you ! request your own movie",show_alert=True)
    if (clicked == typed):
        if query.data.startswith("venom"):
            ident, file_id = query.data.split("#")
            configs = await db.find_chat(query.message.chat.id)
            a = configs["configs"]["callback"]
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
                if not a:
                  await query.answer(url=f"https://t.me/{temp.U_NAME}?start={ident}_-_-_-_{file_id}")
                  return
                else:
                    await query.answer('Check PM, I have sent files in pm', show_alert=True)
                    await client.send_cached_media(
                        chat_id=query.from_user.id,
                        file_id=file_id,
                        caption=f_caption,
                        reply_markup=CAPTION,
                        protect_content=True if ident == "venoms" else False
                        )
        if query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("🛑 Join updates channel and press refresh button To get movie",show_alert=True)
                return
            ident, file_id = query.data.split("#")
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
                    f_caption = f"{title}" 
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=CAPTION
                    )
                    
                 

    elif query.data == "pages":
       await query.answer()
    elif query.data == "close":
          try:
            await query.message.reply_to_message.delete()
            await query.message.delete()
          except:
            await query.message.delete()
        
    if query.data == "close":
        await query.message.delete()


    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            grpid  = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Make sure I'm present in your group!!", quote=True)
                    return
            else:
                await query.message.edit_text(
                    "I'm not connected to any groups!\nCheck /connections or connect to any groups",
                    quote=True
                )
                return

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == "creator") or (str(userid) in ADMINS):    
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("You need to be Group Owner or an Auth User to do that!",show_alert=True)

    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == "private":
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in ["group", "supergroup"]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == "creator") or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Thats not for you!!",show_alert=True)


    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]
        
        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "CONNECT"
            cb = "connectcb"
        else:
            stat = "DISCONNECT"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
                InlineKeyboardButton("DELETE", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("BACK", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Group Name : **{title}**\nGroup ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode="md"
        )
        return

    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Connected to **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text('Some error occured!!', parse_mode="md")
        return

    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Disconnected from **{title}**",
                parse_mode="md"
            )
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
        return
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Successfully deleted connection"
            )
        else:
            await query.message.edit_text(
                f"Some error occured!!",
                parse_mode="md"
            )
        return
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "There are no active connections!! Connect to some groups first.",
            )
            return
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = "✅" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Your connected group details ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        
    elif query.data == "start": 
        reply_markup = START_BTN
        await query.message.edit_text(
            text=Translation.START_TXT.format(query.from_user.first_name),
            reply_markup=reply_markup,
            parse_mode='html'
            )
        
    elif query.data == "about": 
        timefmt = time_formatter(time.time() - start_uptime),
        await query.message.edit_text(Translation.ABOUT_TXT.format(timefmt), reply_markup=InlineKeyboardMarkup(
               [[
                         InlineKeyboardButton("📦 Source", url="https://t.me/M_D_movieses"),
                         InlineKeyboardButton("Dev 🤠", url="https://t.me/mdadmin2")
                         ],
                         [
                         InlineKeyboardButton("🏠 Home", callback_data="start"),
                         InlineKeyboardButton("Close 🗑️", callback_data="close")
                   ]] 
                ))
    
    elif query.data == "help":
        await query.message.edit_text(
            text="<b>ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴅᴏᴄᴜᴍᴇɴᴛᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ꜱᴘᴇᴄɪꜰɪᴄ ᴍᴏᴅᴜʟᴇꜱ..  </b>\n",
            reply_markup=HELP,
            parse_mode='html'
            )
 
    
    elif query.data == "autofilter": 
        buttons = [[InlineKeyboardButton('⇚ Back', callback_data='help'), InlineKeyboardButton('Index', callback_data='index')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Translation.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "song": 
        await query.message.edit_text(
            text=Translation.SONG_TXT,
            reply_markup=BUTTONS1,
            parse_mode='html'
        )
    
    elif query.data == "batch": 
        await query.message.edit_text(
            text=Translation.STORE_TXT,
            reply_markup=BUTTONS1,
            parse_mode='html'
        )  
    elif query.data == "telegraph": 
        await query.message.edit_text(
            text=Translation.TELPH_TXT,
            reply_markup=BUTTONS1,
            parse_mode='html'
        )  
     
    elif query.data == "pin": 
        await query.message.edit_text(
            text=Translation.PIN_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        )  
    elif query.data == "clcltr": 
        await query.message.edit_text(
            text=Translation.CALC_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        )  
    elif query.data == "wiki": 
        await query.message.edit_text(
            text=Translation.WIKI_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        )  
    elif query.data == "misc":
        await query.message.edit_text(
            text=Translation.MISC_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        ) 
    elif query.data == "covid":
        await query.message.edit_text(
            text=Translation.COVID_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        ) 
    elif query.data == "imbs": #dont change imbs it cause error in misc imdb|search
        await query.message.edit_text(
            text=Translation.IMDB_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        ) 
    elif query.data == "json":
        await query.message.edit_text(
            text=Translation.JSON_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        ) 
    elif query.data == "tts":
        await query.message.edit_text(
            text=Translation.TTS_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        ) 
    elif query.data == "sett":
        await query.message.edit_text(
            text=Translation.SETT_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        ) 
    elif query.data == "extramod":
        await query.message.edit_text(
            text=Translation.MISC_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        ) 
    
    elif query.data == "connection": 
        await query.message.edit_text(
            text=Translation.CONNECTION_TXT,
            reply_markup=BUTTONS1,
            parse_mode='html'
        ) 
    elif query.data == "manual": 
        await query.message.edit_text(
            text=Translation.MANUALFILTER_TXT,
            reply_markup=BUTTONS1,
            parse_mode='html'
        ) 
    elif query.data == "stats":
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size() 
        monsize = get_size(monsize)
        text=Translation.STATUS_TXT.format(total, users, chats, monsize)
        await query.answer(f"{text}", show_alert=True)
       
    elif query.data == "sets":
        await botsetting_info(client, query, query)
     
    elif query.data == "request":
        await query.answer('Request successful')
        i, movie, year = query.data.split('#')
        await client.send_message(LOG_CHANNNEL,
                                 f'#request\nFrom - {query.message.user_mention}\n\n<b>movie info:</b>\nName: {movie}\nYear: {year}')
                                                                                                                           
    elif query.data == "index":
        await index_files(client, query, query)
        if query.data.startswith('index_cancel'):
            return await query.answer("cancel indexing",show_alert=True)
        
async def chat_settings(client, message):
  if not await db.get_chat(message.chat.id):
      total=await client.get_chat_members_count(message.chat.id)
      await client.send_message(LOG_CHANNEL, Translation.GROUP_LOG.format(message.chat.title, message.chat.id, total, "Unknown"))       
      await db.add_chat(message.chat.id, message.chat.title)
      await asyncio.sleep(3)
  configs = await db.find_chat(message.chat.id)
  a = configs["configs"]["pm_fchat"]#single
  b = configs["configs"]["imDb"]#imdbg
  c = configs["configs"]["spellcheck"]#spcheck
  d = configs["configs"]["autofilter"]#autoftr
  e = configs["configs"]["advance"]#advance
  f = configs["configs"]["max_pages"]#max_pages
  g = configs["configs"]["delete"]#delete
  t = configs["configs"]["delete_time"]#delete_time
  p = configs["configs"]["protect"]
  st = configs["configs"]["spell_template"] 
  im = configs["configs"]["imdb_template"]
  return a, b, c, d, e, f, g, t, p, st, im

async def group(client, message, spell=False):
    btn = []
    chat = message.message.chat.id if spell else message.chat.id
    mess= message.message if spell else message
    configs = await chat_settings(client, mess)
    single, imdbg, spcheck, autoftr, advance, max_pages, delete, delete_time, protect, spelltemp, imdbtemp= configs
   
    if not autoftr:
        return
    if not spell:
        if message.text.startswith("/"): return
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text): return
        if 2 < len(message.text) < 100:    
            searchs = message.text 
            files = await get_filter_results(query=searchs)
            if not files: 
                if spcheck:
                     if advance:
                         return await advancespellmode(message, single, imdbg, max_pages, delete, delete_time)
                     if not advance:
                         return await normalspellmode(message, spelltemp)
                else: return 
    else:
       searchs, files = spell 
       msg = message.message
       message = message.message.reply_to_message
    if files:
       for file in files:
           file_id = file.file_id
           size = f"{get_size(file.file_size)}"
           name = f"{file.file_name}"
           venom= "venoms" if protect=="True" else "venom"                  
           if single:
               btn.append(
                      [InlineKeyboardButton(text=f"{size} {name}", callback_data=f"{venom}#{file_id}")]
                      )
           else:
               btn.append([InlineKeyboardButton(text=f"{name}", callback_data=f"{venom}#{file_id}"),InlineKeyboardButton(text=f"{get_size(file.file_size)}", callback_data=f"{venom}_#{file_id}")])
        
    if not btn:
        return

    if len(btn) > int(max_pages): 
        btns = list(split_list(btn, int(max_pages))) 
        keyword = f"{message.chat.id}-{message.message_id}"
        BUTTONS[keyword] = {
             "total" : len(btns),
             "buttons" : btns
        }
        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()      
        buttons.append(
        [InlineKeyboardButton(text="Next Page ⏩", callback_data=f"next_0_{keyword}_{searchs}")]
        )    
        buttons.append(
        [InlineKeyboardButton(text=f"🗓 1/{data['total']}",callback_data="pages"), InlineKeyboardButton(text=f"🗑️", callback_data="close"), InlineKeyboardButton(text="All", callback_data=f"spcheck#{searchs}#{message.from_user.id}")]
        )
    else:
        buttons = btn
        buttons.append(
            [InlineKeyboardButton(text="🗓 1/1",callback_data="pages"), InlineKeyboardButton(text=f"🗑️", callback_data="close"), InlineKeyboardButton(text="All", callback_data=f"spcheck#{searchs}#{message.from_user.id}")]
            )
    imdb = await get_poster(searchs) if imdbg else None
    if imdb:
        TEMPLATE = IMDB_TEMPLATE if imdbtemp=="None" else imdbtemp 
        if TEMPLATE:
            try:
              cap = TEMPLATE.format(title = imdb['title'], url = imdb['url'], year = imdb['year'], genres = imdb['genres'], plot = imdb['plot'], rating = imdb['rating'], votes = imdb['votes'], languages = imdb["languages"], runtime = imdb["runtime"], countries = imdb["countries"], release_date = imdb['release_date'], director = imdb["director"], writer=imdb["writer"], aka = imdb["aka"], seasons = imdb["seasons"], box_office = imdb['box_office'], localized_title = imdb['localized_title'], kind = imdb['kind'], imdb_id = imdb["imdb_id"], cast = imdb["cast"], producer = imdb["producer"], composer = imdb["composer"], cinematographer = imdb["cinematographer"], music_team = imdb["music_team"], distributors = imdb["distributors"], certificates = imdb["certificates"], **locals())
            except KeyError as e:
              cap = f"<b>Here is What I Found In My Database For Your Query {searchs} \n\n⚠️ Disclaimer:-\nThis group custom IMDb template is in wrong format.used a wrong key {e}. please group owner or admin correct it !</b>" 
        else:
            cap = f"<b>Here is What I Found In My Database For Your Query {searchs} </b>"   
        try:
            k = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            k = await message.reply_photo(photo=poster, caption=cap[:1024], reply_markup=InlineKeyboardMarkup(buttons))
        except Exception as e:
            k = await message.reply_text(cap, reply_markup=InlineKeyboardMarkup(buttons))
    else:
            k = await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {searchs} </b>", reply_markup=InlineKeyboardMarkup(buttons))
         
    if spell:
        await msg.delete(True)
    if delete:
        await asyncio.sleep(int(delete_time))
        try:
           await k.delete(True)
           await message.delete(True)
        except Exception as e:
           await client.send_message(LOG_CHANNEL,text=f"issue on autodelete message\n{e}" )       
           print(f'error in auto delete message {e}')
    return 
    
