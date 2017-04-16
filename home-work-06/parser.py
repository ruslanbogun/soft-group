import asyncio
import aiohttp
from lxml import html, etree
import re

START_HTTP = "http://forum.overclockers.ua/viewforum.php?f=26"
SUBJECT = []
AMOUNT_PAGES = 2

PRICE_TEMPLATE = "([a-zA-Z0-9\.\s\(\)\-]{1,}[\s]{0,}[[Ц|ц][е|і]на]{0,}[\s]{0,}[0-9]{1,}[\s]{0,1}(грн|\$))"


def pars_topics(body):
    root = html.fromstring(body)
    topics = root.xpath('//li[contains(@class, "row bg")]')
    return topics


def find_price(content):
    raw_content = etree.tostring(content, method="text", encoding='unicode')
    prices = re.findall(PRICE_TEMPLATE, raw_content)
    return prices


async def get_content(loop, topic):
    url = "http://forum.overclockers.ua/" + topic.xpath("./dl/dt/div/a/@href")[0][2:]
    author = topic.xpath("./dl/dd[@class='author']/a/text()")[0]
    topictitles = topic.xpath("./dl/dt/div/a[@class='topictitle']/text()")[0]

    async with aiohttp.request('get', url, loop=loop) as result:
        body = await result.text()
        root = html.fromstring(body)
        content = root.xpath("//div[@class='content']")
        price = find_price(content[0])
        return [url, author, topictitles, price]


async def get_subjects(loop, page):
    async with aiohttp.request('get', START_HTTP, params="start=" + str(page), loop=loop) as result:
        body = await result.text()
        tasks = [loop.create_task(get_content(loop, topic)) for topic in pars_topics(body)]
        price = await asyncio.gather(*tasks, return_exceptions=True)
        return price


async def main(loop, amount_pages):
    tasks = [loop.create_task(get_subjects(loop, page)) for page in range(0, amount_pages * 40, 40)]
    subjects = await asyncio.gather(*tasks, return_exceptions=True)

    for page_results in subjects:
        for page_result in page_results:
            print(page_result)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop, AMOUNT_PAGES))
