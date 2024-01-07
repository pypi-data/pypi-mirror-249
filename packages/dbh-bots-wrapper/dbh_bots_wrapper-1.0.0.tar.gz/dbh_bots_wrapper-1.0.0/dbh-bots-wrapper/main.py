# dbhwrapper/main.py

from . import session

class bot(object):
    def __init__(
        self, 
        discord_id:str, 
        owner_id:str,
        api_key:str,
        name:str=None,
        avatar:str=None,
        users:int=None,
        guilds:int=None,
        shards:int=None
        ):
        self.discord_id = discord_id
        self.owner_id = owner_id
        self.api_key = api_key
        self.name = name
        self.avatar = avatar
        self.users = users
        self.guilds = guilds
        self.shards = shards

    def info(self):
        return {
            'discord_id': self.discord_id,
            'owner_id': self.owner_id,
            'api_key': self.api_key,
            'name': self.name,
            'avatar': self.avatar,
            'users': self.users,
            'guilds': self.guilds,
            'shards': self.shards
            }
            
    def status(self):
        res = session.get("https://bot-api.danbot.host/")
        return { res.message }
        
    def add_bot(self):
        data = {            
            'discord_id': self.discord_id,
            'owner_id': self.owner_id,
            'api_key': self.api_key,
            'name': self.name,
            'avatar': self.avatar,
            'users': self.users,
            'guilds': self.guilds,
            'shards': self.shards
        }
        try:
            res = session.post("https://bot-api.danbot.host/addbot", data)
            res.raise_for_status()
            return res.result
        except requests.exceptions.HTTPError as errh: 
            print("HTTP Error") 
            print(errh.args[0]) 

    def get_bot(self):
        try:
            res = session.get(f'https://bot-api.danbot.host/bot?discord_id={self.discord_id}&user_id={self.owner_id}&api_key={self.api_key}')
            res.raise_for_status() 
            return res.result
        except requests.exceptions.HTTPError as errh: 
            print("HTTP Error") 
            print(errh.args[0]) 

    def get_bots(self):
        try:
            res = session.get(f'https://bot-api.danbot.host/bots?discord_id={self.discord_id}&user_id={self.owner_id}&api_key={self.api_key}')
            res.raise_for_status() 
            return res.result
        except requests.exceptions.HTTPError as errh: 
            print("HTTP Error") 
            print(errh.args[0]) 
