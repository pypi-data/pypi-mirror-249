import re
import json
import uuid 
import shlex
import asyncio
import logging
import urllib.parse

from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)


OFFSET_PID = 50


async def image_keyboard(query: str, my_list: list[str]) -> InlineKeyboardMarkup:
    url = my_list['img_url'].split("/img/")[-1]
    buttons = [[
                InlineKeyboardButton("👤🔄",
                                     switch_inline_query_current_chat=f"!px id:{my_list['author_id']}"),
                InlineKeyboardButton("🔗🔄",
                                     switch_inline_query_current_chat=f"!px {my_list['id']}")
            ],[
                InlineKeyboardButton("💾" ,
                                     callback_data=f"px {url}"),
                InlineKeyboardButton("🔄",
                                     switch_inline_query_current_chat=query),
            ]]
    return InlineKeyboardMarkup(buttons)


async def gallery_dl(raw_url: str, pid=0):
    """Start subprocess gallery-dl"""

    url = await set_url(raw_url)
    command = shlex.split(f"gallery-dl {url} --config-ignore -c config/config.json -j --range {pid + 1}-{pid + OFFSET_PID}")

    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        
        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise Exception(f'gallery-dl failed with return code {process.returncode}: {stderr.decode()}')
        else:
            result = json.loads(stdout.decode())
            my_dict = {}
            lists: list[my_dict] = []
            
            for elemen in result:
                if elemen[0] == 3:
                    my_dict = {}
                    my_dict['img_url'] = elemen[1]
                    my_dict['id'] = str(elemen[2]['id'])
                    my_dict['author'] = str(elemen[2]['user']['name']).encode('utf-8').decode('utf-8')
                    my_dict['author_id'] = str(elemen[2]['user']['id'])
                    my_dict['tags'] = await get_tags(elemen[2]['tags'])
                    my_dict['title'] = str(elemen[2]['title']).encode('utf-8').decode('utf-8')
                    my_dict['extension'] = elemen[2]['extension']
                    my_dict['thumbnail'] = await get_thumbnail(elemen[1])
                    my_dict['sample_img'] = my_dict['thumbnail'].replace("400x400", "600x600")
                    lists.append(my_dict)
            return lists
        
    except Exception as err:
        print(err)


async def set_url(query: str) -> str:
    def_tag = 's_mode=s_tag'
    url = str(query).replace("!px ", "").lower()

    if str(url).isdigit():
        return f"https://www.pixiv.net/en/artworks/{url}"

    id_pattern = r'(id:)(\w+)'
    id_match = re.search(id_pattern, url)
    if id_match:
        return f"https://www.pixiv.net/en/users/{id_match.group(2)}/artworks"

    if "-exact" in url:
        def_tag = ""
    if "-r18" in url:
        def_tag += "&mode=r18"
    elif "-safe" in url:
        def_tag += "&mode=safe"
    if "-no_ai" in url:
        def_tag += "&ai_type=1"

    url = urllib.parse.quote(url.split('-')[0].strip())
    return f"https://www.pixiv.net/en/tags/{url}/artworks?{def_tag}"


async def get_tags(tags: list[str]) -> str:
    real_tags = []
    for tag in tags:
        decoded_str = tag.encode('utf-8').decode('utf-8')
        real_tags.append(f"`{decoded_str}`")
    all_tags = f'{(", ").join(real_tags)}'
    return all_tags


async def get_thumbnail(image_url: str) -> str:
    # https://i.pximg.net/c/600x600/img-master/img/2023/12/14/00/26/56/114205137_p11_master1200.jpg
    url = image_url.split("/img/")[-1]
    url, ext = url.split(".")
    return f"https://i.pximg.net/c/400x400/img-original/img/{url}.{ext}"


async def media_dwd(client, inline_query):
    """Show Pixiv artworks"""

    query = inline_query.query

    if not query:
        return

    offset = inline_query.offset
    pid = int(offset) if offset else 0

    lists = await gallery_dl(query, pid)
    results = []

    list_ext = ['jpg', 'webp', 'png', 'heic', 'jpeg']

    if lists:
        try:
            for my_list in lists:
                if my_list['extension'] in list_ext:
                    result = InlineQueryResultPhoto(
                        photo_url=my_list['sample_img'],
                        thumb_url=my_list['thumbnail'],
                        id=str(uuid.uuid4()) + my_list['id'],
                        caption=(
                            f"Title : [{my_list['title']}](https://www.pixiv.net/en/artworks/{my_list['id']})\n"
                            f"Author : [{my_list['author']}](https://www.pixiv.net/en/users/{my_list['author_id']})\n"
                            f"Tags : {my_list['tags']}"
                        ),
                        reply_markup=await image_keyboard(query, my_list),
                    )

                    results.append(result)
    
            await client.answer_inline_query(
                inline_query.id,
                results=results,
                cache_time=0,
                is_gallery=True,
                next_offset=str(pid + OFFSET_PID)
            )
        except Exception as err:
            logging.error(err)


async def get_px_file(url):
    return f"https://i.pximg.net/img-original/img/{url}"

