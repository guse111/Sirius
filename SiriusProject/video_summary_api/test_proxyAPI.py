from openai import OpenAI

client = OpenAI(api_key="sk-JshQXy1kBfNKeDwa5CYD9yOWoLOvr58l", base_url="https://api.proxyapi.ru/openai/v1")

def AI(text):
    sistpromt = f"Перескажи следующий текст"
    userpromt = text

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.2,
        messages=[{"role": "system", "content": sistpromt}, {"role": "user", "content": userpromt}]
    )
    text = completion.choices[0].message.content
    return text
