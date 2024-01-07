"""A bot to control settings for tgcf live mode."""

import re
import time
import yaml
import logging

from telethon import events, Button

from test_tele import config
from test_tele.bot.bot_header import (
    get_entity,
    start_sending, 
    loop_message
)
from test_tele.bot.utils import (
    admin_protect,
    display_forwards,
    get_args,
    get_command_prefix,
    get_command_suffix,
    remove_source
)
from test_tele.config import CONFIG, write_config
from test_tele.config_bot import BOT_CONFIG, UserBot, write_bot_config
from test_tele.plugin_models import Style
from test_tele.plugins import TgcfMessage

from telethon import errors
from telethon.tl.functions.messages import (
    SetInlineBotResultsRequest, SendMultiMediaRequest, SetTypingRequest,
    UploadMediaRequest
)
from telethon.tl.types import (
    InputBotInlineResult, InputPhoto, InputMediaPhoto, InputSingleMedia, InputDocument,
    InputMediaPhotoExternal, InputMediaDocument, InputMediaDocumentExternal, SendMessageUploadDocumentAction,
    InputBotInlineMessageMediaAuto, InputWebDocument, SendMessageUploadPhotoAction
)


@admin_protect
async def forward_command_handler(event):
    """Handle the `/forward` command."""
    notes = """The `/forward` command allows you to add a new forward.
    Example: suppose you want to forward from a to (b and c)

    ```
    /forward source: a
    dest: [b,c]
    ```

    a,b,c are chat ids

    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n{display_forwards(config.CONFIG.forwards)}")

        parsed_args = yaml.safe_load(args)
        forward = config.Forward(**parsed_args)
        try:
            remove_source(forward.source, config.CONFIG.forwards)
        except:
            pass
        CONFIG.forwards.append(forward)
        config.from_to, config.reply_to = await config.load_from_to(event.client, config.CONFIG.forwards)

        await event.respond("Success")
        write_config(config.CONFIG)
    except ValueError as err:
        await event.respond(str(err))

    finally:
        raise events.StopPropagation


@admin_protect
async def remove_command_handler(event):
    """Handle the /remove command."""
    notes = """The `/remove` command allows you to remove a source from forwarding.
    Example: Suppose you want to remove the channel with id -100, then run

    `/remove source: -100`

    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n{display_forwards(config.CONFIG.forwards)}")

        parsed_args = yaml.safe_load(args)
        source_to_remove = parsed_args.get("source")
        CONFIG.forwards = remove_source(source_to_remove, config.CONFIG.forwards)
        config.from_to, config.reply_to = await config.load_from_to(event.client, config.CONFIG.forwards)

        await event.respond("Success")
        write_config(config.CONFIG)
    except ValueError as err:
        await event.respond(str(err))

    finally:
        raise events.StopPropagation


