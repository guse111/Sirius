import os
from openai import AsyncOpenAI
import httpx
from dotenv import load_dotenv

client = AsyncOpenAI(api_key="sk-JshQXy1kBfNKeDwa5CYD9yOWoLOvr58l", base_url="https://api.proxyapi.ru/openai/v1")

async def AI(text):
    sistpromt = "Перескажи следующий текст"
    userpromt = text

    completion = await client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[{"role": "system", "content": sistpromt}, {"role": "user", "content": userpromt}]
    )
    text = completion.choices[0].message.content
    return text
