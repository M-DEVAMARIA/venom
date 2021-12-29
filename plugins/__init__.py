#_________mdbotz___________________#
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import IMDB_TEMPLATE
from utils import temp
import imdb

VERIFY = {}

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('➕ ADD ME TO YOUR GROUP ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true'),
        ],[
        InlineKeyboardButton("Search Here", switch_inline_query_current_chat=''),
        InlineKeyboardButton("🤖 VENOM UPDATES", url=f"https://t.me/joinchat/EOI9s4lc00cyOTI1")
        ],[
        InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about"),
        InlineKeyboardButton('ʜᴇʟᴘ', callback_data='help')
        ],[
        InlineKeyboardButton('Features ❔', callback_data='user')
        ]] 
        ) 
           
CALCULATE_TEXT = "Made by @FayasNoushad"
CALCULATE_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("DEL", callback_data="DEL"),
        InlineKeyboardButton("AC", callback_data="AC"),
        InlineKeyboardButton("(", callback_data="("),
        InlineKeyboardButton(")", callback_data=")")
        ],[
        InlineKeyboardButton("7", callback_data="7"),
        InlineKeyboardButton("8", callback_data="8"),
        InlineKeyboardButton("9", callback_data="9"),
        InlineKeyboardButton("÷", callback_data="/")
        ],[
        InlineKeyboardButton("4", callback_data="4"),
        InlineKeyboardButton("5", callback_data="5"),
        InlineKeyboardButton("6", callback_data="6"),
        InlineKeyboardButton("×", callback_data="*")
        ],[
        InlineKeyboardButton("1", callback_data="1"),
        InlineKeyboardButton("2", callback_data="2"),
        InlineKeyboardButton("3", callback_data="3"),
        InlineKeyboardButton("-", callback_data="-"),
        ],[
        InlineKeyboardButton(".", callback_data="."),
        InlineKeyboardButton("0", callback_data="0"),
        InlineKeyboardButton("=", callback_data="="),
        InlineKeyboardButton("+", callback_data="+"),
        ]]
    )

CAPTION = InlineKeyboardMarkup([[InlineKeyboardButton('📢 Join Updates Channel ', url='https://t.me/venombotupdates')]])

HELP = InlineKeyboardMarkup(
        [[ 
        InlineKeyboardButton('ᴀᴜᴛᴏ fɪʟᴛᴇʀ', callback_data='autofilter'),
        InlineKeyboardButton('ᴍᴀɴᴜᴀʟ fɪʟᴛᴇʀ', callback_data='manual'),
        InlineKeyboardButton('ᴄᴏɴɴᴇᴄᴛɪᴏɴ', callback_data='connection')
        ],[
        InlineKeyboardButton('song', callback_data='song'),
        InlineKeyboardButton('ᴛᴇʟᴇɢʀᴀᴘʜ', callback_data='telegraph'),
        InlineKeyboardButton('ʙᴀᴛᴄʜ', callback_data='batch')
        ],[
        InlineKeyboardButton('⇚ ʙᴀᴄᴋ', callback_data='start'),
        InlineKeyboardButton('stαtus', callback_data="stats"),
        InlineKeyboardButton('settings', callback_data='covid')
        ],[
        InlineKeyboardButton('ᴄᴏᴜɴᴛʀʏ', callback_data='cal'),
        InlineKeyboardButton('extra', callback_data='extramod'),
        InlineKeyboardButton('ᴘɪɴ', callback_data='pin')
        ],[
        InlineKeyboardButton('mísc', callback_data='misc'),
        InlineKeyboardButton('ɪᴍᴅʙ', callback_data='imbs'),
        InlineKeyboardButton('fun', callback_data='imbs')
        ],[
        InlineKeyboardButton('⇚ ʙᴀᴄᴋ', callback_data='help'),
        InlineKeyboardButton('jѕon', callback_data='json'),
        InlineKeyboardButton('TTS', callback_data='tts')
        ]]
     )
            
            
            
