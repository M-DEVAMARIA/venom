import os
from pyrogram import filters, Client
from translation import Translation


@Client.on_message(filters.command(['info']))
async def bot_info(client, message):
    
    await client.send_message(
        chat_id=message.chat.id,
       
        text=Translation.ABOUT_TXT,
        parse_mode="html")

"@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == "private":
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or ""
        username = message.from_user.username
        dc_id = message.from_user.dc_id or ""
        await message.reply_text(
            f"<b>➲ First Name:</b> {first}\n<b>➲ Last Name:</b> {last}\n<b>➲ Username:</b> {username}\n<b>➲ Telegram ID:</b> <code>{user_id}</code>\n<b>➲ Data Centre:</b> <code>{dc_id}</code>",
            quote=True
        )#/EvaMaria/blob/master/plugins/misc.py#:~:text=setLevel(logging.ERROR)-,%40Client.on_message(filters.command(%27id%27)),),-elif%20chat_type%20in    
