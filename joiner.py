import asyncio,os,sys,json
from pymongo import MongoClient
from telethon import TelegramClient
from telethon.sessions import StringSession
from dotenv import load_dotenv
from cprint import cprint
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import PeerChannel

load_dotenv(override=True)

API_ID = os.getenv('TG_API_ID')
API_HASH = os.getenv('TG_API_HASH')
MONGODB_URL = os.getenv('MONGODB_URL')
SLEEP = int(os.getenv('SLEEP'))

async def main():
    channel = {
        'hash': 'BJ6dxkkNrXhmYmM1',
        'id': 1633336636,
    }
    join = True
    # with open('sessions', 'w') as joined:
        # mongoDBClient = MongoClient(MONGODB_URL)
        # table = mongoDBClient.telebot.usrdump
        # for document in table.find():
            # joined.write(document['session']+'\n')
    sessions = open('sessions', 'r')
    joined = open('sessions-joined', 'w' if join else 'r')
    id_list = []
    for session in (sessions if join else joined):
        session = session.strip()
        client = TelegramClient(StringSession(session), API_ID, API_HASH)
        await client.connect()
        authorized = await client.is_user_authorized()
        if not authorized:
            await client.disconnect()
            cprint('red', 'session expired')
            continue
        try:
            me = await client.get_me()
            if me.id in id_list:
                continue
            id_list.append(me.id)
            if join:
                result = await client(ImportChatInviteRequest(channel['hash']))
                print(result.chats[0].id)
                await asyncio.sleep(SLEEP)
                joined.write(session+'\n')
            else:
                await client.delete_dialog(PeerChannel(channel['id']))
            cprint('green', me.first_name, me.last_name, 'joined' if join else 'left')
            await client.disconnect()
        except Exception as e:
            await client.disconnect()
            cprint('red', repr(e))
        await asyncio.sleep(2)
    sessions.close()
    joined.close()

try:
    asyncio.run(main())
except:
    pass