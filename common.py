import requests
import time
from lxml import etree
from loguru import logger
import random
from tqdm import tqdm,trange
from settings import SourceDic
from urllib.parse import quote

name = '好运时间'
qname = quote(name)

for source in SourceDic:
    logger.info(source['title'])
    if source['group'] == 'A':
        searchUrl = source['query_url'] % qname
        headers = source['header']
        for i in trange(5,colour='#1A68CF',ncols=120):
            searchRes = requests.request("GET", searchUrl,  headers=headers)

            if searchRes.json() == 1:
                time.sleep(1.5)
                continue
            else:
                break
        if  searchRes.json() == 1:
            continue
        else:
            bookListUrl = source['host'] + searchRes.json()[0]['url_list']
            novelName = searchRes.json()[0]['articlename']
            author = searchRes.json()[0]['author']
        bookListRes = requests.request("GET", bookListUrl,  headers=headers)
        bookListRes.encoding = 'utf-8'
        bookListHtml = etree.HTML(bookListRes.text)
        lastChapter = bookListHtml.xpath("//html/head/meta[@property='og:novel:latest_chapter_url']/@content")[0]
        chapterCount = int(lastChapter.split('/')[-1].split('.html')[0])
        chapterUrl = bookListHtml.xpath("//html/head/meta[@property='og:url']/@content")[0]
    else:
        continue

def getNovel(chapterUrl,chapterCount):    
    fullBook = []
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

    # response.encoding = 'utf-8'
    # html = etree.HTML(response.text)
    # html.xpath("/html/body/div[3]/div/div/div/dl/dt/a/@href")
    breakpoint()