# """Ide pake out message True"""
# import os
# import re
# import uuid
# import asyncio
# import aiohttp
# import logging
# import urllib.parse
# import urllib.request


# from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
#                             InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation)


# from .utils import OFFSET_PID, IMG_EXT, GIF_EXT, gallery_dl, get_tags
# from .telegraph import cari_konten, generate_new_telepage, images_in_folder


# async def image_keyboard(query: str, my_list: list[str]) -> InlineKeyboardMarkup:
#     buttons = [[
#                 # InlineKeyboardButton("👨🏻‍🎨🔄",
#                 #                      switch_inline_query_current_chat=f".md artist:{my_list['artist'].replace(' ', '-')}"),
#                 InlineKeyboardButton("📖" ,
#                                      callback_data=f"md {my_list['id']}"),
#                 InlineKeyboardButton("🔄",
#                                      switch_inline_query_current_chat=query),
#             ]]
#     return InlineKeyboardMarkup(buttons)


# async def set_url(query: str):
#     base_url = 'https://hentaihand.com/en/language/english'
#     lang = {'zh':'chinese', 'en':'english', 'jp':'japanese'}
#     title = query.lower().strip().replace('.md ', '')
    
#     inputs = title.split()
#     for idx, val in enumerate(inputs):
#         if val.startswith('-'):
#             lang_code = val[1:]
#             title = title.replace(val, '')
#             if lang_code in lang and 'english' in base_url:
#                 base_url = base_url.rstrip('english')
#                 base_url += lang[lang_code]
#         if val.startswith('tag:'):
#             tag = val[4:]
#             title = title.replace(val, '')
#             base_url = f'https://hentaihand.com/en/tag/{tag}'

#     search_title = urllib.parse.quote(title.strip())
#     if search_title != '':
#         full_url = base_url + '?page=1&q=' + search_title
#     else:
#         full_url = base_url
#     return full_url


# async def get_hh_tags(tags: list[str], limit: int = 0) -> str:
#     real_tags = []
#     i = 0
#     for tag in tags:
#         if limit != 0:
#             i += 1
#         decoded_str = str(tag['slug'])
#         real_tags.append(f"`{decoded_str}`")
#         if limit != 0 and i == limit:
#             break
#     all_tags = f'{(", ").join(real_tags)}'
#     return all_tags


# async def slugify(text):
#     text = re.sub(r'[^a-zA-Z\d\s\-]', '', text)
#     slug = '-'.join(text.lower().split()).replace('--', '-')
#     return slug


# async def set_info_dict(gallery_dl_result) -> list[dict]:
#     """Set dict based on website"""
#     my_dict = {}
#     lists: list[dict] = []

#     if gallery_dl_result:
#         for elemen in gallery_dl_result:
#             if elemen[0] == 6:
#                 my_dict = {}
#                 my_dict['post_url'] = elemen[1]
#                 my_dict['id'] = str(elemen[2]['id'])
#                 my_dict['title'] = str(elemen[2]['title'])
#                 my_dict['tags'] = await get_hh_tags(elemen[2]['tags'], 40)
#                 my_dict['pages'] = str(elemen[2]['pages'])
#                 my_dict['slug'] = str(elemen[2]['slug'])
#                 if elemen[2]['language']:
#                     my_dict['language'] = str(elemen[2]['language']['name'])
#                 else:
#                     my_dict['language'] = 'English'
#                 my_dict['thumbnail'] = elemen[2]['thumb_url']
#                 lists.append(my_dict)
#             elif elemen[0] == 3:
#                 my_dict = {}
#                 my_dict['img_url'] = elemen[1]
#                 if elemen[2]['artist']:
#                     my_dict['artist'] = elemen[2]['artist'][0]
#                 else:
#                     my_dict['artist'] = 'Anonymous'
#                 my_dict['id'] = str(elemen[2]['gallery_id'])
#                 my_dict['language'] = elemen[2]['language']
#                 my_dict['tags'] = await get_tags(elemen[2]['tags'])
#                 my_dict['title'] = str(elemen[2]['title'])
#                 my_dict['thumbnail'] = elemen[2]['thumbnail_url']
#                 my_dict['index'] = elemen[2]['filename']
#                 lists.append(my_dict)

#     return lists


# async def download_media(session, elemen):
#     nama_file =  elemen['id'] + "_" + elemen['index'] +'.jpg'
#     folder = f"temps/{elemen['id']}"

#     if not os.path.exists(folder):
#         os.makedirs(folder)

#     logging.warning(f"mulai download di : {folder}")
    
#     path_file = os.path.join(folder, nama_file)
#     async with session.get(elemen['img_url']) as response:
#         if response.status == 200:
#             with open(path_file, 'wb') as f:
#                 f.write(await response.read())
#             logging.warning(f"download berhasil, {nama_file}")
#         else:
#             logging.warning(f'Failed to download file {nama_file}')


# async def generate_telegraph(slug):
#     url = f"https://hentaihand.com/en/comic/{slug}"
#     gallery_dl_result = await gallery_dl(url, offset=10000)

#     logging.warning(gallery_dl_result)
#     try:
#         lists = await set_info_dict(gallery_dl_result)
#         logging.warning(lists)
#     except Exception as err:
#         logging.error("error", exc_info=True)

#     # Bagian download gambar secara paralel
#     async with aiohttp.ClientSession() as session:
#         tasks = [download_media(session, element) for element in lists]
#         await asyncio.gather(*tasks)
    
#     logging.warning("selesai download")
#     logging.warning("mulai buat telegraph")

#     # Bagian upload ke telegraph
#     link_telepage = await generate_new_telepage(
#         await images_in_folder(f'temps/{lists[-1]["id"]}'),
#         lists[-1]['id'] + '-' + lists[-1]['title'],
#         lists[-1]['artist']
#     )

#     logging.warning(f"ini link nya : {link_telepage}")

#     return link_telepage


# async def inline_hentaihand(client, inline_query):
#     """Show hentaihand arts"""
#     query = inline_query.query

#     if not query:
#         return

#     offset = inline_query.offset
#     pid = int(offset) if offset else 0
    
#     url = await set_url(query)
#     my_filter = f'--chapter-range'
#     gallery_dl_result = await gallery_dl(url, pid, offset=30, filter=my_filter)

#     lists = await set_info_dict(gallery_dl_result)
#     results = []

#     if lists:
#         try:
#             for my_list in lists:
#                 logging.warning(my_list)
#                 result = InlineQueryResultArticle(
#                     title=my_list['title'],
#                     input_message_content=InputTextMessageContent(
#                         f"Title : **{my_list['title']}**\n"
#                         f"Language : {my_list['language']}\n"
#                         f"Pages : {my_list['pages']}\n"
#                         f"Tags : {my_list['tags']}\n"
#                     ),
#                     id=str(uuid.uuid4()),
#                     description=f"Language : {my_list['language']}\nPages : {my_list['pages']}\nTags : {my_list['tags'].replace('`', '')}",
#                     thumb_url=my_list['thumbnail'],
#                     reply_markup=await image_keyboard(query, my_list),
#                 )
               
#                 results.append(result)
    
#             await client.answer_inline_query(
#                 inline_query.id,
#                 results=results,
#                 cache_time=0,
#                 next_offset=str(pid + 30)
#             )
#         except Exception as err:
#             logging.error(err, exc_info=True)

