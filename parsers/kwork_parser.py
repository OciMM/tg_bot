from kwork import Kwork
import asyncio
import json
import os


async def kwork_parser(categories_id: int):
    api = Kwork(login=os.getenv('LOGIN'), password=os.getenv('PASSWORD'))
    # profile = await api.get_me()
    # print(profile)

    # categories = await api.get_categories()
    # print(categories)

    projects = await api.get_projects(categories_ids=[categories_id])
    print(projects)

    with open('projects.json', 'w', encoding="utf-8") as file:
        json.dump(projects, file, indent=4, ensure_ascii=False)


    await api.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(kwork_parser(categories_id=11))