from pyrogram import Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from translation import Translation








Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        elif query.data == "song":
            buttons = [[
                InlineKeyboardButton('👩‍🦯 Back', callback_data='help')
            ]]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=Translation.AUTOFILTER_TXT,
                reply_markup=reply_markup,
                parse_mode='html'
            )
