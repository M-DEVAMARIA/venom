import os
from pyrogram import filters, Client
from translation import Translation


@Client.on_message(filters.command(['info']))
async def bot_info(client, message):
    
    await client.send_message(
        chat_id=message.chat.id,
       
        text=Translation.ABOUT_TXT,
        parse_mode="html")
