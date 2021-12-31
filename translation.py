class Translation(object):
    START_TXT = """ <b>HEY, {}</b>

<code>I am a autofilter + manual + filestore bot I will give movies in your group and my PM ! Also I can store files</code>

<b>maintained by : @mdadmin2</b>"""

    ABOUT_TXT = """ 
╔═╦═╗╔═╗╔═╦╗╔═╗╔══╗ 
╚╗║╔╝║╩╣║║║║║╬║║║║║
─╚═╝─╚═╝╚╩═╝╚═╝╚╩╩╝ 
   ╭━━━━━━━━━━━━━━━➣
║┣⪼📃Bot : <a href="t.me/md_movises">venom Robot</a>
║┣⪼👦Creator : <a href="t.me/mdadmin2">MDADMIN</a>
║┣⪼📡Hosted On : <a href="https://t.me/md_movises">Heroku</a>
║┣⪼🗣️Language : <a href="https://docs.pyrogram.org">Python3</a>
║┣⪼📚Library : <a href="https://docs.pyrogram.org">Pyrogram Asyncio 1.13.0 </a>
║┣⪼🕛uptime : <a href="t.me/md_movises">{}</a>
║┣⪼🗒️Version : <a href="t.me/md_movises">1.0.0</a>
   ╰━━━━━━━━━━━━━━━➣
"""
    SETTINGS_TXT = """<b>coustime your</b> {} <b>Group settings.</b>\n
Current settings:-\n
⪼ <b>Auto Filter::</b> {}\n
⪼ <b>Buttons mode:</b> {}\n
⪼ <b>Spelling mode:</b> {}\n
⪼ <b>Filter per page:</b> {}\n
⪼ <b>Auto delete :</b> {}\n
⪼ <b>Imdb:</b> {}

change above value using buttons below
"""

    AUTOFILTER_TXT = """ <b>Auto Filter</b>
<b>NOTE:</b>

1. Make me the admim of your channel if it's private .
2. make sure that your channel does not contains cam rip, porn and fake files.
3. send /index then Forward the last message to me with quotes.
 I'll add all the files in that channel to my db."""
    
    MANUALFILTER_TXT = """
Help: <b>Filters</b>

- Filter is the feature were users can set automated replies for a particular keyword and venom will respond whenever a keyword is found the message

NOTE:
1. Venom should have admin privillage.
2. only admins can add filters in a chat.
3. alert buttons have a limit of 64 characters.

Commands and Usage:
• /filter - <code>add a filter in chat</code>
• /filters - <code>list all the filters of a chat</code>
• /del - <code>delete a specific filter in chat</code>
• /delall - <code>delete the whole filters in a chat (chat owner only)</code>"""
    
    CONNECTION_TXT = """
Help: <b>Connections</b>

- Used to connect bot to PM for managing filters 
- it helps to avoid spamming in groups.

NOTE:
1. Only chat admins can add a connection.
2. Send /connect for connecting Venom to your PM

Commands and Usage:
• /connect  - <code>connect a particular chat to Venom PM</code>
• /disconnect  - <code>disconnect from a chat</code>
• /connections - <code>list all your connections</code> """
   
    STATUS_TXT = """
➭ Total files in db: <code>{}</code>
➭ users: <code>{}</code>
➭ total groups: <code>{}</code>
➭ used storage: <code>{}</code> """
    MISC_TXT = """Help: <b>Extra Modules</b>
<b>NOTE:</b>

<b>Commands and Usage:</b>
• /id - <code>get id of a specifed user.</code>
• /info  - <code>get information about a user.</code>"""
    SONG_TXT = """
🎧 Song Downloader

A Module To Download Songs From Youtube

/song <code>{song name}</code> - <code>Download song from youtube</code>"""
    TELPH_TXT = """
<b>Telegraph</b>

<b>Note:</b>

</code>send media under 5mb then bot will send telegraph link</code> """
    COVID_TXT = """ <b> 🌏 covid information </b>
  
A module to find all country covid informations.
    
<b>🗣️ Available commands </b>\n
▪️/covid :- <code> reply to country name </code> """

    PIN_TXT ="""<b>PIN MODULE</b>
<b>Pin :</b>\n
<b>All The Pin Related Commands Can Be Found Here; Keep Your Chat Up To Date On The Latest News With A Simple Pinned Message!</b>\n
<b>📚 Commands & Usage:</b>\n
◉ /Pin :- <code>Pin The Message You Replied To Message To Send A Notification To Group Members</code>
◉ /Unpin :- <code>Unpin The Current Pinned Message. If Used As A Reply, Unpins The Replied To Message</code>"""

    JSON_TXT = """<b>JSON module:</b>\n\n𝖡𝗈𝗍 𝗋𝖾𝗍𝗎𝗋𝗇𝗌 𝗃𝗌𝗈𝗇 𝖿𝗈𝗋 𝖺𝗅𝗅 𝗋𝖾𝗉𝗅𝗂𝖾𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 with /json.\n\n𝖥𝖾𝖺𝗍𝗎𝗋𝖾𝗌:\n𝖬𝖾𝗌𝗌𝖺𝗀𝖾 𝖤𝖽𝗂𝗍𝗍𝗂𝗇𝗀 JSON\n𝖯𝗆 𝖲𝗎𝗉𝗉𝗈𝗋𝗍\n𝖦𝗋𝗈𝗎𝗉 𝖲𝗎𝗉𝗉𝗈𝗋𝗍\n <b>📕 Commands:</b>\n\n
/json - <code>reply to message which you want get json | നിങ്ങൾക്ക് json ലഭിക്കാൻ ആഗ്രഹിക്കുന്ന സന്ദേശത്തിന് മറുപടി നൽകുക</code>"""
    
    STORE_TXT = """<b>Batch module</b>\n\nThis module is for store one or more files or message using venom. You can get stored message or file by a special link given by bot\n\n📚 Command\n\n/batch -  <code>command for store files or message</code>"""
    TTS_TXT = """<b>🗣 TEXT To Speech</b>\n\nA Module To Convert TEXT To Voice With Language Support\n\n<b>📚Commands:</b>\n\n◉ /tts :- <code>Reply To Any TEXT Message  To Convert as audio</code>"""
    IMDB_TXT = """<b>IMDB MODULE</b>\n\nA Module To Get The Movie Informations. Use This Module To Get Movie Informations\n\n📚<b> commands:</b>\n◉ /imdb - <code>get the film information from IMDb source.</code>\n◉ /search - <code>get the film information from IMDb source.</code>"""
    SETT_TXT = """<b>Settings module</b>\n\nThis module is for customise your Auto filters settings in your group.\n\n📚 Commands:\n\n/settings <code>- command for open settings module in group</code>"""
    
    
