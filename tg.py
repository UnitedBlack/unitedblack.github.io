from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
import hashlib
import os
import t3nsor
from datetime import datetime
import time


def chat_gpt(prompt_user):
    messages = []

    t3nsor_cmpl = t3nsor.Completion.create(
        prompt=prompt_user,
        messages=messages
    )

    print('gpt:', t3nsor_cmpl.completion.choices[0].text)

    messages.extend([
        {'role': 'user', 'content': prompt_user},
        {'role': 'assistant',
            'content': t3nsor_cmpl.completion.choices[0].text}
    ])
    return t3nsor_cmpl.completion.choices[0].text


bot = Bot(token='6471699804:AAGGn86o0zTLOUdB1xDDlsPJoz7XbNwKOfE')
dp = Dispatcher(bot)


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery, ):
    text = query.query or "echo"
    result = chat_gpt(query.query)
    result_id = hashlib.md5((text + str(datetime.now().timestamp())).encode()).hexdigest()

    articles = [types.InlineQueryResultArticle(
        id=result_id,
        title="Ask ChatGPT",
        input_message_content=types.InputTextMessageContent(
            message_text=result))]

    await query.answer(articles, cache_time=30, is_personal=True)

executor.start_polling(dp, skip_updates=True)
