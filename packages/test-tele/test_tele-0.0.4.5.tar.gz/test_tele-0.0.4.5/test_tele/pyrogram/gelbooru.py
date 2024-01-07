import re
import logging

from test_tele.extractors.gelbooru import *
from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation)


async def image_keyboard(image: dict, query: str) -> InlineKeyboardMarkup:
    buttons = [[
                InlineKeyboardButton("🔗", url=f'https://gelbooru.com/index.php?page=post&s=view&id={image["id"]}'),
            ],[
                InlineKeyboardButton("💾", callback_data=f"gb {image['id']}"),
                InlineKeyboardButton("🔄", switch_inline_query_current_chat=query),
            ]]
    
    url_pattern = r'(https?:\/\/(?:\w+\.)?\w+\.\w+(?:\/.\S+)+)'
    is_url_valid = re.search(url_pattern, image['source'])
    if image['source'] != '' and is_url_valid:
        if 'pixiv' in image['source']:
            art_px_id = image['source'].split("artworks/")[-1]
            new_button = InlineKeyboardButton("👤🔄", switch_inline_query_current_chat=f'.px {art_px_id}')
        else:
            new_button = InlineKeyboardButton("👤🔗", url=is_url_valid.group(1))
        buttons[0].insert(0, new_button)

    return InlineKeyboardMarkup(buttons)


connection_error_message = InputTextMessageContent(message_text='Network error.')
connection_error_response = InlineQueryResultArticle(
    id='networkerror', title='No response from Gelbooru',
    description='Please try again a little later.',
    input_message_content=connection_error_message)


async def inline_gelbooru(client, inline_query):
    """Handle inline query for gelbooru search"""
    query = inline_query.query

    if not query:
        return

    offset = inline_query.offset
    pid = int(offset) if offset else 0

    mode, keywords = await clean_up_tags(query)

    keywords = await autocomplete(keywords)
    if keywords is None:
        err_result = [
            InlineQueryResultArticle(
                'Could not autocomplete last tag', InputTextMessageContent(message_text='Could not find provided tags.'), id='notags', 
                description='Gelbooru tag list does not contain any match.\nPlease fix a typo or try a different tag.')
        ]
        await client.answer_inline_query(
            inline_query.id,
            results=err_result
        )
        return
    
    results = []
    images = await get_images(keywords, pid, mode)
    
    if pid == 0 and not images:
        err_result = [
            InlineQueryResultArticle(
                'No results found', InputTextMessageContent(message_text='No results found.'), 
                id='noresults', description='Please try again with different tags.')
        ]
        await client.answer_inline_query(
            inline_query.id,
            results=err_result
        )
        return

    for image in images:
        try:
            if 'no_tag' not in mode:
                caption = f"Tags : {image['tags']}" 
            else:
                caption = ''
                
            if image['full_url'].endswith('.webm') or image['full_url'].endswith('.mp4'):
                result = InlineQueryResultVideo(
                    video_url=image['full_url'],
                    thumb_url=image['thumbnail_url'],
                    title=f'Video {image["image_width"]}×{image["image_height"]}',
                    id=str(image['id']),
                    mime_type='video/mp4',
                    caption=caption,
                    reply_markup=await image_keyboard(image=image, query=query),
                )
            elif image['full_url'].endswith('.gif'):
                result = InlineQueryResultAnimation(
                    animation_url=image['full_url'],
                    animation_width=image['image_width'],
                    animation_height=image['image_height'],
                    thumb_url=image['thumbnail_url'],
                    id=str(image['id']),
                    title=str(image['id']),
                    caption=caption,
                    reply_markup=await image_keyboard(image=image, query=query),
                )
            else:
                result = InlineQueryResultPhoto(
                    photo_url=image['full_url'],
                    thumb_url=image['thumbnail_url'],
                    photo_width=image['image_width'],
                    photo_height=image['image_height'],
                    id=str(image['id']),
                    title=str(image['id']),
                    caption=caption,
                    reply_markup=await image_keyboard(image=image, query=query),
                )
            results.append(result)
        except Exception as e:
            logging.error(e)
            pass
    
    try:
        await client.answer_inline_query(
            inline_query.id,
            results=results,
            cache_time=0,
            is_gallery=True,
            next_offset=str(pid + 1)
        )
    except Exception as err:
        logging.error(err)


async def get_gb_file(data):
    """Handle callback query from inline keyboard"""
    if data:
        data = f'https://gelbooru.com/index.php?page=post&s=view&id={data}'
        image_file = await get_file(data)
        if image_file:
            return image_file
