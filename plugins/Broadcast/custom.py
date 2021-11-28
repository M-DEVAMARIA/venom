
from pyrogram import Client, filters
from telegraph import upload_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from pyrogram.errors.exceptions.bad_request_400 import PeerIdInvalid
@Client.on_message(filters.media & filters.private)
async def telegraph_upload(bot, update):
    
    except Exception as error:
            print(error)
            await update.reply_text(text="Something wrong. Contact <a href='https://telegram.me/TheFayas'>Developer</a>.", disable_web_page_preview=True)
            return
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
