"""The module responsible for operating tgcf in live mode."""

import re
import sys
import logging
from typing import Union

from telethon import TelegramClient, events, functions, types
from telethon.sessions import StringSession
from telethon.tl.custom.message import Message

from test_tele import config, const
from test_tele import storage as st
from test_tele.bot import get_events
from test_tele.config import CONFIG, get_SESSION
from test_tele.plugins import apply_plugins
from test_tele.utils import clean_session_files, send_message


async def new_message_handler(event: Union[Message, events.Album, events.NewMessage]) -> None:
    """Process new incoming messages."""
    chat_id = event.chat_id

    if chat_id not in config.from_to:
        return
    
    if event.grouped_id != None:
        logging.info(f"Album tetep kedetesi sebagai new message {chat_id}")
        return

    logging.info(f"New message received in {chat_id}")
    message = event.message

    event_uid = st.EventUid(event)

    length = len(st.stored)
    exceeding = length - const.KEEP_LAST_MANY

    if exceeding > 0:
        for key in st.stored:
            del st.stored[key]
            break

    dest = config.from_to.get(chat_id)
    rpl = config.reply_to[chat_id]

    tm = await apply_plugins(message)
    if not tm:
        return

    if event.is_reply:
        r_event = st.DummyEvent(chat_id, event.reply_to_msg_id)
        r_event_uid = st.EventUid(r_event)
        
    st.stored[event_uid] = {}
    for i, d in enumerate(dest):
        if event.is_reply and r_event_uid in st.stored:
            tm.reply_to = st.stored.get(r_event_uid).get(d)
        if rpl and rpl[i] != 0 and not event.is_reply:
            tm.reply_to = rpl[i]
        fwded_msg = await send_message(d, tm)
        st.stored[event_uid].update({d: fwded_msg})

        # if CONFIG.plugins.special.check and CONFIG.plugins.special.download:
        #     link_regex = re.compile(r"https?://\S+")
        #     link = re.findall(link_regex, tm.text)
        #     if link:
        #         tm.reply_to = st.stored.get(event_uid).get(d)
        #         tm.text = link[0]
        #         await start_download(d, tm)
    tm.clear()


async def edited_message_handler(event) -> None:
    """Handle message edits."""
    message = event.message

    chat_id = event.chat_id

    if chat_id not in config.from_to:
        return

    logging.info(f"Message edited in {chat_id}")

    event_uid = st.EventUid(event)

    tm = await apply_plugins(message)

    if not tm:
        return

    fwded_msgs = st.stored.get(event_uid)

    if fwded_msgs:
        for _, msg in fwded_msgs.items():
            if config.CONFIG.live.delete_on_edit == message.text:
                await msg.delete()
                await message.delete()
            else:
                await msg.edit(tm.text)
        return

    dest = config.from_to.get(chat_id)
    rpl = config.reply_to[chat_id]

    for i, d in enumerate(dest):
        if rpl and rpl[i] != 0:
            tm.reply_to = rpl[i]
        await send_message(d, tm)
    tm.clear()


async def deleted_message_handler(event):
    """Handle message deletes."""
    chat_id = event.chat_id
    if chat_id not in config.from_to:
        return

    logging.info(f"Message deleted in {chat_id}")

    event_uid = st.EventUid(event)
    fwded_msgs = st.stored.get(event_uid)
    if fwded_msgs:
        for _, msg in fwded_msgs.items():
            await msg.delete()
        return


ALL_EVENTS = {
    "new": (new_message_handler, events.NewMessage()),
    "edited": (edited_message_handler, events.MessageEdited()),
    "deleted": (deleted_message_handler, events.MessageDeleted()),
}


## ================================================ Pyrogram Inline

from pyrogram import filters
from pyrogram.types import InlineQuery, CallbackQuery, Message
from pyrogram.enums import ParseMode

from test_tele.pyrogram.pixiv import inline_pixiv, get_px_file
from test_tele.pyrogram.gelbooru import inline_gelbooru, get_gb_file
from test_tele.pyrogram.tsumino import inline_tsumino, generate_telegraph, cari_konten
from test_tele.pyrogram.pornpics import inline_pornpics, get_pp_file
from test_tele.pyrogram.furry import inline_furry, get_fur_file
from test_tele.pyrogram.vip_vanillarock import inline_vanillarock, get_vr_file

