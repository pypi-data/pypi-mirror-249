# import time
# import uuid 
# import requests
# import logging

# from bs4 import BeautifulSoup

# from pyrogram import enums
# from pyrogram.types import InputMediaPhoto, InputMediaDocument
# from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
#                             InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)

# from test_tele.pyrogram.utils import OFFSET_PID, autocomplete, not_found_msg, is_japanese
# from test_tele.config_bot import BOT_CONFIG


# async def image_keyboard(query: str, file_name: str) -> InlineKeyboardMarkup:
#     buttons = [[
#                 InlineKeyboardButton("💾" ,
#                                      callback_data=f"2d {file_name}"),
#                 InlineKeyboardButton("🔄",
#                                      switch_inline_query_current_chat=query),
#             ]]
#     return InlineKeyboardMarkup(buttons)


# async def get_child_page(url: str, limit: int, imgs: list, starts: int):
#     response = requests.get(url)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, 'html.parser')
#         div_posts = soup.find_all('div', class_='img-box')

#         for div_post in div_posts[starts:]:
#             div_img = div_post.find('div', class_='main-img')
#             img_tag = div_img.find('img')  # Mengakses tag <img> di dalam <div class="main-img">
#             if img_tag:  # Memastikan tag <img> ditemukan sebelum mencoba mengakses atribut src
#                 imgs.append(img_tag.get('src'))
            
#             if len(imgs) == limit:
#                 break
    
#     return imgs


# async def get_main_page(base_url: str, pid: int, limit: int=OFFSET_PID):
#     page_number = pid // 300 + 1
#     post_number = (pid % 300) // 30 + 1
#     img_urls = []
#     post_dict = {}
#     posts = []
#     n_loop = 0
#     is_first = True

#     while len(img_urls) < limit:
#         if n_loop >= 2 and len(img_urls) == 0:
#             break

#         n_loop += 1
#         url = f'{base_url}&paged={page_number}' if page_number > 1 else base_url
#         response = requests.get(url)

#         if response.status_code == 200:
#             soup = BeautifulSoup(response.content, 'html.parser')
#             div_posts = soup.find_all('div', class_='post')
#             for div_post in div_posts[post_number:]:
#                 h2_title = div_post.find('h2', class_='entry-title')
#                 if h2_title:
#                     url = div_post.find('div', class_='more-link').find('a')['href']
#                     id_img = 0
#                     if is_first:
#                         id_img = (pid % (limit * 10)) % 30
#                         is_first = False
#                     img_urls = await get_child_page(url, limit, img_urls, id_img)
#                     post_dict['main_tag'] = div_post.find('div', class_='cat-tag').find('a').text

#                 if len(img_urls) >= limit:
#                     break

#             if len(img_urls) >= limit:
#                 break

#             page_number += 1
#             post_number = 1
    
#     post_dict['img_urls'] = img_urls
#     posts.append(post_dict)
#     return posts


# async def set_url(query: str) -> str:
#     query = query.strip().lower().replace(".2d", "").lstrip()
#     all_tags = BOT_CONFIG.all_tags.tags

#     if not await is_japanese(query):
#         gen_tag = await autocomplete(all_tags, query, False)
#         if gen_tag:
#             query = query.replace(query, gen_tag)
    
#     # Default = loli
#     tags = 'ロリ' if query == '' else query.replace(" ", "+")
#     return f"https://vanilla-rock.com/?s={tags}&submit=検索"


# async def inline_vanillarock(client, inline_query):
#     """Show Vanilla-rock arts"""
#     query = inline_query.query
#     if not query:
#         return
    
#     offset = inline_query.offset
#     pid = int(offset) if offset else 0

#     url = await set_url(query)
#     lists = await get_main_page(url, pid)
#     results = []

#     if pid == 0 and not lists[-1]['img_urls']:
#         return await not_found_msg(client, inline_query)
    
#     tag = url.split("?s=")[1].split("&submit=")[0]
#     tag = f", `{tag}`" if tag != lists[-1]['main_tag'] else ''

#     if lists:
#         try:
#             for url in lists[-1]['img_urls']:
#                 file_name = url.split("uploads/")[1]
#                 result = InlineQueryResultPhoto(
#                     photo_url=url,
#                     id=str(uuid.uuid4()),
#                     caption=(
#                         f"Tags : `{lists[-1]['main_tag']}`" + tag
#                     ),
#                     reply_markup=await image_keyboard(query, file_name),
#                 )
#                 results.append(result)

#             await client.answer_inline_query(
#                 inline_query.id,
#                 results=results,
#                 cache_time=60,
#                 is_gallery=True,
#                 next_offset=str(pid + OFFSET_PID)
#             )
#         except Exception as err:
#             logging.error(err)


# async def get_vr_file(url):
#     return f"https://vanilla-rock.com/wp-content/uploads/{url}"


# # Perlu decorator premium
# async def upload_vr_batch(app, message):
#     start_time = time.time()
#     query = str(message.text)
#     if not query:
#         return
    
#     pid = 0
#     limit = 30
#     asfile = False
#     img_slice = 10

#     input = query.split()
#     for i, val in enumerate(input):
#         if 'limit:' in val:
#             limit = int(val.split("limit:")[-1].strip())
#             limit = limit if limit <= 30 else 30
#             query = query.replace(val, '')
#         if val.isdigit():
#             pid = int(val)
#             query = query.replace(val, '')
#         if 'as_file' in val:
#             asfile = True
#             query = query.replace(val, '')

#     url = await set_url(query)
#     lists = await get_main_page(url, pid, limit)

#     if not lists:
#         return
    
#     await app.send_chat_action(message.chat.id, enums.ChatAction.UPLOAD_PHOTO)
#     for i in range(0, len(lists[-1]['img_urls']), img_slice):
#         media_to_send = []
#         for url in lists[-1]['img_urls'][i:i + 10]:
#             if asfile:
#                 media_to_send.append(InputMediaDocument(media=url))
#             else:
#                 media_to_send.append(InputMediaPhoto(media=url))
#         if media_to_send:
#             try:
#                 await app.send_media_group(message.chat.id, media_to_send, disable_notification=True)
#             except:
#                 pass
    
#     await app.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
#     logging.warning(f"response time: {round(time.time() - start_time, 1)}")

