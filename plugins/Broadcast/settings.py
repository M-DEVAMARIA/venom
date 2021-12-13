#@crazybot filter bot v2
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import ButtonDataInvalid, FloodWait

@Client.on_message(filters.command(['settinga'])& filters.group, group=1)
async def bot_info(client, message):
    buttons = [[
            InlineKeyboardButton("🤖 Venom UPDATES", url=f"https://t.me/joinchat/EOI9s4lc00cyOTI1")
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_message(
        chat_id=message.chat.id,
        reply_markup=reply_markup,
        text="hi, how are you ",
        parse_mode="html")
