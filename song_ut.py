
from os import enviorn
from Python_ARQ import ARQ
from pyrogram import Client
import aiofiles
import aiohttp
import ffmpeg
import requests
import wget

ARQ_API_KEY = getenv("ARQ_API_KEY", None)
aiohttpsession = aiohttp.ClientSession()
chat_id = None
arq = ARQ("https://thearq.tech", ARQ_API_KEY, aiohttpsession)
