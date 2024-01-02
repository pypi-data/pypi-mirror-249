import os
import uuid 
import time
import shutil
import aiohttp
import asyncio
import logging

from pixivpy3 import *
from pyrogram import enums
from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputMediaPhoto, InputMediaDocument)

from .utils import IMG_EXT, BOT_CONFIG, not_found_msg
from .telegraph import images_in_folder

PIXIV_MODE = ['no_ai', 'no_tag', 'novel', 'nsfw', 'safe']

api = AppPixivAPI()
api.auth(refresh_token=BOT_CONFIG.apis.pixiv_refresh_token)


async def image_keyboard(query: str, my_list: list[str]) -> InlineKeyboardMarkup:
    url = my_list['img_urls']['img_original'].split("/img/")[-1]
    buttons = [[
                InlineKeyboardButton("👤🔄",
                                     switch_inline_query_current_chat=f".px id:{my_list['user_id']}"),
                InlineKeyboardButton("🔗🔄",
                                     switch_inline_query_current_chat=f".px {my_list['id']}")
            ],[
                InlineKeyboardButton("💾" ,
                                     callback_data=f"px {url}"),
                InlineKeyboardButton("🔄",
                                     switch_inline_query_current_chat=query),
            ]]
    return InlineKeyboardMarkup(buttons)


async def get_pixiv_list(query: str, offset: int):
    if query != '':
        input = query.split()
        for val in input:
            if val.isdigit():
                return await set_dict_detail(api.illust_detail(int(val)))
            if 'id:' in val:
                user_id = val.split("id:")[-1]
                return await set_dict_search(api.user_illusts(int(user_id), offset=offset))
    else:
        # Default = sangonomiya kokomi 
        query = '珊瑚宮心海'

    return await set_dict_search(api.search_illust(query, offset=offset))


async def set_dict_search(pixiv_json) -> dict:
    illusts = pixiv_json["illusts"]
    media_posts = []

    for illust in illusts:
        if illust["meta_pages"]:
            img_ori = illust["meta_pages"][0]["image_urls"]["original"]
        else:
            img_ori = illust['meta_single_page']['original_image_url']
            
        images = {
            "img_thumb": illust["image_urls"]["square_medium"],
            "img_sample": illust["image_urls"]["medium"],
            "img_original": img_ori
        }

        media_post = {
            'id': str(illust["id"]),
            'title': illust["title"],
            'user_id': str(illust["user"]["id"]),
            'user_name': illust["user"]["name"],
            'tags': await get_pixiv_tags(illust["tags"]),
            'img_urls': images
        }
        media_posts.append(media_post)
    return media_posts


async def set_dict_detail(pixiv_json) -> dict:
    illusts = pixiv_json["illust"]
    media_posts = []

    if 'meta_pages' in illusts and illusts['meta_pages']:
        for illust in illusts['meta_pages']:
            images = {
                "img_thumb": illust["image_urls"]["square_medium"],
                "img_sample": illust["image_urls"]["medium"],
                "img_original": illust["image_urls"]["original"]
            }

            media_post = {
                'id': str(illusts["id"]),
                'title': illusts["title"],
                'user_id': str(illusts["user"]["id"]),
                'user_name': illusts["user"]["name"],
                'tags': await get_pixiv_tags(illusts["tags"]),
                'img_urls': images
            }
            media_posts.append(media_post)
    else:
        images = {
            "img_thumb": illusts["image_urls"]["square_medium"],
            "img_sample": illusts["image_urls"]["medium"],
            "img_original": illusts["meta_single_page"]["original_image_url"]
        }
        media_post = {
            'id': str(illusts["id"]),
            'title': illusts["title"],
            'user_id': str(illusts["user"]["id"]),
            'user_name': illusts["user"]["name"],
            'tags': await get_pixiv_tags(illusts["tags"]),
            'img_urls': images
        }
        media_posts.append(media_post)
    return media_posts


async def get_pixiv_tags(tags):
    all_tags = []
    for tag in tags:
        if not tag.translated_name:
            re_tag = f"`{tag.name}`"
        else:
            re_tag = f"`{tag.name}`(`{tag.translated_name}`)"
        all_tags.append(re_tag)
    final_tag = (", ").join(all_tags)
    return final_tag


async def set_pixiv_mode(query: str):
    """Setting searching mode"""
    example_query = ".px sangonomiya kokomi loli no_ai no_tag safe"
    current_modes = {}
    query = query.strip().lower().replace(".px", "").lstrip()
    keywords = query.split()

    for keyword in keywords:
        if keyword in PIXIV_MODE:
            current_modes[keyword] = True
            query = query.replace(keyword, '')
        if keyword.isdigit():
            current_modes['illust_detail'] = True
        if 'no_inline' in keyword:
            current_modes['no_inline'] = True
            query = query.replace(keyword, '')
        if 'as_file' in keyword:
            if current_modes.get('no_inline'):
                current_modes['as_file'] = True
            query = query.replace(keyword, '')
        if 'limit:' in keyword:
            if current_modes.get('no_inline'):
                limit = keyword.split('limit:')[-1]
                current_modes['limit'] = limit
            query = query.replace(keyword, '')
        if 'offset:' in keyword:
            if current_modes.get('no_inline'):
                offset = keyword.split('offset:')[-1]
                current_modes['offset'] = offset
            query = query.replace(keyword, '')

    return current_modes, query.strip()


