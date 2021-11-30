from __future__ import unicode_literals

from pyrogram import Client, filters
import ffmpeg
import asyncio
import os
import time
import youtube_dl
from youtube_search import YoutubeSearch
import requests
from pyrogram.types import Message
from pytube import YouTube
from youtubesearchpython import VideosSearch
#________arq__________#
import requests


dl_limit = 0
def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url
    
def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])        


@Client.on_message(filters.command(["music", "song"]))
async def song(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
 
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("Enter a song name. Check /help")
        return ""
    status = await message.reply("🚀 🔎 🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 𝐭𝐡𝐞 𝐬𝐨𝐧𝐠... 🎶 𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 ⏳️ 𝐅𝐨𝐫 𝐅𝐞𝐰 𝐒𝐞𝐜𝐨𝐧𝐝𝐬 [🚀](https://telegra.ph/file/777939adbee7e24f55d5c.mp4)")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("✖️ 𝐅𝐨𝐮𝐧𝐝 𝐍𝐨𝐭𝐡𝐢𝐧𝐠. 𝐒𝐨𝐫𝐫𝐲.\n\n𝐓𝐫𝐲 𝐀𝐧𝐨𝐭𝐡𝐞𝐫 𝐊𝐞𝐲𝐰𝐨𝐫𝐤 𝐎𝐫 𝐌𝐚𝐲𝐛𝐞 𝐒𝐩𝐞𝐥𝐥 𝐈𝐭 𝐏𝐫𝐨𝐩𝐞𝐫𝐥𝐲.\n\nEg.`/song Faded`")
        return ""
    yt = YouTube(video_link)
    results = []
    count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
    thumbnail = results[0]["thumbnails"][0]
    audio = yt.streams.filter(only_audio=True).first()
    thumb_name = f'thumb{message.message_id}.jpg' 
    thumb = requests.get(thumbnail, allow_redirects=True)
    try:
        
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Failed to download song 😶")
        
        return ""
    rename = os.rename(download, f"{str(user_id)}.mp3")
    await client.send_chat_action(message.chat.id, "upload_audio")
    await client.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        thumb=thumb_name,
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")
            

    
  









def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))

