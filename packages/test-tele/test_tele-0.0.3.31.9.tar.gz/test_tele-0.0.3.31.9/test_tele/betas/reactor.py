# import re
# import json
# import uuid
# import logging
# import urllib.parse

# from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
#                             InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)


# from .utils import OFFSET_PID, IMG_EXT, GIF_EXT, gallery_dl, get_tags, turn_into_gif


# async def image_keyboard(query: str, my_list: list[str]) -> InlineKeyboardMarkup:
#     url = my_list['id'] + "." + my_list['extension']
#     buttons = [[
#                 InlineKeyboardButton("💾" ,
#                                      callback_data=f"tp {url}"),
#                 InlineKeyboardButton("👤🔄",
#                                      switch_inline_query_current_chat=f".tp user:{my_list['author']}"),
#                 InlineKeyboardButton("🔄",
#                                      switch_inline_query_current_chat=query),
#             ]]
#     return InlineKeyboardMarkup(buttons)


# async def set_url(query: str):
#     url = query.lower().strip().replace('.tp ', '')
#     if 'loli' in url:
#         url = url.replace('loli', '')
    
#     if 'user:' in url:
#         user = url.split(':')[1]
#         return f"tp://thatpervert.com/user/{user}"

#     url = urllib.parse.quote(url)
#     return f"http://thatpervert.com/search?q={url}"


# async def set_info_dict(gallery_dl_result) -> list[dict]:
#     """Set dict based on website"""
#     my_dict = {}
#     lists: list[my_dict] = []
    
#     for elemen in gallery_dl_result:
#         if elemen[0] == 3:
#             my_dict = {}
#             my_dict['img_url'] = elemen[1]
#             my_dict['id'] = str(elemen[2]['filename'])
#             my_dict['author'] = str(elemen[2]['user'])
#             my_dict['tags'] = await get_tags(elemen[2]['tags'])
#             my_dict['title'] = str(elemen[2]['title'])
#             my_dict['extension'] = 'gif' if elemen[2]['extension'] == 'webm' else elemen[2]['extension']
#             my_dict['thumbnail'] = await turn_into_gif(elemen)
#             lists.append(my_dict)
#     return lists


# async def inline_reactor(client, inline_query):
#     """Show That Pervert arts"""
#     query = inline_query.query

#     if not query:
#         return

#     offset = inline_query.offset
#     pid = int(offset) if offset else 0

#     url = await set_url(query)
#     gallery_dl_result = await gallery_dl(url, pid)
#     lists = await set_info_dict(gallery_dl_result)

#     logging.warning(lists)

#     results = []

#     if lists:
#         try:
#             for my_list in lists:
#                 if my_list['extension'] in GIF_EXT:
#                     result = InlineQueryResultAnimation(
#                         animation_url=my_list['thumbnail'],
#                         id=str(uuid.uuid4()) + my_list['id'],
#                         caption=(
#                             f"Author : [{my_list['author']}](http://thatpervert.com/user/{my_list['author']})\n"
#                             f"Tags : {my_list['tags']}"
#                         ),
#                         reply_markup=await image_keyboard(query, my_list),
#                     )
#                 elif my_list['extension'] in IMG_EXT:
#                     result = InlineQueryResultPhoto(
#                         photo_url=my_list['thumbnail'],
#                         thumb_url=my_list['thumbnail'],
#                         id=str(uuid.uuid4()) + my_list['id'],
#                         caption=(
#                             f"Author : [{my_list['author']}](http://thatpervert.com/user/{my_list['author']})\n"
#                             f"Tags : {my_list['tags']}"
#                         ),
#                         reply_markup=await image_keyboard(query, my_list),
#                     )

#                     results.append(result)
    
#             await client.answer_inline_query(
#                 inline_query.id,
#                 results=results,
#                 cache_time=0,
#                 is_gallery=True,
#                 next_offset=str(pid + OFFSET_PID)
#             )
#         except Exception as err:
#             logging.error(err)


# async def get_tp_file(url):
#     return f"http://img2.thatpervert.com/pics/post/full/{url}"

