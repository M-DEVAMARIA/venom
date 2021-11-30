#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, IMDB_TEMPLATE, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, BUTTON, start_uptime, IMDB
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re, time, asyncio
import re
import ast
import pyrogram 
from plugins.__init__ import CALCULATE_TEXT, CALCULATE_BUTTONS, button
from translation import Translation
from pyrogram.errors import UserNotParticipant
from database.connection_db import active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from utils import Media, get_filter_results, get_file_details, is_subscribed, get_poster, time_formatter, temp, search_gagala
from database.users_db import db 
from database.filters_db import del_all, find_filter, get_filters 
import random
BUTTONS = {}
BOT = {}
SPELL_CHECK = {}
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton('⇚back', callback_data="help")]])
BUTTONS2 = InlineKeyboardMarkup([[InlineKeyboardButton('⇚back', callback_data="extra")]])


    
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
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            spf = await message.reply_video(
        
            video=google, 
            caption=f"""
👋Hey {message.from_user.mention}
If this movie is not in our database you will not get that movie..
Otherwise, the spelling of the name of the requested movie may not be correct...
So you go to google and check the spelling of the name of the movie you want.
ഈ സിനിമ ഞങ്ങളുടെ ഡാറ്റാബേസിൽ ഇല്ലെങ്കിൽ നിങ്ങൾക്ക് ഈ സിനിമ ലഭിക്കില്ല
അല്ലെങ്കിൽ, അഭ്യർത്ഥിച്ച സിനിമയുടെ പേരിന്റെ അക്ഷരവിന്യാസം ശരിയായിരിക്കില്ല ...
അതിനാൽ നിങ്ങൾ ഗൂഗിളിൽ പോയി നിങ്ങൾക്ക് ആവശ്യമുള്ള സിനിമയുടെ പേരിന്റെ സ്പെല്ലിംഗ് പരിശോധിക്കുക""",
            reply_markup=InlineKeyboardMarkup(
                      [[ 

                         InlineKeyboardButton("🔍 GOOGLE 🔎", url=f'https://www.google.com/')
                        ]]
                ),     
            parse_mode="html",
            reply_to_message_id=message.message_id)
            await asyncio.sleep(30)
            await spf.delete()
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
        else:
            query = search
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        
    
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            
                await message.reply_photo(photo=poster.get('poster'), caption=f"**↪️ Requested:** {query}\n**🎬 Title:** {poster.get('title')}\n**🎭 Genres:** {poster.get('genres')}\n**📆 Year:** <a href={poster['url']}/releaseinfo>{poster.get('year')}</a>\n**🌟Rating:** <a href={poster['url']}/ratings>{poster.get('rating')}</a> / 10\n**📑 Total Page :** <code>1 to 1</code>\n**🗃️ TotalFiles :** None\n**👤requested by:** {message.from_user.mention}", reply_markup=InlineKeyboardMarkup(buttons))

        else:
                await message.reply_text(imdb, reply_markup=InlineKeyboardMarkup(buttons))
        return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⫸",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"↪️ Requested: {search}\n**🎬 Title:** {poster.get('title')}\n**🎭 Genres:** {poster.get('genres')}\n**📆 Year:** <a href={poster['url']}/releaseinfo>{poster.get('year')}</a>\n**🌟Rating:** <a href={poster['url']}/ratings>{poster.get('rating')}</a> / 10\n**📑 Total Page :** <code>1 to 1</code>\n**🗃️ TotalFiles :** None\n**👤requested by:** {message.from_user.mention}", reply_markup=InlineKeyboardMarkup(buttons))

        else:
            await message.reply_text(f"sorry no imdb found", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def give_filter(client, message):
    group_id = message.chat.id
    name = message.text

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
                            await message.reply_text(reply_text, disable_web_page_preview=True)
                        else:
                            button = eval(btn)
                            await message.reply_text(
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button)
                            )
                    elif btn == "[]":
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or ""
                        )
                    else:
                        button = eval(btn) 
                        await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button)
                        )
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
    _, user, movie_ = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer("okDa", show_alert=True)
    if movie_  == "close_spellcheck":
        return await query.message.delete()
    movies = SPELL_CHECK.get(query.message.reply_to_message.message_id)
    if not movies:
        return await query.answer("You are clicking on an old button which is expired.", show_alert=True)
    movie = movies[(int(movie_))]
    await query.answer('Checking for Movie in database...')
    files, offset, total_results = await get_search_results(movie, offset=0, filter=True)
    if files:
        k = (movie, files, offset, total_results)
        await auto_filter(bot, query, k)
    else:
        k = await query.message.edit('This Movie Not Found In DataBase')
        await asyncio.sleep(10)
        await k.delete()

        
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
    
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        


        elif query.data.startswith("subinps"):
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
                    f_caption = f"{files.file_name}" 
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=button.CAPTION,
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
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
                    f_caption = f"{title}" hhh
                buttons = [
                    [
                        InlineKeyboardButton('More Bots', url='https://t.me/joinchat/EOI9s4lc00cyOTI1'),
                        InlineKeyboardButton('bot updates', url='https://t.me/joinchat/EOI9s4lc00cyOTI1')
                    ]
                    ]
                hhhhhh
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=button.CAPTION
                    )
    elif query.data == "pages":
       await query.answer()
    elif query.data == "close":
          try:
            await query.message.reply_to_message.delete()
            await query.message.delete()
          except:
            await query.message.delete()
                
    else:
        await query.answer("കൌതുകും ലേശം കൂടുതൽ ആണല്ലേ👀",show_alert=True)
        
 
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
        buttons = [[ 
            InlineKeyboardButton('➕ ADD ME TO YOUR GROUP ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true'),
            ],[
            InlineKeyboardButton("Search Here", switch_inline_query_current_chat=''),
            InlineKeyboardButton("🤖 VENOM UPDATES", url=f"https://t.me/joinchat/EOI9s4lc00cyOTI1")
            ],[
            InlineKeyboardButton("😎About", callback_data="about"),
            InlineKeyboardButton('ℹHELP', callback_data='help')
            ],[
            InlineKeyboardButton('how to use me ❔', callback_data='use')
         ]] 
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Translation.START_TXT.format(query.from_user.first_name),
            reply_markup=reply_markup,
            parse_mode='html'
            )
        
    elif query.data == "about": 
        timefmt = time_formatter(time.time() - start_uptime),
        await query.message.edit_text(Translation.ABOUT_TXT.format(timefmt), reply_markup=InlineKeyboardMarkup(
               [[
                         InlineKeyboardButton("📦 Source", url="https://t.me/mD_movieseses"),
                         InlineKeyboardButton("Dev 🤠", url="https://t.me/mdadmin2")
                         ],
                         [
                         InlineKeyboardButton("🏕️ Home", callback_data="start"),
                         InlineKeyboardButton("Close 🗑️", callback_data="close")
                   ]] 
                ))
    
    elif query.data == "use":
        buttons = [[
            InlineKeyboardButton('🚶close', callback_data='close')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.reply_video(
            video='https://telegra.ph/file/fe9b257274b17e9487dbb.mp4',
            caption='tutorial will comming soon \n\n you dont know anything please contact @mdadmin2',
            reply_markup=reply_markup,
            parse_mode='html')
        
    elif query.data == "help":
        buttons = [[ 
            InlineKeyboardButton('AUTO FILTER', callback_data='autofilter'),
            InlineKeyboardButton('MANUAL FILTER', callback_data='manual'),
            InlineKeyboardButton('CONNECTION', callback_data='connection')
            ],[
            InlineKeyboardButton('SONGS', callback_data='song'),
            InlineKeyboardButton('TELEGRAPH', callback_data='telegraph'),
            InlineKeyboardButton('CALCULATOR', callback_data='cal')
            ],[
            InlineKeyboardButton('🏠 Home', callback_data='start'),
            InlineKeyboardButton('🔮 Status', callback_data="stats"),
            InlineKeyboardButton('NEXT ➪', callback_data='extra')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="<b> hey user my name is venom i will send movies </b>\n",
            reply_markup=reply_markup,
            parse_mode='html'
            )
 
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('COVID', callback_data='covid'),
            InlineKeyboardButton('COUNTRY', callback_data='cal'),
            InlineKeyboardButton('EXTRA', callback_data='extramod')
            ],[
            InlineKeyboardButton('PIN', callback_data='pin'),
            InlineKeyboardButton('MISC', callback_data='misc'),
            InlineKeyboardButton('IMDB', callback_data='imdb')
            ],[
            InlineKeyboardButton('⇚ back', callback_data='help'),
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="extra mods are not available\n avilable soon...",
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "autofilter": 
        await query.message.edit_text(
            text=Translation.AUTOFILTER_TXT,
            reply_markup=BUTTONS,
            parse_mode='html'
        )
    elif query.data == "song": 
        await query.message.edit_text(
            text=Translation.SONG_TXT,
            reply_markup=BUTTONS,
            parse_mode='html'
        )  
    elif query.data == "telegraph": 
        await query.message.edit_text(
            text=Translation.TELPH_TXT,
            reply_markup=BUTTONS,
            parse_mode='html'
        )  
     
    elif query.data == "pin": 
        await query.message.edit_text(
            text=Translation.PIN_TXT,
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
    elif query.data == "extramod":
        await query.message.edit_text(
            text=Translation.MISC_TXT,
            reply_markup=BUTTONS2,
            parse_mode='html'
        ) 
    elif query.data == "connection": 
        await query.message.edit_text(
            text=Translation.CONNECTION_TXT,
            reply_markup=BUTTONS,
            parse_mode='html'
        ) 
    elif query.data == "manual": 
        await query.message.edit_text(
            text=Translation.MANUALFILTER_TXT,
            reply_markup=BUTTONS,
            parse_mode='html'
        ) 
    elif query.data == "stats":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('⇚Back', callback_data='help'),
            InlineKeyboardButton('↻ refresh', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size() 
        monsize = get_size(monsize)
        await query.message.edit_text(
            text=Translation.STATUS_TXT.format(total, users, chats, monsize),
            reply_markup=reply_markup,
            parse_mode='html'
        )
 
    elif query.data == "rfrsh":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('⇚ Back', callback_data='help'),
            InlineKeyboardButton('↻ refresh', callback_data='rfrsh')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        total = await Media.count_documents()
        users = await db.total_users_count()
        chats = await db.total_chat_count()
        monsize = await db.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        await query.message.edit_text(
            text=Translation.STATUS_TXT.format(total, users, chats, monsize),
            reply_markup=reply_markup,
            parse_mode='html'
      )
   
async def cb_data(bot, update):
        data = update.data
        try:
            message_text = update.message.text.split("\n")[0].strip().split("=")[0].strip()
            message_text = '' if CALCULATE_TEXT in message_text else message_text
            if data == "=":
                text = float(eval(message_text))
            elif data == "DEL":
                text = message_text[:-1]
            elif data == "AC":
                text = ""
            else:
                text = message_text + data
            await update.message.edit_text(
                text=f"{text}\n\n{CALCULATE_TEXT}",
                disable_web_page_preview=True,
                reply_markup=CALCULATE_BUTTONS
            )
        except Exception as error:
            print(error)

            
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text 
        leng = ("total_len")
        query = search
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                    )
        else: 
            spf = await message.reply_text(
            text=f"Sorry, I didn't get any files matches with your keyword, maybe your spelling is wrong. try sending the proper movie name...",
            reply_markup=InlineKeyboardMarkup(
                      [[ 

                         InlineKeyboardButton("🔍 GOOGLE 🔎", url=f'https://www.google.com/')
                        ]]
                ),     
            parse_mode="html",
            reply_to_message_id=message.message_id)
            await asyncio.sleep(10)
            await spf.delete()
            
     
               
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
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster.get('poster'), caption=f"**↪️ Requested:** {query}\n**🎬 Title:** {poster.get('title')}\n**🎭 Genres:** {poster.get('genres')}\n**📆 Year:** <a href={poster['url']}/releaseinfo>{poster.get('year')}</a>\n**🌟Rating:** <a href={poster['url']}/ratings>{poster.get('rating')}</a> / 10\n**📑 Total Page :** <code>1**to**1</code>\n**🗃️ TotalFiles :** None\n**👤requested in:** {message.chat.title}", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⫸ ",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster.get('poster'), caption=f"**↪️ Requested:** {query}\n**🎬 Title:** {poster.get('title')}\n**🎭 Genres:** {poster.get('genres')}\n**📆 Year:** <a href={poster['url']}/releaseinfo>{poster.get('year')}</a>\n**🌟Rating:** <a href={poster['url']}/ratings>{poster.get('rating')}</a> / 10\n**📑 Total Page :** <code>1 to {data['total']}</code>\n**🗃️ TotalFiles :** None\n**👤requested in:** {message.chat.title}", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(caption=imdb, reply_markup=InlineKeyboardMarkup(buttons))
    
        
async def advantage_spell_chok(msg):
    query = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)", "", msg.text, flags=re.IGNORECASE) # plis contribute some common words 
    query = query.strip() + " movie"
    g_s = await search_gagala(query)
    g_s += await search_gagala(msg.text)
    gs_parsed = []
    if not g_s:
        k = await msg.reply("I couldn't find any movie in that name.")
        await asyncio.sleep(8)
        await k.delete()
        return
    regex = re.compile(r".*(imdb|wikipedia).*", re.IGNORECASE) # look for imdb / wiki results
    gs = list(filter(regex.match, g_s))
    gs_parsed = [re.sub(r'\b(\-([a-zA-Z-\s])\-\simdb|(\-\s)?imdb|(\-\s)?wikipedia|\(|\)|\-|reviews|full|all|episode(s)?|film|movie|series)', '', i, flags=re.IGNORECASE) for i in gs]
    if not gs_parsed:
        reg = re.compile(r"watch(\s[a-zA-Z0-9_\s\-\(\)]*)*\|.*", re.IGNORECASE) # match something like Watch Niram | Amazon Prime 
        for mv in g_s:
            match  = reg.match(mv)
            if match:
                gs_parsed.append(match.group(1))
    user = msg.from_user.id if msg.from_user else 0
    movielist = []
    gs_parsed = list(dict.fromkeys(gs_parsed)) # removing duplicates https://stackoverflow.com/a/7961425
    if len(gs_parsed) > 3:
        gs_parsed = gs_parsed[:3]
    if gs_parsed:
        for mov in gs_parsed:
            imdb_s = await get_poster(mov.strip(), bulk=True) # searching each keyword in imdb
            if imdb_s:
                movielist += [movie.get('title') for movie in imdb_s]
    movielist += [(re.sub(r'(\-|\(|\)|_)', '', i, flags=re.IGNORECASE)).strip() for i in gs_parsed]
    movielist = list(dict.fromkeys(movielist)) # removing duplicates
    if not movielist:
        k = await msg.reply("I couldn't find anything related to that. Check your spelling")
        await asyncio.sleep(8)
        await k.delete()
        return
    SPELL_CHECK[msg.message_id] = movielist
    btn = [[
                InlineKeyboardButton(
                    text=movie.strip(),
                    callback_data=f"spolling#{user}#{k}",
                )
            ] for k, movie in enumerate(movielist)]
    btn.append([InlineKeyboardButton(text="Close", callback_data=f'spolling#{user}#close_spellcheck')])
    await msg.reply("I couldn't find anything related to that\nDid you mean any one of these?", reply_markup=InlineKeyboardMarkup(btn))
    

