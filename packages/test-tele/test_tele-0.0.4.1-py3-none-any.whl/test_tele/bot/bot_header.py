import json
import shlex
import asyncio

from typing import TYPE_CHECKING
from telethon.tl import types

from test_tele.utils import start_sending

if TYPE_CHECKING:
    from test_tele.plugins import TgcfMessage


## Helper function for get_message
    
async def get_entity(event, entity):
    """Get chat entity from entity parameter"""
    if entity.isdigit() or entity.startswith("-"):
        chat = types.PeerChannel(int(entity))
    else:
        try:
            chat = await event.client.get_entity(entity)
        except Exception as e:
            chat = await event.client.get_entity(types.PeerChat(int(entity)))

    return chat


async def loop_message(event, chat, ids: int, next=True):
    """Loop channel posts to get message"""
    skip = 20
    tries = 0
    while True:
        if ids > 0 and tries <= skip:
            message = await event.client.get_messages(chat, ids=ids)
            tries += 1
            if not message:
                if next:
                    ids += 1
                    continue
                else:
                    ids -= 1
                    continue
            else:
                if hasattr(message, 'message'):
                    if message.media and not (message.sticker or message.voice or message.web_preview):
                        return message
                ids = ids + 1 if next else ids - 1
        else:
            return


## E-Hen.. 
async def get_doujins(event):
    """Get doujins detail from given link"""
    tm = TgcfMessage(event.message)
    tm.text = ""

    command = shlex.split(f"gallery-dl {event.message.text} --config-ignore -c config/config.json -j --range 1-5")
    # print(*command)

    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await process.communicate()

    if stderr:
        print(stderr.decode())
    else:
        links = []
        result = json.loads(stdout.decode())

        for elemen in result:
            if elemen[0] == 3:
                links.append(elemen[1])
                # tm.text += elemen[1] + "\n"
        
        tm.new_file = links
        await start_sending(tm.message.chat_id, tm)



