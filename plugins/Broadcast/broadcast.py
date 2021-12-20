import asyncio
from pyrogram import Client, filters
import datetime
import time 
from info import ADMINS 
#broadcast 
from utils import broadcast_messages
from database.users_db import db

        
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
# https://t.me/GetTGLink/4178
async def verupikkals(bot, message):
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    sts = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed =0

    success = 0
    async for user in users:
        pti, sh = await broadcast_messages(int(user['id']), b_msg)
        if pti:
            success += 1
        elif pti == False:
            if sh == "Bocked":
                blocked+=1
            elif sh == "Deleted":
                deleted += 1
            elif sh == "Error":
                failed += 1
        done += 1
        await asyncio.sleep(2)
        if not done % 20:
            await sts.edit(f"Broadcast in progress:\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.edit(f"Broadcast Completed:\nCompleted in {time_taken} seconds.\n\nTotal Users {total_users}\nCompleted: {done} / {total_users}\nSuccess: {success}\nBlocked: {blocked}\nDeleted: {deleted}")

        
@Client.on_message(filters.command("gbroadcast") & filters.user(ADMINS))
async def chatverupikkals(bot, message):
    users = await db.get_all_chats() 
   # user =  int(users['id']) 
    async for chat in users:
        user =  int(chat['id'])
        new = dict(
          spellcheck=True,
          max_pages=True,
          max_results=True,
          autofilter=True,
          pm_fchat=True,
          imDb=True)
    await db.update_configs(user, new)

@Client.on_message(filters.command("/refresh") & filters.user(ADMINS))
async def refresh(bot, message):
    users = await db.get_all_chats() 
    user = message.message.chat.id 
   # async for chat in users:
      #  user =  int(chat['id'])
        new = dict(
          spellcheck=True,
          max_pages=True,
          max_results=True,
          autofilter=True,
          pm_fchat=True,
          imDb=True)
    await db.update_configs(user, new)
