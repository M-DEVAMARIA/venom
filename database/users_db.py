# https://github.com/odysseusmax/animated-lamp/blob/master/bot/database/database.py
import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI, DATABASE_NAME2

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups
  
        self.cache = {}

    def new_user(self, id, name):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
        )


    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
            configs = dict(
                spellcheck=True,
                max_pages=10,
                max_results=50,
                autofilter=True,
                delete=False,
                delete_time=3600,
                pm_fchat=True,
                advance=True,
                imDb=True
            ),
        )
    def updatec(self, id):
        return dict(
            configs = dict(
                spellcheck=True,
                max_pages=5,
                max_results=50,
                autofilter=True,
                pm_fchat=True,
                advance=True,
                imDb=True
            )
        )
            
    async def add_user(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
    
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
    
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id':int(id)})
        if not user:
            return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return self.col.find({})
    

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})


    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        chats = self.grp.find({'chat_status.is_disabled': True})
        b_chats = [chat['id'] async for chat in chats]
        b_users = [user['id'] async for user in users]
        return b_users, b_chats
    


    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)
        await self.refresh_cache(chat)
        
    async def update(self, id, configs):
       # chat = await self.grp.find_one({'id': id})
        c = await self.grp.insert_one({'_id': id},{'configs': configs})
        await self.refresh_cache(int(id))
    

    async def get_chat(self, chat: int):
        chat = await self.grp.find_one({'id':int(chat)})
        if not chat:
            return False
        else:
            return chat.get('chat_status', 'configs')
    

    async def re_enable_chat(self, id):
        chat_status=dict(
            is_disabled=False,
            reason="",
            )
        await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
    

    async def disable_chat(self, chat, reason="No Reason"):
        chat_status=dict(
            is_disabled=True,
            reason=reason,
            )
        await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
    

    async def total_chat_count(self):
        count = await self.grp.count_documents({})
        return count
    

    async def get_all_chats(self):
        return self.grp.find({})


    async def get_db_size(self):
        return (await self.db.command("dbstats"))['dataSize']

#=====================stng====================

    async def update_configs(self, chat: int, configs):
        """
        A Funtion to update a chat's configs in db
        """
        prev = await self.grp.find_one({"id": chat})

        if prev:
            try:
                await self.grp.update_one(prev, {"$set":{"configs": configs}})
                await self.refresh_cache(chat)
                return True
            
            except Exception as e:
                print (e)
                return False
        print("You Should First Connect To A Chat To Use This")
        return False 
    
    async def refresh_cache(self, id: int):
        """
        A Funtion to refresh a chat's chase data
        in case of update in db
        """
        if self.cache.get(str(id)):
            self.cache.pop(str(id))
        
        prev = await self.grp.find_one({"id": id})
        
        if prev:
            self.cache[str(id)] = prev
        return True 
    async def find_chat(self, chat: int):
        """
        A funtion to fetch a group's settings
        """
        connections = self.cache.get(str(chat))
        
        if connections is not None:
            return connections

        connections = await self.grp.find_one({'id': chat})
        
        if connections:
            self.cache[str(chat)] = connections

            return connections
        else: 
            return self.new_group(None, None)
        
db = Database(DATABASE_URI, DATABASE_NAME)

