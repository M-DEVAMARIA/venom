import imdb 
from utils import temp
from info import IMDB_TEMPLATE
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def S(text):
        style = {
            'a': 'ᴀ',
            'b': 'ʙ',
            'c': 'ᴄ',
            'd': 'ᴅ',
            'e': 'ᴇ',
            'f': 'ғ',
            'g': 'ɢ',
            'h': 'ʜ',
            'i': 'ɪ',
            'j': 'J',
            'k': 'ᴋ',
            'l': 'ʟ',
            'm': 'ᴍ',
            'n': 'ɴ',
            'o': 'ᴏ',
            'p': 'ᴘ',
            'q': 'ǫ',
            'r': 'ʀ',
            's': 's',
            't': 'ᴛ',
            'u': 'ᴜ',
            'v': 'ᴠ',
            'w': 'ᴡ',
            'x': 'x',
            'y': 'ʏ',
            'z': 'ᴢ',
            'A': 'A',
            'B': 'B',
            'C': 'C',
            'D': 'D',
            'E': 'E',
            'F': 'F',
            'G': 'G',
            'H': 'H',
            'I': 'I',
            'J': 'J',
            'K': 'K',
            'L': 'L',
            'M': 'M',
            'N': 'N',
            'O': 'O',
            'P': 'P',
            'Q': 'Q',
            'R': 'R',
            'S': 'S',
            'T': 'T',
            'U': 'U',
            'V': 'V',
            'W': 'W',
            'X': 'X',
            'Y': 'Y',
            'Z': 'Z',
            '0': '𝟶',
            '1': '𝟷',
            '2': '𝟸',
            '3': '𝟹',
            '4': '𝟺',
            '5': '𝟻',
            '6': '𝟼',
            '7': '𝟽',
            '8': '𝟾',
            '9': '𝟿'
        }
        for i, j in style.items():
            text = text.replace(i, j)
        return text

class Button(object):
   START_BTN = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('➕ ᗩᗪᗪ ᗰᗴ TO YOᑌᖇ ᘜᖇOᑌᑭ ➕', url=f'http://t.me/Venom_moviebot?startgroup=true'),
        ],[
        InlineKeyboardButton(S("search here"), switch_inline_query_current_chat=''),
        InlineKeyboardButton(S("venom updates"), url=f"https://t.me/joinchat/EOI9s4lc00cyOTI1")
        ],[
        InlineKeyboardButton(S("about"), callback_data="about"),
        InlineKeyboardButton(S('help'), callback_data='help')
        ],[
        InlineKeyboardButton(S('mode'), callback_data='mode#i#i')
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

   CAPTION = InlineKeyboardMarkup([[InlineKeyboardButton(S('📢 Join updates Channel '), url='https://t.me/venombotupdates')]])

   HELP = InlineKeyboardMarkup(
        [[ 
        InlineKeyboardButton(S('auto filter'), callback_data='autofilter'),
        InlineKeyboardButton(S('manual filter'), callback_data='manual'),
        InlineKeyboardButton(S('connection'), callback_data='connection')
        ],[
        InlineKeyboardButton(S('song'), callback_data='song'),
        InlineKeyboardButton(S('telegraph'), callback_data='telegraph'),
        InlineKeyboardButton(S('file store'), callback_data='batch')
        ],[
        InlineKeyboardButton(S('settings'), callback_data='sett'),
        InlineKeyboardButton(S('calculator'), callback_data="clcltr"),
        InlineKeyboardButton(S('covid'), callback_data='covid')
        ],[
        InlineKeyboardButton(S('wikipedia'), callback_data='wiki'),
        InlineKeyboardButton(S('extra'), callback_data='extramod'),
        InlineKeyboardButton(S('pin'), callback_data='pin')
        ],[
        InlineKeyboardButton(S('misc'), callback_data='misc'),
        InlineKeyboardButton(S('imdb'), callback_data='imbs'),
        InlineKeyboardButton(S('json'), callback_data='json')
        ],[
        InlineKeyboardButton(S('back'), callback_data='start'),
        InlineKeyboardButton(S('status'), callback_data='stats'),
        InlineKeyboardButton(S('tts'), callback_data='tts')
        ]]
     )
            
   HELPS = InlineKeyboardMarkup(
       [[  
       InlineKeyboardButton(S('auto filter'), callback_data='autofilter'),
       InlineKeyboardButton(S('manual filter'), callback_data='manual')
       ],[    
       InlineKeyboardButton(S('connection'), callback_data='connection'),
       InlineKeyboardButton(S('file store'), callback_data='batch')
       ],[
       InlineKeyboardButton(S('settings'), callback_data='sett'),
       InlineKeyboardButton(S('extra'), callback_data='extramod') 
       ],[
       InlineKeyboardButton(S('back'), callback_data='start'),
       InlineKeyboardButton(S('status'), callback_data='stats'),
       ]])

   BUTTON = InlineKeyboardMarkup([[InlineKeyboardButton(S('back'), callback_data="start")]])
   BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton(S('back'), callback_data="help")]])
 
