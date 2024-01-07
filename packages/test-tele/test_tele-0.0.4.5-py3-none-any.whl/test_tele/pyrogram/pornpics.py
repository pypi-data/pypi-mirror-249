import uuid 
import logging

from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)

from test_tele.pyrogram.utils import not_found_msg
from test_tele.extractors.pornpics import *


async def image_keyboard(post, query: str, my_list: list[str]) -> InlineKeyboardMarkup:
    if post:
        buttons = [[
                    InlineKeyboardButton("🔗🔄",
                                        switch_inline_query_current_chat=f".rp id:{my_list['id']}"),
                    InlineKeyboardButton("🔄",
                                        switch_inline_query_current_chat=query),
                ]]
    else:
        url = my_list['img_url'].split("/1280/")[-1]
        buttons = [[
                    InlineKeyboardButton("💾" ,
                                        callback_data=f"rp {url}"),
                    InlineKeyboardButton("🔗🔄",
                                        switch_inline_query_current_chat=f".rp id:{my_list['id']}"),
                    InlineKeyboardButton("🔄",
                                        switch_inline_query_current_chat=query),
                ]]

    return InlineKeyboardMarkup(buttons)


async def inline_pornpics(client, inline_query):
    """Show Pornpics artworks"""
    query = inline_query.query

    if not query:
        return

    offset = inline_query.offset
    pid = int(offset) if offset else 0
        
    url = await set_url(query)
    
    if 'galleries' not in url:
        my_filter = '--chapter-range'
    else:
        my_filter = '--range'

    gallery_dl_result = await gallery_dl(url, pid, filter=my_filter)    
    lists = await set_info_dict(gallery_dl_result)
    results = []

    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)

    if lists:
        try:
            for my_list in lists:
                if 'img_url' in my_list:
                    result = InlineQueryResultPhoto(
                        photo_url=my_list['sample_img'],
                        thumb_url=my_list['thumbnail'],
                        id=str(uuid.uuid4()) + my_list['id'],
                        caption=(
                            f"Models : {my_list['models']}\n"
                            f"Tags : {my_list['tags']}\n"
                        ),
                        reply_markup=await image_keyboard(False, query, my_list),
                    )
                    results.append(result)
                else:
                    result = InlineQueryResultPhoto(
                        photo_url=my_list['sample_img'],
                        thumb_url=my_list['thumbnail'],
                        id=str(uuid.uuid4()) + my_list['id'],
                        reply_markup=await image_keyboard(True, query, my_list),
                    )
                    results.append(result)
    
            await client.answer_inline_query(
                inline_query.id,
                results=results,
                cache_time=180,
                is_gallery=True,
                next_offset=str(pid + OFFSET_PID)
            )
        except:
            logging.error("An error occurred:", exc_info=True)

