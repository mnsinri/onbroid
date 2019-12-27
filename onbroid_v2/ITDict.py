import asyncio
import aiohttp
from bs4 import BeautifulSoup

from selector import Selector

class ITDict():
    def __init__(self, source_text):
        self.text = source_text
        self.endpoint = 'http://e-words.jp/w/' + self.text
        self.pathes = Selector()
        self.contents = dict()

    # @return contents
    async def search(self):
        html_obj = await self.get_html(self.endpoint)
        soup = self.parse_html(html_obj)
        self.edit_result(soup)
        self.return_contents()

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
        self.update_contents('title', self.fetch_text(soup, self.pathes.term_path()), '**', ':mag:')
        self.update_contents('title', self.fetch_text(soup, self.pathes.term_detail_path()))
        self.update_contents('description', self.fetch_text(soup, self.pathes.term_meaning_path()))

    # @param  BeautifulSoupObject
    # @param  contents_key
    # @return text
    def fetch_text(self, soup, selector_path):
        value = soup.select_one(selector_path)
        text = value.get_text().replace('\xa0', '') if value else ''
        return text

    # @param  contents_key
    # @param  markdown
    # @param  emoji
    def update_contents(self, contents_key, value, markdown = '', emoji = ''):
        text = emoji + markdown + value + markdown
        if contents_key in self.contents:
            self.contents[contents_key] += text
        else:
            self.contents[contents_key] = text

    # @param  contents
    def return_contents(self):
        return self.contents
