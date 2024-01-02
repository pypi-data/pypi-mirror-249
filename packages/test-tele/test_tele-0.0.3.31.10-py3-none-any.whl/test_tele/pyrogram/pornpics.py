import uuid 
import logging

from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)

from .utils import OFFSET_PID, IMG_EXT, GIF_EXT, gallery_dl, get_tags, not_found_msg


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


async def set_info_dict(gallery_dl_result) -> list[dict]:
    """Set dict based on website"""
    my_dict = {}
    lists: list[dict] = []
    
    if gallery_dl_result:
        for elemen in gallery_dl_result:
            if elemen[0] == 6:
                my_dict = {}
                my_dict['post_url'] = elemen[1]
                my_dict['id'] = str(elemen[2]['gid'])
                my_dict['title'] = str(elemen[2]['desc']).rsplit(' ', 1)[0]
                my_dict['thumbnail'] = elemen[2]['t_url']
                my_dict['sample_img'] = elemen[2]['t_url_460']
                lists.append(my_dict)
            elif elemen[0] == 3:
                my_dict = {}
                my_dict['img_url'] = elemen[1]
                my_dict['thumbnail'] = await get_thumbnail(elemen[1])
                my_dict['sample_img'] = my_dict['thumbnail'].replace("/300/", "/460/")
                my_dict['title'] = str(elemen[2]['title'])
                my_dict['id'] = str(elemen[2]['gallery_id'])
                my_dict['slug'] = str(elemen[2]['slug'])
                my_dict['models'] = await get_tags(elemen[2]['models'])
                my_dict['tags'] = await get_tags(elemen[2]['categories'])
                my_dict['extension'] = elemen[2]['extension']
                lists.append(my_dict)
    return lists


async def get_thumbnail(image_url: str) -> str:
    # https://cdni.pornpics.com/460/7/687/69235644/69235644_009_15ef.jpg
    url = image_url.split("/1280/")[-1]
    url, ext = url.split(".")
    return f"https://cdni.pornpics.com/300/{url}.{ext}"


async def set_url(query: str) -> str:
    url = str(query).strip().lower().replace(".rp", "").lstrip()

    if 'id:' in url:
        url = url.replace('id:', '')
        return f"https://www.pornpics.com/galleries/{url}"

    url = url.replace(' ', '+')
    return f"https://www.pornpics.com/?q={url}"


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


async def get_pp_file(url):
    return f"https://cdni.pornpics.com/1280/{url}"