async def create_inline_query_result_photo(my_list, px_mode, query):
    caption = (
        f"**[{my_list['title']}](https://www.pixiv.net/en/artworks/{my_list['id']})**\n"
        f"Artist : [{my_list['user_name']}](https://www.pixiv.net/en/users/{my_list['user_id']})\n"
        f"Tags : {my_list['tags']}"
    )

    sample_img = my_list['img_urls']['img_sample'].replace('540x540_70', '600x1200_90')
    thumb_img = my_list['img_urls']['img_thumb'].replace('360x360_70', '400x400')

    if str(my_list['img_urls']['img_sample']).endswith(tuple(IMG_EXT)):
        result = InlineQueryResultPhoto(
            photo_url=sample_img,
            thumb_url=thumb_img,
            id=str(uuid.uuid4()) + my_list['id'],
            caption=caption if 'no_tag' not in px_mode or my_list['title'] != '' else '',
            reply_markup=await image_keyboard(query, my_list),
        )
        return result
    return None


async def inline_pixiv(client, inline_query):
    """Show Pixiv artworks"""
    query = inline_query.query
    if not query:
        return

    limit = 30
    offset = inline_query.offset
    pid = int(offset) if offset else 0

    px_mode, keywords = await set_pixiv_mode(query)
    logging.warning(px_mode)
    lists = await get_pixiv_list(keywords, pid)
    results = []

    if pid == 0 and not lists:
        return await not_found_msg(client, inline_query)

    if lists:
        try:
            for my_list in lists:
                result = await create_inline_query_result_photo(my_list, px_mode, query)
                if result:
                    results.append(result)

            cache_time = 60
            next_offset = str(pid + limit) if 'illust_detail' not in px_mode else None
            await client.answer_inline_query(
                inline_query.id, 
                results=results, 
                cache_time=cache_time, 
                is_gallery=True, 
                next_offset=next_offset)
        except Exception as err:
            logging.error(err, exc_info=True)
    

async def get_px_file(url):
    return f"https://i.pximg.net/img-original/img/{url}"


# Perlu decorator premium
async def upload_px_batch(app, message):
    query = str(message.text)
    if not query:
        return
    
    start = time.time()
    img_slice = 10
    chat_id = message.chat.id

    px_mode, keywords = await set_pixiv_mode('no_inline ' + query)

    limit = px_mode.get('limit', 30)
    offset = px_mode.get('offset', 0)
    as_file = px_mode.get('as_file', False)

    lists = await get_pixiv_list(keywords, offset)

    if not lists:
        return
    
    logging.warning(f"selesai ambil data: {round(time.time() - start, 2)}")
    try:
        for i in range(0, len(lists), img_slice):
            media_to_send = []
            if i + 10 > limit:
                break

            await app.send_chat_action(chat_id, enums.ChatAction.UPLOAD_PHOTO)
            if as_file:
                for list in lists[i:i + 10]:
                    if str(list['img_urls']['img_sample']).endswith(tuple(IMG_EXT)):
                        media_to_send.append(InputMediaDocument(media=list['img_urls']['img_original']))
            else:
                images_list = await download_px_images(lists)
                for list in images_list:
                    media_to_send.append(InputMediaPhoto(media=list))

            if media_to_send:
                try:
                    await app.send_media_group(chat_id, media_to_send, disable_notification=True)
                except:
                    pass
            await app.send_chat_action(chat_id, enums.ChatAction.CANCEL)

        await rmfolder_pixiv(f"temps/pixiv/{lists[-1]['id']}")
        
        logging.warning(f"akhir : {round(time.time() - start, 2)}")
    except Exception as err:
        logging.error(err, exc_info=True)


async def download_media(folder, lists):
    tasks = [api.download(my_list['img_urls']['img_sample'].replace('540x540_70', '600x1200_90'), path=f'temps/pixiv/{lists[-1]["id"]}') for my_list in lists]
    await asyncio.gather(*tasks)


async def download_px_images(lists):
    folder = f"temps/pixiv/{lists[-1]['id']}"
    if not os.path.exists(folder):
        os.makedirs(folder)
    await download_media(api, lists)
    images = await images_in_folder(f'temps/pixiv/{lists[-1]["id"]}')
    return images


async def rmfolder_pixiv(folder):
    shutil.rmtree(folder)

