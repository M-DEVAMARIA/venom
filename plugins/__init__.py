#_________mdbotz___________________#
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import IMDB_TEMPLATE
from utils import temp
import imdb

VERIFY = {}

START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('➕ ADD ME TO YOUR GROUP ➕', url=f'http://t.me/Venom_moviebot?startgroup=true'),
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
           
CALCULATE_TEXT = "Use below buttons to calculate numbers"
CALCULATE_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton("DEL", callback_data="cal#DEL"),
        InlineKeyboardButton("AC", callback_data="cal#AC"),
        InlineKeyboardButton("(", callback_data="cal#("),
        InlineKeyboardButton(")", callback_data="cal#)")
        ],[
        InlineKeyboardButton("7", callback_data="cal#7"),
        InlineKeyboardButton("8", callback_data="cal#8"),
        InlineKeyboardButton("9", callback_data="cal#9"),
        InlineKeyboardButton("÷", callback_data="cal#/")
        ],[
        InlineKeyboardButton("4", callback_data="cal#4"),
        InlineKeyboardButton("5", callback_data="cal#5"),
        InlineKeyboardButton("6", callback_data="cal#6"),
        InlineKeyboardButton("×", callback_data="cal#*")
        ],[
        InlineKeyboardButton("1", callback_data="cal#1"),
        InlineKeyboardButton("2", callback_data="cal#2"),
        InlineKeyboardButton("3", callback_data="cal#3"),
        InlineKeyboardButton("-", callback_data="cal#-")
        ],[
        InlineKeyboardButton(".", callback_data="cal#."),
        InlineKeyboardButton("0", callback_data="cal#0"),
        InlineKeyboardButton("=", callback_data="cal#="),
        InlineKeyboardButton("+", callback_data="cal#+")
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
        InlineKeyboardButton('Fɪʟᴇ sᴛᴏʀᴇ', callback_data='batch')
        ],[
        InlineKeyboardButton('settings', callback_data='sett'),
        InlineKeyboardButton('ᴄᴀʟᴄᴜʟᴀᴛᴏʀ', callback_data="clcltr"),
        InlineKeyboardButton('ᴄᴏᴠɪᴅ', callback_data='covid')
        ],[
        InlineKeyboardButton('Wɪᴋɪᴘᴇᴅɪᴀ', callback_data='wiki'),
        InlineKeyboardButton('extra', callback_data='extramod'),
        InlineKeyboardButton('ᴘɪɴ', callback_data='pin')
        ],[
        InlineKeyboardButton('mísc', callback_data='misc'),
        InlineKeyboardButton('ɪᴍᴅʙ', callback_data='imbs'),
        InlineKeyboardButton('jѕon', callback_data='json')
        ],[
        InlineKeyboardButton('⇚ ʙᴀᴄᴋ', callback_data='start'),
        InlineKeyboardButton('stαtus', callback_data='stats'),
        InlineKeyboardButton('TTS', callback_data='tts')
        ]]
     )
            
HELPS = InlineKeyboardMarkup(
       [[  
       InlineKeyboardButton('ᴀᴜᴛᴏ fɪʟᴛᴇʀ', callback_data='autofilter'),
       InlineKeyboardButton('ᴍᴀɴᴜᴀʟ fɪʟᴛᴇʀ', callback_data='manual')
       ],[    
       InlineKeyboardButton('ᴄᴏɴɴᴇᴄᴛɪᴏɴ', callback_data='connection'),
       InlineKeyboardButton('Fɪʟᴇ sᴛᴏʀᴇ', callback_data='batch')
       ],[
       InlineKeyboardButton('settings', callback_data='sett'),
       InlineKeyboardButton('extra', callback_data='extramod')   
       ]])
