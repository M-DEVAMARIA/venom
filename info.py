import re, time
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default
    
# Bot information 
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']
SESSION = environ.get('SESSION', 'Media_search')

# Admins & channels
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ['CHANNELS'].split()]

# MongoDB information

DATABASE_URI = environ.get('DATABASE_URI', 'mongodb+srv://M_dautofilterv3:M_dautofilterv3@cluster0.wzriv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
DATABASE_NAME = environ.get('DATABASE_NAME', 'Md_movies')
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')
DATABASE_NAME2 = environ.get('DATABASE_NAME2', 'users')
# bot settings
IMDB = is_enabled((environ.get('IMDB', "True")), True)
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
#force sub & restrict users
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel

#broadcast db
BROADCAST_CHANNEL = int(environ.get("BROADCAST_CHANNEL", -1001553356176))
PHOTO = (environ.get("PHOTOS", "https://telegra.ph/file/0ea48259dee162a3f1af5.jpg https://telegra.ph/file/521928a593ee7f6317148.jpg https://telegra.ph/file/2de25e9b92952e71a38fe.jpg https://telegra.ph/file/43e0475c64c6e62620cde.jpg https://telegra.ph/file/8b19847ac853a1acd6fad.jpg https://telegra.ph/file/695f80d49d3d1c854880a.jpg https://telegra.ph/file/068e8dbd8024340fa003c.jpg https://telegra.ph/file/d0aa3ce797458642782d6.jpg https://telegra.ph/file/2c1835c35522fea3ee110.jpg https://telegra.ph/file/b005f398d96344f4e9a08.jpg https://telegra.ph/file/43d0782de5d7ef269faed.jpg https://telegra.ph/file/8f990e11a9bfc24e35a8c.jpg")).split()
start_uptime = time.time()
# for main filter.py
IMDB_TEMPLATEF = environ.get("IMDB_TEMPLATEF", "674a4381")
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Query: {query}</b> \n‌‌‌‌IMDb Data:\n\n🏷 Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n📆 Year: <a href={url}/releaseinfo>{year}</a>\n🌟 Rating: <a href={url}/ratings>{rating}</a> / 10")
BUTTON = environ.get("BUTTON",False)
OMDB_API_KEY = environ.get("OMDB_API_KEY", "674a4381")
if OMDB_API_KEY.strip() == "":
    API_KEY=None
else:
    API_KEY=OMDB_API_KEY
    
FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "")
if FILE_CAPTION.strip() == "":
    CUSTOM_FILE_CAPTION=None
else:
    CUSTOM_FILE_CAPTION=FILE_CAPTION
AUTH_GROUPS = [int(admin) for admin in environ.get("AUTH_GROUPS", "").split()]
