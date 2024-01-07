import uuid 
import logging

from pyrogram import enums
from pyrogram.types import InputMediaPhoto, InputMediaDocument
from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)

from test_tele.extractors.furry import *
from test_tele.pyrogram.utils import not_found_msg


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

