import nest_asyncio
nest_asyncio.apply()

import asyncio
from aiohttp import ClientSession


async def getUrl(url, session):
  try:
    async with session.get(url=url) as response:
      return await response.read()
  except Exception as e:
    print('Failed to get {}. Error: {}.'.format(url, e.__class__))


async def main(urls):
  async with ClientSession() as session:
    tasks = []
    for url in urls:
      task = asyncio.ensure_future(getUrl(url, session))
      tasks.append(task)
    return await asyncio.gather(*tasks)


def getUrls(urls):
  return asyncio.get_event_loop().run_until_complete(main(urls))