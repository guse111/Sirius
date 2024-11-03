import httpx

async def download_from_yandex_disk(public_url, save_path):
    async with httpx.AsyncClient() as client:
        # Получаем ссылку для скачивания
        response = await client.get('https://cloud-api.yandex.net/v1/disk/public/resources/download', params={'public_key': public_url})
        response.raise_for_status()  # Если произошла ошибка, поднимем исключение

        download_url = response.json()['href']

        # Скачиваем файл и сохраняем, используя метод stream
        async with client.stream('GET', download_url, follow_redirects=True) as r:
            r.raise_for_status()
            with open(save_path, 'wb') as f:
                async for chunk in r.aiter_bytes(chunk_size=8192):
                    f.write(chunk)
