import os
from pyrogram.types import Message
from pyrogram import Client, filters
from telegraph import upload_file
from pyrogram.types import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from requests.utils import requote_uri
API = "https://api.sumanjay.cf/covid/?country="
BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://telegram.me/FayasNoushad')]])

from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
@Client.on_message(filters.media & filters.private)
async def telegraph_upload(bot, update):

    medianame = "./DOWNLOADS/" + "FayasNoushad/FnTelegraphBot"
    text = await update.reply_text(
        text="<code>Downloading to My Server ...</code>",
        disable_web_page_preview=True
    )
    await bot.download_media(
        message=update,
        file_name=medianame
    )
    await text.edit_text(
        text="<code>Downloading Completed. Now I am Uploading to telegra.ph Link ...</code>",
        disable_web_page_preview=True
    )
    try:
        response = upload_file(medianame)
    except Exception as error:
        print(error)
        await text.edit_text(
            text=f"Error :- {error}",
            disable_web_page_preview=True
        )
        return
    try:
        os.remove(medianame)
    except Exception as error:
        print(error)
        return
    await text.edit_text(
        text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>\n\n<b>Join :-</b> @MT_Botz",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Open Link", url=f"https://telegra.ph{response[0]}"),
                    InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
                ],
                [  
                    InlineKeyboardButton(text="⚙ Join Updates Channel ⚙", url="https://telegram.me/FayasNoushad")
                ],
                [
                    InlineKeyboardButton('🖥️ Deploy Video 🖥️', url='https://youtu.be/c-GfUfriP50')
                ]
            ]
        )
    )

@Client.on_message(filters.reply & filters.command("covid"))
async def reply_info(bot, message):
    reply_markup = BUTTONS
    b_msg = message.reply_to_message
    await message.reply_text(
        text=covid_info(b_msg),
        disable_web_page_preview=True,
        quote=True,
        
 
        reply_markup=reply_markup
    )
    
def covid_info(country_name):
    try:
        r = requests.get(API + requote_uri(country_name.lower()))
        info = r.json()
        country = info['country'].capitalize()
        active = info['active']
        confirmed = info['confirmed']
        deaths = info['deaths']
        info_id = info['id']
        last_update = info['last_update']
        latitude = info['latitude']
        longitude = info['longitude']
        recovered = info['recovered']
        covid_info = f"""--**Covid 19 Information**--
Country : `{country}`
Actived : `{active}`
Confirmed : `{confirmed}`
Deaths : `{deaths}`
ID : `{info_id}`
Last Update : `{last_update}`
Latitude : `{latitude}`
Longitude : `{longitude}`
Recovered : `{recovered}`
Made by @FayasNoushad"""
        return covid_info
    except Exception as error:
        return error

#-------------------pin---------------------#
@Client.on_message(filters.command("pin"))
async def pin(_, message: Message):
    if not message.reply_to_message:
        return
    await message.reply_to_message.pin()

@Client.on_message(filters.command("unpin"))
async def unpin(_, message: Message):
    if not message.reply_to_message:
        return
    await message.reply_to_message.unpin()
    

#_________________calculator_________________#
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
@Client.on_message(filters.private & filters.command(["calc", "calculate", "calculator"]))
async def calculate(bot, update):
    await update.reply_text(
        text=CALCULATE_TEXT,
        reply_markup=CALCULATE_BUTTONS,
        disable_web_page_preview=True,
        quote=True
    )

