import uuid 
import logging

from pyrogram import enums
from pyrogram.types import InputMediaPhoto, InputMediaDocument
from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)

from .utils import OFFSET_PID, IMG_EXT, GIF_EXT, gallery_dl, get_tags, not_found_msg


async def image_keyboard(query: str, my_list: list[str]) -> InlineKeyboardMarkup:
    buttons = [[
                InlineKeyboardButton("💾" ,
                                     callback_data=f"fur {my_list['category']},{my_list['id_file']}.{my_list['extension']}"),
                InlineKeyboardButton("🔗",
                                     url=f'https://e6ai.net/posts/{my_list["id"]}'),
                InlineKeyboardButton("🔄",
                                     switch_inline_query_current_chat=query),
            ]]
    return InlineKeyboardMarkup(buttons)


async def set_info_dict(gallery_dl_result) -> list[dict]:
    """Set dict based on website"""
    my_dict = {}
    lists: list[my_dict] = []
    
    for elemen in gallery_dl_result:
        if elemen[0] == 3:
            my_dict = {}
            my_dict['img_url'] = elemen[1]
            my_dict['id_file'] = str(elemen[2]['file']['md5'])
            my_dict['id'] = str(elemen[2]['id'])
            my_dict['extension'] = elemen[2]['extension']
            my_dict['category'] = elemen[2]['category']
            my_dict['width'] = elemen[2]['file']['width']
            my_dict['height'] = elemen[2]['file']['height']
            my_dict['artist'] = await get_tags(elemen[2]['tags']['artist']) if 'artist' in elemen[2]['tags'] else "AI"
            my_dict['thumbnail'] = elemen[2]['preview']['url']
            my_dict['tags'] = await get_tags(elemen[2]['tags']['general'], 40)
            lists.append(my_dict)
    return lists


async def set_url(query: str) -> str:
    base_url = "https://e621.net/posts?tags="
    url = str(query).strip().lower().replace(".fur", "").lstrip()

    if "-ai" in url:
        url = url.replace("-ai", '')
        base_url = base_url.replace("e621.net", "e6ai.net")

    # Default = my little pony
    url = "my_little_pony+-penis" if url == "" else url.replace(" ", '+')
    return f"{base_url}{url}"


async def inline_furry(client, inline_query):
    """Show e621 artworks"""
    query = inline_query.query
    if not query:
        return

    offset = inline_query.offset
    pid = int(offset) if offset else 0
        
    url = await set_url(query)
    gallery_dl_result = await gallery_dl(url, pid)
    lists = await set_info_dict(gallery_dl_result)
    results = []

    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)

    if lists:
        try:
            for my_list in lists:
                if my_list['extension'] in GIF_EXT:
                    result = InlineQueryResultAnimation(
                        animation_url=my_list['img_url'],
                        animation_width=my_list['width'],
                        animation_height=my_list['height'],
                        thumb_url=my_list['thumbnail'],
                        id=str(uuid.uuid4()) + my_list['id'][:3],
                        caption=f'Artist : {my_list["artist"].replace("`", "")}\nTags : {my_list["tags"]}',
                        reply_markup=await image_keyboard(query, my_list),
                    )
                    results.append(result)

                elif my_list['extension'] in IMG_EXT:
                    result = InlineQueryResultPhoto(
                        photo_url=my_list['img_url'],
                        thumb_url=my_list['thumbnail'],
                        photo_width=my_list['width'],
                        photo_height=my_list['height'],
                        id=str(uuid.uuid4()) + my_list['id'][:3],
                        caption=f'Artist : {my_list["artist"].replace("`", "")}\nTags : {my_list["tags"]}',
                        reply_markup=await image_keyboard(query, my_list),
                    )
                    results.append(result)
    
            await client.answer_inline_query(
                inline_query.id,
                results=results,
                cache_time=180,
                is_gallery=True,
                next_offset=str(pid + OFFSET_PID)
            )
        except Exception as err:
            logging.error(err, exc_info=True)


async def get_fur_file(callb_query:str):
    website, file_name = callb_query.split(",")
    modified_string = "{}/{}/{}".format(file_name[:2], file_name[2:4], file_name)
    return f"https://static1.{website}.net/data/{modified_string}"


# Perlu decorator premium
async def upload_fur_batch(app, message):
    query = str(message.text)
    if not query:
        return
    
    pid = 0
    limit = 30
    asfile = False
    img_slice = 10

    input = query.split()
    for i, val in enumerate(input):
        if 'limit:' in val:
            limit = int(val.split("limit:")[-1].strip())
            limit = limit if limit <= 30 else 30
            query = query.replace(val, '')
        if val.isdigit():
            pid = int(val)
            query = query.replace(val, '')
        if 'as_file' in val:
            asfile = True
            query = query.replace(val, '')

    url = await set_url(query)
    gallery_dl_result = await gallery_dl(url, pid, limit)
    lists = await set_info_dict(gallery_dl_result)

    if not lists:
        return
    
    await app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_PHOTO)
    try:
        for i in range(0, len(lists), img_slice):
            media_to_send = []
            for list in lists[i:i + 10]:
                if not list['extension'] in GIF_EXT:
                    if asfile:
                        media_to_send.append(InputMediaDocument(media=list['img_url']))
                    else:
                        media_to_send.append(InputMediaPhoto(media=list['img_url']))
                else:
                    await app.send_animation(message.chat.id, list['img_url'], disable_notification=True)

            if media_to_send:
                try:
                    await app.send_media_group(message.chat.id, media_to_send, disable_notification=True)
                except:
                    pass

        await app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
    
    except Exception as err:
        logging.error(err, exc_info=True)

