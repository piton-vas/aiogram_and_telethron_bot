import asyncio

from telethon import TelegramClient, sync, events
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

import os
from dotenv import load_dotenv
load_dotenv('.venv/.env')
telethon_api_id = os.getenv('telethon_api_id')
telethon_api_hash = os.getenv('telethon_api_hash')

client = TelegramClient('session_name', telethon_api_id, telethon_api_hash)




# send_to_china_get_slow_response('Что такое обеспечение контракта?')




@client.on(events.NewMessage(chats=('v_karpyuk')))
async def normal_handler(event):
    # print(event.message.to_dict())
    # print("Го")
    # if event.message.to_dict() == "Го":
    send_message_id = client.send_message('neuro44fz_bot', 'Что такое обеспечение контракта?')
    await asyncio.sleep(5)
    print(send_message_id)

@client.on(events.MessageEdited(chats=('neuro44fz_bot')))
async def normal_handler(event):
    # print(event.message.to_dict())   #.message.to_dict()['message']
    pass

# print(client.send_message('neuro44fz_bot', 'Что такое обеспечение контракта?'))

client.start()

def send_to_china_get_slow_response(request_text):
    request_message = client.send_message('neuro44fz_bot', request_text)

# send_to_china_get_slow_response('Что такое обеспечение контракта?')



client.run_until_disconnected()



