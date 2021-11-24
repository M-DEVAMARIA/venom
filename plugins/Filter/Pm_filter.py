#Kanged From @TroJanZheX
from info import AUTH_CHANNEL, IMDB_TEMPLATE, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, BUTTON, start_uptime, IMDB
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re, time, asyncio

from translation import Translation
from pyrogram.errors import UserNotParticipant
from utils import Media, get_filter_results, get_file_details, is_subscribed, get_poster, time_formatter, temp, search_gagala
from database.users_db import db
from .Inline import RATING, GENRES
import random
BUTTONS = {}
BOT = {}
SPELL_CHECK = {}
      
        
    
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
    
        imdfb = f"<b>Query: {query}</b> \n‌‌‌‌IMDb Data:\n\n
        🏷 Title: <a href={url}>{title}</a>\n
        🎭 Genres: {genres}\n
        📆 Year: <a href={url}/releaseinfo>{year}</a>\n
        🌟 Rating: <a href={url}/ratings>{rating}</a> / 10")
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
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="Close ❌",callback_data="close")])
            poster=None
            imdb = await get_poster(search, file=(files[0]).file_name) if IMDB else None
            
            
            if imdb and imdb.get('poster'):
                await message.reply_photo(photo=poster.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(buttons))
               

            else:
                await message.reply_text(imdb, reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
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
            await message.reply_photo(photo=poster, caption=imdb, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"sorry no imdb found", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text 
        leng = ("total_len")
        imdb = f"**🗂️ Title:** {search}\n🗃️ Total Files : {leng}\n**⭐ Rating:** {random.choice(RATING)}\n**🎭 Genre:** {random.choice(GENRES)}\n**📤 Uploaded by {message.chat.title}**" 
        
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
            await advantage_spell_chok(message)
     
               
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
                await message.reply_photo(photo=poster, caption=imdb, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"<b>Here is What I Found In My Database For Your Query {search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </b>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
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
            await message.reply_photo(photo=poster, caption=imdb, reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(caption=imdb, reply_markup=InlineKeyboardMarkup(buttons))

    
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
                buttons = [
                    [
                        InlineKeyboardButton('More Bots', url='https://t.me/joinchat/EOI9s4lc00cyOTI1'),
                        InlineKeyboardButton('Update Channel', url='https://t.me/joinchat/EOI9s4lc00cyOTI1')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
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
                    f_caption = f"{title}"
                buttons = [
                    [
                        InlineKeyboardButton('More Bots', url='https://t.me/joinchat/EOI9s4lc00cyOTI1'),
                        InlineKeyboardButton('bot updates', url='https://t.me/joinchat/EOI9s4lc00cyOTI1')
                    ]
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
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



        
    elif query.data == "start":
        buttons = [[ 
            InlineKeyboardButton('➕ ADD ME TO YOUR GROUP ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true'),
            ],[
            InlineKeyboardButton("Search Here", switch_inline_query_current_chat=''),
           InlineKeyboardButton("🤖 VENOM UPDATES", url=f"https://t.me/joinchat/EOI9s4lc00cyOTI1")
            ],[
            InlineKeyboardButton("😎About", callback_data="about"),
            InlineKeyboardButton('ℹ️HELP', callback_data='help')
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
                         InlineKeyboardButton("📦 Source", callback_data="source"),
                         InlineKeyboardButton("Dev 🤠", url="https://t.me/mdadmin2")
                         ],
                         [
                         InlineKeyboardButton("🏕️ Home", callback_data="start"),
                         InlineKeyboardButton("Close 🗑️", callback_data="close")
                   ]] 
                ))
    elif query.data == "source":
       await query.message.edit_text(
        text='<b> private source code are used in bot </b>',
        parse_mode='html')
    
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
            InlineKeyboardButton('Auto Filter', callback_data='autofilter'),
            InlineKeyboardButton('Extra Mods', callback_data='extra')
            ],[
            InlineKeyboardButton('🏠 Home', callback_data='start'),
            InlineKeyboardButton('📈 Status', callback_data="stats")
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="<b> hey user my name is venom i will send movies </b>\n",
            reply_markup=reply_markup,
            parse_mode='html'
            )

    elif query.data == "autofilter":
        buttons = [[
            InlineKeyboardButton('🚶Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=Translation.AUTOFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode='html'
        )
    elif query.data == "extra":
        buttons = [[
            InlineKeyboardButton('🚶Back', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="extra mods are not available\n avilable soon...",
            reply_markup=reply_markup,
            parse_mode='html'
        )
        
    elif query.data == "stats":
        await query.answer("Fetching MongoDb DataBase")
        buttons = [[
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('🔄 refresh', callback_data='rfrsh')
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
            InlineKeyboardButton('👩‍🦯 Back', callback_data='help'),
            InlineKeyboardButton('🔄 refresh', callback_data='rfrsh')
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
    

