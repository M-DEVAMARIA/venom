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
