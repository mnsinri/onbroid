import asyncio
import aiohttp
from bs4 import BeautifulSoup

from selector import Selector

class ITDict():
    def __init__(self):
        self.pathes = Selector()
        self.endpoint = 'http://e-words.jp/w/'
        self.contents = dict()

    # @param  source_text
    # @return contents
    async def search(self, source_text):
        # print(f'endpoint: {self.endpoint + source_text + ".html"}')
        html_obj = await self.get_html(self.endpoint + source_text + '.html')
        # print(f'html_obj: {html_obj}')
        soup = self.parse_html(html_obj)
        contents = self.edit_result(soup)
        return contents

    # @param  endpoint
    # @return HTMLObject
    async def get_html(self, endpoint):
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                return await response.text()

    # @param  HTMLObject
    # @return BeautifulSoupObject
    def parse_html(self, html_object):
        return BeautifulSoup(html_object, 'html.parser')

    # @param  BeautifulSoupObject
    def edit_result(self, soup):
        contents = {}
        title = self.fetch_text(soup, self.pathes.term_path()) or self.fetch_text(soup, self.pathes.term_path_jp())
        # print(f'title: {title}')
        if title:
            contents.update(self.create_content(contents, 'title', title, '**', ':mag:'))
            contents.update(self.create_content(contents, 'title', self.fetch_text(soup, self.pathes.term_detail_path())))
            contents.update(self.create_content(contents, 'description', self.fetch_text(soup, self.pathes.term_meaning_path())))
            print(f'contents: {contents}')
        return contents

    # @param  BeautifulSoupObject
    # @param  contents_key
    # @return text
    def fetch_text(self, soup, selector_path):
        value = soup.select_one(selector_path)
        text = value.get_text().replace('\xa0', '') if value else ''
        return text

    # @param  contents
    # @param  contents_key
    # @param  value
    # @param  markdown
    # @param  emoji
    def create_content(self, contents, contents_key, value, markdown='', emoji=''):
        text = emoji + markdown + value + markdown
        if contents_key in contents:
            contents[contents_key] += text
        else:
            contents[contents_key] = text
        return contents
