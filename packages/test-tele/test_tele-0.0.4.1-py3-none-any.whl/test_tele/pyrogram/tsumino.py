"""Deprecated use hentaihand"""
import os
import re
import uuid
import shutil
import asyncio
import aiohttp
import logging
import urllib.parse
import urllib.request


from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation)


from .utils import OFFSET_PID, IMG_EXT, GIF_EXT, gallery_dl, get_tags, not_found_msg
from .telegraph import cari_konten, generate_new_telepage, images_in_folder


async def image_keyboard(query: str, my_list: list[str]) -> InlineKeyboardMarkup:
    buttons = [[
                InlineKeyboardButton("📖" ,
                                     callback_data=f"md {my_list['id']}"),
                InlineKeyboardButton("🔄",
                                     switch_inline_query_current_chat=query),
            ]]
    return InlineKeyboardMarkup(buttons)


async def set_url(query: str):
    url = query.strip().lower().replace('.md', '').lstrip()
    rate = 'MinimumRating~0'

    pattern = r'(artist:(\w+))'
    match_artist = re.search(pattern, url)

    if match_artist:
        if ' ' in url:
            user = urllib.parse.quote(match_artist.group(2))
            url = urllib.parse.quote(url.replace(match_artist.group(1), ''))
            return f"https://www.tsumino.com/books#~(Text~'{url}~Include~(~)~Tags~(~(Type~5~Text~'{user}~Exclude~false)))#"
        else:
            user = match_artist.group(2).replace('_', '+')
            return f"https://www.tsumino.com/books#?Artist={user}"

    if 'rating:' in url:
        ratepattern = r'(?:rating:(\d))'
        match_rate = re.search(ratepattern, url)
        if match_rate:
            url = url.replace(f"rating:{match_rate.group(1)}", '')
            rate = f'MinimumRating~{match_rate.group(1)}'

    # Default = onee
    url = 'onee' if url == "" else url.replace(' ', '*20')
    return f"https://www.tsumino.com/books#~(Text~\'{url}~{rate}~Include~(~))#"


async def set_info_dict(gallery_dl_result) -> list[dict]:
    """Set dict based on website"""
    my_dict = {}
    lists: list[dict] = []

    if gallery_dl_result:
        for elemen in gallery_dl_result:
            if elemen[0] == 6:
                my_dict = {}
                my_dict['post_url'] = elemen[1]
                my_dict['id'] = str(elemen[2]['id'])
                my_dict['title'] = str(elemen[2]['title'])
                my_dict['pages'] = str(elemen[2]['duration'])
                my_dict['type'] = str(elemen[2]['entryType'])
                my_dict['rating'] = str(elemen[2]['rating'])
                my_dict['thumbnail'] = elemen[2]['thumbnailUrl']
                lists.append(my_dict)
            elif elemen[0] == 3:
                my_dict = {}
                my_dict['img_url'] = elemen[1]
                my_dict['artist'] = str(elemen[2]['artist'][0])
                my_dict['id'] = str(elemen[2]['gallery_id'])
                my_dict['tags'] = await get_tags(elemen[2]['tags'])
                my_dict['title'] = str(elemen[2]['title'])
                my_dict['uploader'] = elemen[2]['uploader']
                my_dict['thumbnail'] = elemen[2]['thumbnail']
                my_dict['index'] = elemen[2]['filename']
                lists.append(my_dict)

    return lists


async def download_media(session, elemen):
    nama_file =  elemen['id'] + "_" + elemen['index'] +'.jpg'
    folder = f"temps/{elemen['id']}"

    if not os.path.exists(folder):
        os.makedirs(folder)
    
    path_file = os.path.join(folder, nama_file)
    async with session.get(elemen['img_url']) as response:
        if response.status == 200:
            with open(path_file, 'wb') as f:
                f.write(await response.read())
        else:
            logging.warning(f'Failed to download file {nama_file}')


async def generate_telegraph(id):
    url = f"https://www.tsumino.com/entry/{id}"
    gallery_dl_result = await gallery_dl(url, offset=10000, filter='--range')

    lists = await set_info_dict(gallery_dl_result)
    
    # Bagian download gambar secara paralel
    async with aiohttp.ClientSession() as session:
        tasks = [download_media(session, element) for element in lists]
        await asyncio.gather(*tasks)

    # Bagian upload ke telegraph
    link_telepage = await generate_new_telepage(
        f'temps/{lists[-1]["id"]}',
        lists[-1]['id'] + '-' + lists[-1]['title'],
        lists[-1]['artist']
    )
    
    return link_telepage


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

