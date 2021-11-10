import re
from os import environ

id_pattern = re.compile(r'^.\d+$')

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

# bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', False))

#force sub & restrict users
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else auth_channel

#broadcast db
BROADCAST_CHANNEL = int(os.environ.get("BROADCAST_CHANNEL", "-1001553356176"))
