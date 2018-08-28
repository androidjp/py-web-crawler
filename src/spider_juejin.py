from urllib import request
from bs4 import BeautifulSoup as bs
import os

URL_JUEJIN = 'https://juejin.im/welcome/'
OUTPUT_PATH = r'./../output/'
JUEJIN_TABS = (
    'frontend'
    , 'android', 'ios'
    , 'backend'
    , 'design'
    , 'product'
    , 'freebie'
    , 'article'
    , 'ai'
    , 'devops')


def requestJuejin(url):
    # attempt as a Browser operation
    user_agent = 'User-Agent'
    user_agent_value = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    # send request
    resp = request.Request(url)
    # mock the browser
    resp.add_header(user_agent, user_agent_value)
    resp = request.urlopen(resp)
    return resp.read().decode('utf-8')


def parseHtml(htmlCode):
    soup = bs(htmlCode, 'html.parser')
    return soup


class JuejinArticle(object):
    def __init__(self, title, url):
        self.title = title
        self.url = url

    def __str__(self):
        return f'文章标题：{self.title}\n文章链接：{self.url}'


def grepArticle(htmlContent):
    articleList = htmlContent.find_all('a', {'class', 'title'})
    allArticle = list(
        map(lambda article: JuejinArticle(article.string, 'https://juejin.im' + article.get('href')), articleList))
    return allArticle


def doGrepAndSaveFile(url, fileName='default.txt'):
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)
    htmlCode = requestJuejin(url)
    htmlCode = parseHtml(htmlCode)
    allArticle = grepArticle(htmlCode)
    with open(f'{OUTPUT_PATH}{fileName}', 'w', encoding='UTF-8') as f:
        for item in allArticle:
            f.write(f'{item.__str__()}\n')


def main():
    for item in JUEJIN_TABS:
        print(f'---grep `{item}` start---')
        doGrepAndSaveFile(f'{URL_JUEJIN}{item}', f'{item}.txt')
        print(f'---grep `{item}` finish---')


if __name__ == '__main__':
    main()
