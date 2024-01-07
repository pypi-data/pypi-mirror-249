import os
import re
import uuid
import asyncio
import aiohttp
import logging
import urllib.parse
import urllib.request


from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation)

from test_tele.extractors.manga import *
from test_tele.pyrogram.utils import not_found_msg


async def image_keyboard(query: str, my_list: list[str]) -> InlineKeyboardMarkup:
    buttons = [[
                InlineKeyboardButton("📖" ,
                                     callback_data=f"md {my_list['id']}"),
                InlineKeyboardButton("🔄",
                                     switch_inline_query_current_chat=query),
            ]]
    return InlineKeyboardMarkup(buttons)


async def inline_tsumino(client, inline_query):
    """Show Tsumino arts"""
    query = inline_query.query

    if not query:
        return

    offset = inline_query.offset
    pid = int(offset) if offset else 0

    url = await set_url(query)
    my_filter = '--chapter-range'
    gallery_dl_result = await gallery_dl(url, pid, filter=my_filter)

    lists = await set_info_dict(gallery_dl_result)
    results = []

    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)
         
    if lists:
        try:
            for my_list in lists:
                result = InlineQueryResultArticle(
                    title=my_list['title'],
                    input_message_content=InputTextMessageContent(
                        f"Title : {my_list['title']}\n"
                        f"Book ID : {my_list['id']}\n"
                        f"Rating : {my_list['rating']}\n"
                        f"Pages : {my_list['pages']}\n"
                    ),
                    id=str(uuid.uuid4()) + my_list['id'],
                    # url=f"https://www.tsumino.com/entry/{my_list['id']}",
                    description=f"Rating : {my_list['rating']}\nPages : {my_list['pages']}",
                    thumb_url=my_list['thumbnail'],
                    reply_markup=await image_keyboard(query, my_list),
                )
               
                results.append(result)
    
            await client.answer_inline_query(
                inline_query.id,
                results=results,
                cache_time=180,
                next_offset=str(pid + OFFSET_PID)
            )
        except Exception as err:
            logging.error(err)

