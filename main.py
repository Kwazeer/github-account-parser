import asyncio
import aiohttp
import json


def open_file():
    try:
        with open('git_user.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_file(obj):
    try:
        with open('git_user.json', 'w', encoding='utf-8') as file:
            return json.dump(obj=obj, fp=file, ensure_ascii=False, indent=4)
    except Exception as e:
        raise e


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def main():
    url = 'https://api.github.com/users/kwazeer/events'
    result = await fetch_url(url)
    if result:
        save_file(result)
    else:
        print('Данные не найдены')
    return result


output = asyncio.run(main())
print(output)