async def run_pyrogram():
    from test_tele.live_pyrogram import APP
    app = APP

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    @app.on_message(filters.text | filters.photo)
    async def incoming_message_handler(app, message: Message):
        """Handle spesific incoming message"""
        try:
            if message.text:
                pattern = r'ID\s\:\s(.+)'
                match = re.search(pattern, message.text)
                if match:
                    telepages = await cari_konten(match.group(1))
                    if not telepages:
                        await generate_telegraph(match.group(1))
            elif message.photo:
                logging.warning("ya ini photo")
                # logging.warning(message.photo)
                
        except Exception as err:
            logging.error(err, exc_info=True)
    

    @app.on_inline_query()
    async def inline_handler(app, inline_query: InlineQuery):
        """Handle inline query search"""
        query_handlers = {
            '.md': inline_tsumino,
            '.px': inline_pixiv,
            '.rp': inline_pornpics,
            '.fur': inline_furry,
            '.2d': inline_vanillarock
        }

        for query_prefix, handler in query_handlers.items():
            if inline_query.query.lower().startswith(query_prefix):
                await handler(app, inline_query)
                break
        else:
            await inline_gelbooru(app, inline_query)


    @app.on_callback_query(filters.regex(r"(?:md|gb|px|rp|fur|2d)"))
    async def callback_query_handler(app, callback_query: CallbackQuery):
        """Get callback query from inline keyboard"""
        handlers = {
            "md": None,
            "gb": get_gb_file,
            "px": get_px_file,
            "rp": get_pp_file,
            "fur": get_fur_file,
            "2d": get_vr_file
        }

        for prefix, handler in handlers.items():
            if callback_query.data.startswith(prefix):
                if prefix == "md":
                    telepages = await cari_konten(callback_query.data.replace(f"{prefix} ", ''))
                    if not telepages:
                        return await app.send_message(callback_query.from_user.id, 'Please wait while the telegraph is being generated')

                    text = f"[{telepages[0]['title']}]({telepages[0]['url']})\nAuthor : {telepages[0]['author_name']}"
                    return await app.send_message(
                        callback_query.from_user.id,
                        text,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_notification=True,
                        protect_content=True
                    )
                else:
                    image_file = await handler(callback_query.data.replace(f"{prefix} ", ''))
                    await app.send_document(callback_query.from_user.id, image_file)
                    break
        else:
            # Handle case when no prefix matches
            pass


    await app.start()

## =================================================== End of pyrogram


async def start_sync() -> None:
    """Start tgcf live sync."""
    # clear past session files
    clean_session_files()

    USER_SESSION = StringSession(CONFIG.login.SESSION_STRING) # tambahan ku
    # SESSION = get_SESSION()
    client = TelegramClient( 
        USER_SESSION,
        CONFIG.login.API_ID,
        CONFIG.login.API_HASH,
        sequential_updates=CONFIG.live.sequential_updates,
    )
    bot_client = TelegramClient( # tambahan ku
        'tgcf_bot',
        CONFIG.login.API_ID,
        CONFIG.login.API_HASH,
        sequential_updates=CONFIG.live.sequential_updates,
    )
    
    if CONFIG.login.user_type == 0: # bot
        if CONFIG.login.BOT_TOKEN == "":
            logging.warning("Bot token not found, but login type is set to bot.")
            sys.exit()
        await bot_client.start(bot_token=CONFIG.login.BOT_TOKEN) # edit variable
    else:
        await client.start()
        await bot_client.start(bot_token=CONFIG.login.BOT_TOKEN) # tambahan ku

    config.is_bot = await bot_client.is_bot()
    logging.info(f"config.is_bot={config.is_bot}")

    await config.load_admins(bot_client)

    if CONFIG.login.user_type == 1: # user
        command_events = get_events(1)
        ALL_EVENTS.update(command_events)
        for key, val in ALL_EVENTS.items():
            if config.CONFIG.live.delete_sync is False and key == "deleted":
                continue
            client.add_event_handler(*val)

    # tambahan ku
    command_events = get_events(0)
    ALL_EVENTS.update(command_events)
    for key, val in ALL_EVENTS.items():
        if config.CONFIG.live.delete_sync is False and key == "deleted":
            continue
        bot_client.add_event_handler(*val)
        logging.info(f"Added event handler for {key}")

    if const.REGISTER_COMMANDS: # config.is_bot and
        await bot_client( # edit variable
            functions.bots.SetBotCommandsRequest(
                scope=types.BotCommandScopeDefault(),
                lang_code="en",
                commands=[
                    types.BotCommand(command=key, description=value)
                    for key, value in const.COMMANDS.items()
                ],
            )
        )
    config.from_to, config.reply_to = await config.load_from_to(client, config.CONFIG.forwards)

    if CONFIG.login.user_type == 1: # user
        await client.run_until_disconnected()
    await bot_client.run_until_disconnected()

