import asyncio
import aiohttp
import json


def open_file():
    """Load JSON file"""
    try:
        with open('git_user.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_file(obj):
    """Save info to JSON"""
    try:
        with open('git_user.json', 'w', encoding='utf-8') as file:
            return json.dump(obj=obj, fp=file, ensure_ascii=False, indent=4)
    except Exception as e:
        raise e


async def fetch_url(url):
    """Parsing info from given URL"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def main():
    name_check = input('Enter GitHub username: ').lower()
    url = f'https://api.github.com/users/{name_check}/events'
    result = await fetch_url(url)

    if result:
        save_file(result)
    else:
        print('Could not find any data.')
        return None

    user_data = {
        'username': name_check.capitalize(),
        'commits': 0
    }

    for data in result:
        commits = data['payload'].get('commits')

        if isinstance(commits, list):
            user_data['commits'] += len(commits)

    if user_data['commits'] == 0:
        user_data['commits_display'] = 'Нет коммитов'

    return user_data

output = asyncio.run(main())
print(f'Username: {output['username']}\n'
      f'Commits made: {output['commits']}')

