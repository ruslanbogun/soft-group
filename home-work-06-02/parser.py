import asyncio
import aiohttp
from lxml import html, etree
import re

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Numeric
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')

Base = declarative_base()
DBSession = sessionmaker()
DBSession.configure(bind=engine)
session = DBSession()

START_HTTP = "http://forum.overclockers.ua/viewforum.php?f=26"
SUBJECT = []
AMOUNT_PAGES = 2

PRICE_TEMPLATE = "([0-9]{0,}[.,]{0,1}[0-9]{1,})[\s]{0,1}([Г|г]рн|\$)" \
                 "|[Ц|ц][е|і]на{0,1}([\s]{0,}[0-9]{0,}[.,]{0,1}[0-9]{1,})[\s]{0,1}([Г|г]рн|\$)"


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Messages(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    url = Column(String(250), nullable=False)
    title = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(Text)
    price = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(50))


def pars_topics(body):
    root = html.fromstring(body)
    return root.xpath('//li[contains(@class, "row bg")]')


def find_price(content):
    price = max(re.findall(PRICE_TEMPLATE, content)) if re.findall(PRICE_TEMPLATE, content) else [[], []]
    return [price[0] if price[0] is not "" else price[2], price[1] if price[1] is not "" else price[3]]


async def get_content(loop, topic):
    url = "http://forum.overclockers.ua/" + topic.xpath("./dl/dt/div/a/@href")[0][2:]
    author = topic.xpath("./dl/dd[@class='author']/a/text()")[0]
    topictitles = topic.xpath("./dl/dt/div/a[@class='topictitle']/text()")[0]

    async with http_session.request('get', url) as result:
        body = await result.text()
        root = html.fromstring(body)
        content = root.xpath("//div[@class='content']")
        clear_content = etree.tostring(content[0], method="text", encoding='unicode')
        price = find_price(clear_content)
        return [url, author, topictitles, price, clear_content]


async def get_subjects(loop, page):
    async with http_session.request('get', START_HTTP, params="start=" + str(page)) as result:
        body = await result.text()
        tasks = [loop.create_task(get_content(loop, topic)) for topic in pars_topics(body)]
        return await asyncio.gather(*tasks, return_exceptions=True)


async def main(loop, amount_pages):
    global http_session
    http_session = aiohttp.ClientSession()

    tasks = [loop.create_task(get_subjects(loop, page)) for page in range(0, amount_pages * 40, 40)]
    subjects = await asyncio.gather(*tasks, return_exceptions=True)
    for page_results in subjects:
        for page_result in page_results:
            user = session.query(Users).filter(Users.name == page_result[1]).first()
            if user is None:
                new_user = Users(name=page_result[1])
                session.add(new_user)
                session.commit()
                user = session.query(Users).filter(Users.name == page_result[1]).first()
            price = 0.00 if not page_result[3][0] else float(page_result[3][0].replace(",", "."))
            if session.query(Messages).filter(
                                    Messages.title == page_result[2] and Messages.author_id == user.id).first() is None:
                new_message = Messages(
                    url=page_result[0],
                    title=page_result[2],
                    author_id=user.id,
                    content=page_result[4],
                    price=price,
                    currency=page_result[3][1])
                session.add(new_message)
                session.commit()
            print(page_result)


if __name__ == '__main__':
    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(main(main_loop, AMOUNT_PAGES))