@admin_protect
async def style_command_handler(event):
    """Handle the /style command"""
    notes = """This command is used to set the style of the messages to be forwarded.

    Example: `/style bold`

    Options are preserve,normal,bold,italics,code, strike

    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n")
        _valid = [item.value for item in Style]
        if args not in _valid:
            raise ValueError(f"Invalid style. Choose from {_valid}")
        CONFIG.plugins.fmt.style = args
        await event.respond("Success")
        write_config(CONFIG)
    except ValueError as err:
        await event.respond(str(err))

    finally:
        raise events.StopPropagation


async def start_command_handler(event):
    """Handle the /start command"""

    if not event.message.chat_id in [item.user_id for item in BOT_CONFIG.user_cfg]:
        user_cfg = UserBot(user_id=event.message.chat_id)
        BOT_CONFIG.user_cfg.append(user_cfg)
        write_bot_config(BOT_CONFIG)

    await event.respond(BOT_CONFIG.bot_messages.start)


async def help_command_handler(event):
    """Handle the /help command."""
    await event.respond(BOT_CONFIG.bot_messages.bot_help)


async def get_message_command_handler(event):
    """Handle the command /get"""
    notes = """This command is used to retrieve messages from a public channel or group even if forwarding is not allowed.

    Command: `/get`
    Usage: LINK..
    Note: copy the message link from the public channel or group, and paste it here as argument
    
    **Example** 
    `/get https://t.me/username/post_id`
    """.replace("    ", "")

    try:
        args = get_args(event.message.text)

        if not args:
            raise ValueError(f"{notes}\n")

        pattern = r'(t.me/(c/)?|)(-?\w+)/(\d+)'
        match = re.search(pattern, args)

        tm = TgcfMessage(event.message)

        if match:
            entity = str(match.group(3))
            ids = int(match.group(4))
            chat = await get_entity(event, entity)

            if chat is None:
                raise ValueError("Unable to get post")

            message = await event.client.get_messages(chat, ids=ids)            
            tm.text = message.message
            caption = tm.text + f"\n\n👉 {BOT_CONFIG.bot_name} 👈"

            if message.grouped_id is not None and message.media:
                from test_tele.live_pyrogram import APP as app
                await app.copy_media_group(
                    tm.message.chat_id, 
                    chat.username, 
                    message.id, 
                    disable_notification=True,
                    captions=caption, 
                )
            elif message.grouped_id is None and message.media:
                from test_tele.live_pyrogram import APP as app
                await app.copy_message(
                    tm.message.chat_id, 
                    chat.username, 
                    message.id, 
                    disable_notification=True,
                    caption=caption, 
                )

    except ValueError as err:
        await event.respond(str(err))

    except Exception as err:
        logging.error(err)

    finally:
        raise events.StopPropagation


async def get_id_command_handler(event):
    """Handle the /id command"""

    try:
        args = get_args(event.message.text)

        if not args and CONFIG.login.user_type == 1:
            tm = TgcfMessage(event.message)
            tm.text = ""
            i = 0

            async for dialog in event.client.iter_dialogs():
                if dialog.is_channel:
                    i += 1
                    if i <= 80:
                        ch_id = f"`{str(dialog.id)}`"
                        ch_name = str(dialog.name).replace("`", "'")
                        tm.text += ch_id + " 👉 " + ch_name + "\n"
                    else:
                        await start_sending(tm.message.chat_id, tm)
                        tm.text = ""
                        i = 0
            
            await start_sending(tm.message.chat_id, tm)

        message = await event.message.get_reply_message()
        await event.respond(f"```{message.stringify()}```")

    except Exception as err:
        logging.error(err)
        message = await event.message.get_reply_message()
        await event.respond(f"```{message.stringify()}```")

    finally:
        raise events.StopPropagation


async def report_command_handler(event):
    """Handle the /report command"""
    notes = """The `/report` command allows you to send a message to the bot Admin.

    Command: `/report`
    Usage: MESSAGE..

    **Example**
    `/report Bot is not responding. Not sure if you received this or not.. lol`
    """.replace(
        "    ", ""
    )

    try:
        args = get_args(event.message.text)
        if not args:
            raise ValueError(f"{notes}\n")
        
        tm = TgcfMessage(event.message)
        tm.text = f"**-= New Message =-**\nfrom: `{tm.message.chat_id}`\n———————————\n" + args
        tm.text += f"\n———————————\n#report"

        await start_sending(CONFIG.admins[0], tm)
        await event.respond("We have received your message. Please wait while the Admin attempts to fix it")
        
    except ValueError as err:
        await event.respond(str(err))
    finally:
        raise events.StopPropagation


@admin_protect
async def respond_command_handler(event):
    """Handle the /reply command handler"""
    
    try:
        args = get_args(event.message.text)
        if not args:
            return

        tm = TgcfMessage(event.message)
        
        matches = re.match(r'(\d+)\s(.+)', args, re.DOTALL)
        id_user = matches.group(1)
        isi_pesan = matches.group(2)

        tm.text = f'Admin says: "{isi_pesan}"'
        await start_sending(int(id_user), tm)

    except Exception as err:
        logging.error(err)
    finally:
        raise events.StopPropagation


async def callback_get_message(event):
    """Handle callback for get messages"""
    try:
        pattern = r'gt(?:p|n)_(\w+)_(\d+)'
        text = event.data.decode('utf-8')
        match = re.match(pattern, text)
        id_post = 2

        if match:
            ent_chnl = match.group(1)
            id_post = int(match.group(2))

            if text.startswith("gtp_"):
                id_post -= 1
                message = await loop_message(event, ent_chnl, id_post, False)
            if text.startswith("gtn_"):
                id_post += 1
                message = await loop_message(event, ent_chnl, id_post)

            id_msg = message.id
            msg_text = message.text + f"\n\n👉 {BOT_CONFIG.bot_name} 👈 | `t.me/{ent_chnl}/{id_msg}`"
            return await event.edit(text=msg_text, file=message.media, buttons=[
                                Button.inline('◀️', f'gtp_{ent_chnl}_{id_msg}'),
                                Button.inline('▶️', f'gtn_{ent_chnl}_{id_msg}')
                            ])

    except Exception as err:
        logging.error(err)
    finally:
        raise events.StopPropagation


async def advanced_get_message_command_handler(event):
    """Handle new incoming post link message"""
    try:
        pattern = r'(?:t\.me/|@)(\w+)(?:/(\d+))?' 
        if match := re.search(pattern, event.message.text):
            entity, ids = match.groups()
            ids = int(ids) if ids else 2
        else:
            return

        # username = await get_entity(event, entity)
        username = entity
        message = await loop_message(event, username, ids)

        if message:
            ids = message.id
            message.text += f"\n\n👉 {BOT_CONFIG.bot_name} 👈 | `t.me/{username}/{ids}`"
            return await event.client.send_message(event.message.chat_id, message, buttons=[
                                Button.inline('◀️', f'gtp_{username}_{ids}'),
                                Button.inline('▶️', f'gtn_{username}_{ids}')
                            ])
        return

    except Exception as err:
        logging.error(err)
    finally:
        raise events.StopPropagation


async def get_images_from_inline(event):
    query = event.message.text
    category = query.split()[0]

    logging.warning("mode : %s", category)
    
    if query.startswith('.px'):
        from test_tele.extractors.pixiv import get_pixiv_list, clean_up_tags, PIXIV_MODE
        px_mode, keywords = await clean_up_tags('no_inline ' + event.message.text, PIXIV_MODE, '.px')
        limit = px_mode.get('limit', 30)
        offset = px_mode.get('offset', 0)
        as_file = px_mode.get('as_file', False)

    n = 0
    img_slice = 10
    chat_id = event.input_chat

    if query.startswith('.px'):
        lists = await get_pixiv_list(keywords, offset)

    if not lists:
        return

    try:
        for i in range(0, len(lists), img_slice):
            media_to_send = []
            await event.client(SetTypingRequest(chat_id, SendMessageUploadPhotoAction(0)))
            
            for chunk in lists[i:i + img_slice]:
                n += 1
                if n > int(limit):
                    break
                    
                start = time.time()
                try:
                    if category == '.px':
                        img_url = chunk['img_urls']['img_original']
                    ttl_seconds = 86000
                    if as_file:
                        media = await event.client(UploadMediaRequest(chat_id, InputMediaDocumentExternal(img_url, ttl_seconds=ttl_seconds)))
                        input_media = InputSingleMedia(InputMediaDocument(InputDocument(media.photo.id, media.photo.access_hash, b'')), '')
                    else:
                        media = await event.client(UploadMediaRequest(chat_id, InputMediaPhotoExternal(img_url, ttl_seconds=ttl_seconds)))
                        input_media = InputSingleMedia(InputMediaPhoto(InputPhoto(media.photo.id, media.photo.access_hash, b'')), '')
                    media_to_send.append(input_media)
                    
                except errors.MultiError as e:
                    logging.warning("UploadMedia returned one or more errors")
                    logging.debug('error: %s', e, exc_info=True)
                    
                    if not any(e.results):
                        logging.exception("All UploadMedia requests failed")
                        return
                    media_to_send += filter(None, e.results)
                logging.warning("lama upload: %s", time.time() - start)

            try:
                await event.client(SendMultiMediaRequest(chat_id, media_to_send))
            except errors.FloodWaitError as e:
                logging.warning(f"Got FloodWait error: {e.seconds}, {e}")
                time.sleep(3)
                await event.client(SendMultiMediaRequest(chat_id, media_to_send, silent=True, background=True))
            except errors.WebpageCurlFailedError:
                continue
            except Exception:
                continue

    except Exception as err:
        logging.error(err)

    finally:
        raise events.StopPropagation


def get_events(val): # tambah argumen
    logging.info(f"Command prefix is . for userbot and / for bot")
    _ = get_command_prefix(val)
    u = get_command_suffix(val)
    command_events = {
        "start": (start_command_handler, events.NewMessage(pattern=f"{_}start{u}")),
        "forward": (forward_command_handler, events.NewMessage(pattern=f"{_}forward")),
        "remove": (remove_command_handler, events.NewMessage(pattern=f"{_}remove")),
        "style": (style_command_handler, events.NewMessage(pattern=f"{_}style")),
        "help": (help_command_handler, events.NewMessage(pattern=f"{_}help{u}")),
        "get_id": (get_id_command_handler, events.NewMessage(pattern=f"{_}id{u}")),
    }
    if val == 0: # bot
        khusus_bot= {
            "report": (report_command_handler, events.NewMessage(pattern=f"{_}report")),
            "reply": (respond_command_handler, events.NewMessage(pattern=f"{_}reply")),
            "get_post": (get_message_command_handler, events.NewMessage(pattern=f"{_}get")),
            "get_images": (get_images_from_inline, events.NewMessage(pattern=r".(?:px)")),
            "adv_get_post": (advanced_get_message_command_handler, events.NewMessage(pattern=r'(?:https?://)?(?:t.me\/|@)(\w+)')),
            "cb_get_post": (callback_get_message, events.CallbackQuery(pattern=r'gt(?:p|n)_')),
        }
        command_events.update(khusus_bot)

    return command_events

