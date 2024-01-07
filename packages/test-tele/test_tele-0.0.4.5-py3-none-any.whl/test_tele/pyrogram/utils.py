from pyrogram.types import (InlineQueryResultArticle, InlineQueryResultPhoto, InlineQueryResultVideo, InlineKeyboardMarkup, 
                            InlineKeyboardButton, InputTextMessageContent, InlineQueryResultAnimation, InputTextMessageContent)


async def not_found_msg(client, inline_query):
    err_result = [
        InlineQueryResultArticle(
            'No results found', InputTextMessageContent(message_text='No results found'), 
            id='noresults', description='Please try again with different tags')
    ]
    await client.answer_inline_query(
        inline_query.id,
        results=err_result
    )
    return
