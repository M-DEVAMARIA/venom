import asyncio
from pyrogram import Client, filters
import datetime
import time 
from info import ADMINS, BROADCAST_CHANNEL as LOG_CHANNEL
#broadcast 
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from database.users_db import db
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

    
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
            if sh == "Blocked":
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

async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Succes"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"
        
@Client.on_message(filters.command("gbroadcast") & filters.user(ADMINS))
async def chatverupikkals(bot, message):
    users = await db.get_all_chats() 
   # user =  int(users['id']) 
    done=0
    half=0
    start_time = time.time()
    async for chat in users:
        user =  int(chat['id'])
        new = dict(
          spellcheck=True,
          max_pages=10,
          max_results=10,
          autofilter=True,
          delete=False,
          delete_time=3600,
          pm_fchat=True,
          callback=False,
          advance=True,
          welcome=True,
          protect=False,
          spell_template=None,
          imdb_template=None,
          imDb=True)

        k = await db.update_configs(user, new)
        if not k:
           await db.update(int(user), new)  
        else:
           try:
             link = (await bot.create_chat_invite_link(chat_id)).invite_link
             await message.reply_text(f"#updated\nupdated a chat\nID: {user}\nwith new {new}\ninvie link: {link}")
           except ChatAdminRequired:
             link ="im not admin in that chat"
             await message.reply_text(f"#updated\nupdated a chat\nID: {user}\nwith new {new}\ninvite link: {link}")
           except Exception as e:
             link = e
             await message.reply_text(f"#updated\nupdated a chat\nID: {user}\nwith new {new}\ninvite link: {link}")
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))          
    await message.reply_text(f"successfully completed within: {time_taken}")

@Client.on_message(filters.command("refresh"))
async def refresh(bot, message):
    users = await db.get_all_chats() 
    user = message.chat.id 
    cmd = message
    if not await db.get_chat(cmd.chat.id):
            total=await bot.get_chat_members_count(cmd.chat.id)
            channel_id = cmd.chat.id
            group_id = cmd.chat.id
            title = cmd.chat.title
            await db.add_chat(cmd.chat.id, cmd.chat.title) 
            return await bot.send_message(LOG_CHANNEL, f"#NEWGROUP \n\nGroup Name -  [{cmd.chat.title}]\nGroup id - {cmd.chat.id}\nTotal members = [{total}]\nAdded by - 'Unknown'")
              
    new = dict(
          spellcheck=True,
          max_pages=10,
          max_results=10,
          autofilter=True,
          delete=False,
          delete_time=3600,
          pm_fchat=True,
          callback=False,
          advance=True,
          welcome=True,
          protect=False,
          spell_template=None,
          imdb_template=None,
          imDb=True)
    append = await db.update_configs(user, new)
    if append: 
       #await db.update(int(user), new)
       text=" group settings refreshed."
       await message.reply_text(text=text)
