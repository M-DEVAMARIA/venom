import motor.motor_asyncio
from info import DATABASE_NAME, DATABASE_URI

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users
        self.grp = self.db.groups

#_________total users _______________#
    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count
      
#_________all users___________________#
    async def get_all_users(self):
        return self.col.find({})
    
    
db=Database(DATABASE_URL, DATABASE_NAME)    
