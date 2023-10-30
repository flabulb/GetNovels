import requests
import time
from lxml import etree
from loguru import logger
import random


def getBookNumber(book_name):
    reqUrl = "https://www.xzmncy.com/api/search?q=%s " % book_name

    headersList = {
        "Host": "www.xzmncy.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76",
        "Connection": "close"
    }

    response = requests.request("GET", reqUrl, headers=headersList)
    author = response.json()['data']['search'][0]['author']
    book_number = response.json()['data']['search'][0]['book_list_url']
    breakpoint()
    return author, book_number


def getList(book_number):
    reqUrl = "https://www.xzmncy.com%s" % book_number

    headersList = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76",
        "Connection": "close"
    }

    payload = ""

    response = requests.request(
        "GET", reqUrl, data=payload,  headers=headersList)
    response.encoding = 'utf-8'
    html = etree.HTML(response.text)
    return html


def getBook(book_list):
    chapter_count = len(book_list.xpath("//*[@id=\"list\"]/dl/dd/a"))
    full_book_list = []
    for i in range(1, chapter_count+1):
        chapter_index = "".join(book_list.xpath(
            "//*[@id=\"list\"]/dl/dd[%s]/a/text()" % i))
        logger.info(chapter_index)
        chapter_url = "".join(book_list.xpath(
            "//*[@id=\"list\"]/dl/dd[%s]/a/@href" % i))
        reqUrl = "https://www.xzmncy.com%s" % chapter_url
        headersList = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.76",
            "Connection": "close"
        }
        response = requests.request("GET", reqUrl,  headers=headersList)
        response.encoding = 'utf-8'
        html = etree.HTML(response.text)
        chapter_content = "\n".join(html.xpath(
            "//*[@id=\"htmlContent\"]/p/text()"))
        chapter = chapter_index + '\n' + chapter_content
        full_book_list.append(str(chapter))
        t = random.uniform(4, 7)
        time.sleep(t)
    full_book = "\n".join(full_book_list)
    return full_book


def main(book_name):
    author, book_number = getBookNumber(book_name)
    book_list = getList(book_number)
    book = getBook(book_list)
    f = open(f'./{book_name}-{author}.txt', 'w')
    f.writelines(str(book))
    f.close()


main('仙道第一小白脸')
