import asyncio
import aiohttp
from lxml import html, etree
import re
import json

START_HTTP = "http://forum.overclockers.ua/viewforum.php?f=26"
SUBJECT = []
AMOUNT_PAGES = 2

PRICE_TEMPLATE = "([0-9]{0,}[.,]{0,1}[0-9]{1,})[\s]{0,1}([Г|г]рн|\$)"


def pars_topics(body):
    root = html.fromstring(body)
    topics = root.xpath('//li[contains(@class, "row bg")]')
    return topics


def find_price(content):
    prices = max(re.findall(PRICE_TEMPLATE, content)) if re.findall(PRICE_TEMPLATE, content) else [[], []]
    return prices


async def get_content(loop, topic):
    url = "http://forum.overclockers.ua/" + topic.xpath("./dl/dt/div/a/@href")[0][2:]
    author = topic.xpath("./dl/dd[@class='author']/a/text()")[0]
    topictitles = topic.xpath("./dl/dt/div/a[@class='topictitle']/text()")[0]

    async with aiohttp.request('get', url, loop=loop) as result:
        body = await result.text()
        root = html.fromstring(body)
        content = root.xpath("//div[@class='content']")
        clear_content = etree.tostring(content[0], method="text", encoding='unicode')
        price = find_price(clear_content)
        return [url, author, topictitles, price, clear_content]


async def get_subjects(loop, page):
    async with aiohttp.request('get', START_HTTP, params="start=" + str(page), loop=loop) as result:
        body = await result.text()
        tasks = [loop.create_task(get_content(loop, topic)) for topic in pars_topics(body)]
        price = await asyncio.gather(*tasks, return_exceptions=True)
        return price


async def main(loop, amount_pages):
    tasks = [loop.create_task(get_subjects(loop, page)) for page in range(0, amount_pages * 40, 40)]
    subjects = await asyncio.gather(*tasks, return_exceptions=True)

    with open("parser.log", mode="w") as file:
        for page_results in subjects:
            for page_result in page_results:
                json.dump(
                    {"title": page_result[2], "url": page_result[0], "author": page_result[1], "text": page_result[4],
                     "price": page_result[3][0], "currency": page_result[3][1]}, file, ensure_ascii=False)
                file.write("\r\n")
                print(page_result)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop, AMOUNT_PAGES))
