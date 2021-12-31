import os
import time
from pyrogram.types import Message
from pyrogram import Client, filters
from telegraph import upload_file
from pyrogram.types import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from requests.utils import requote_uri
from utils import temp
API = "https://api.sumanjay.cf/covid/?country="
BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton('⚙ Join Updates Channel ⚙', url='https://t.me/venombotupdates')]])

from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
@Client.on_message(filters.media & filters.private)
async def telegraph_upload(bot, update):

    medianame = "./DOWNLOADS/" + "venom/telegraph"
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
        text=f"<b>Link :-</b> <code>https://telegra.ph{response[0]}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Open Link", url=f"https://telegra.ph{response[0]}"),
                    InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
                ],
                [  
                    InlineKeyboardButton(text="📢 Join venom Update Channel ", url="https://t.me/venombotupdates")
                ]
            ]
        )
    )

@Client.on_message(filters.command("covid"))
async def reply_info(bot, message):
    reply_markup = BUTTONS
    b_msg = message.text.split(None, 1)[1]
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
searched by @{temp.U_NAME}"""
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
    
import wikipedia

#_____________________ping_____________________
@Client.on_message(filters.command("ping"))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"Pong!\n{time_taken_s:.3f} ms")

#==========================================================
@Client.on_message(filters.reply & filters.command("wiki"))
async def wiki(bot, message):
    srch = message.reply_to_message
    if not srch:
        return await message.reply_text ("`Give some text to search on wikipedia !`")
    msg = await message.reply_text( f"`Searching {srch} on wikipedia..`")
    try:
        mk = wikipedia.summary(srch, sentences=3)
        te = f"**Search Query :** {srch}\n\n**Results :** {mk[:100]}"
        await msg.edit(te)
    except Exception as e:
        await msg.edit(f"**ERROR** : {str(e)}")
    b_msg = message.reply_to_message

#=============================================================
from io import BytesIO

@Client.on_message(filters.command(["json", "response"]), group=1)
async def response_json(bot, update):
    json = update.reply_to_message
    with BytesIO(str.encode(str(json))) as json_file:
        json_file.name = "JSON.text"
        await json.reply_document(
            document=json_file,
            quote=True
        )
        try:
            os.remove(json_file)
        except:
            pass

#================================================================
import traceback
from asyncio import get_running_loop 
from googletrans import Translator
from gtts import gTTS


def convert(text):
    audio = BytesIO()
    i = Translator().translate(text, dest="en")
    lang = i.src
    tts = gTTS(text, lang=lang)
    audio.name = lang + ".mp3"
    tts.write_to_fp(audio)
    return audio


@Client.on_message(filters.command("tts"))
async def text_to_speech(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to some text ffs.")
    if not message.reply_to_message.text:
        return await message.reply_text("Reply to some text ffs.")
    m = await message.reply_text("Processing")
    text = message.reply_to_message.text
    try:
        loop = get_running_loop()
        audio = await loop.run_in_executor(None, convert, text)
        await message.reply_audio(audio)
        await m.delete()
        audio.close()
    except Exception as e:
        await m.edit(e)
        e = traceback.format_exc()
        print(e)

@Client.on_message(filters.command(["findid", "stickerid"]))
async def find_by_file_id(_, message):
    if not message.reply_to_message:
        return
    stickerid = str(message.reply_to_message.text)
    try:
        await message.reply_cached_media(
            stickerid,
            quote=True
        )
    except Exception as error:
        await message.reply_text(error occurred", quote=True)
