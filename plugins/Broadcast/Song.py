import aiofiles
import aiohttp
import wget
import yt_dlp as youtube_dl
from pyrogram import filters
from pyrogram.types import Message
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL





@Client.on_message(filters.command(["music", "song"]))
async def ytmusic(client, message: Message):
    urlissed = get_text(message)
    if not urlissed:
        await client.send_message(
            message.chat.id,
            "Invalid Command Syntax, Please Check Help Menu To Know More!",
        )
        return
    global dl_limit
    if dl_limit >= 4:
        await message.reply_text(
            "Daisy's server busy due to too many downloads, try again after sometime."
        )
        return
    pablo = await client.send_message(
        message.chat.id, f"`Getting {urlissed} From Youtube Servers. Please Wait.`"
    )
    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    try:
        mi = search.result()
        mio = mi["search_result"]
        mo = mio[0]["link"]
        mio[0]["duration"]
        thum = mio[0]["title"]
        fridayz = mio[0]["id"]
        thums = mio[0]["channel"]
        kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    except:
        await message.reply_text(
            "Sorry I accounted an error.\n Unkown error raised while getting search result"
        )
        return

    await asyncio.sleep(0.6)
    sedlyf = wget.download(kekme)
    opts = {
        "format": "bestaudio",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "writethumbnail": True,
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "720",
            }
        ],
        "outtmpl": "%(id)s.mp3",
        "quiet": True,
        "logtostderr": False,
    }
    try:
        dl_limit = dl_limit + 1
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(mo, download=True)

    except Exception as e:
        await pablo.edit(f"**Failed To Download** \n**Error :** `{str(e)}`")
        # dl_limit = dl_limit-1
        return
    c_time = time.time()
    capy = f"**Song Name :** `{thum}` \n**Requested For :** `{urlissed}` \n**Channel :** `{thums}` \n**Link :** `{mo}`"
    file_stark = f"{ytdl_data['id']}.mp3"
    try:
        await client.send_audio(
            message.chat.id,
            audio=open(file_stark, "rb"),
            duration=int(ytdl_data["duration"]),
            title=str(ytdl_data["title"]),
            performer=str(ytdl_data["uploader"]),
            thumb=sedlyf,
            caption=capy,
            progress=progress,
            progress_args=(
                pablo,
                c_time,
                f"`Uploading {urlissed} Song From YouTube Music!`",
                file_stark,
            ),
        )
        dl_limit = dl_limit - 1
    except:
        dl_limit = dl_limit - 1
        return
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)


ydl_opts = {
    "format": "bestaudio/best",
    "writethumbnail": True,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}


def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


# Funtion To Download Song
async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return song_name

is_downloading = False


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))
