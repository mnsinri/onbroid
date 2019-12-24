import asyncio
import aiohttp
from bs4 import BeautifulSoup

# from embed import Embed
from selector import Selector

class WeblioDict():
    def __init__(self, source_text):
        self.text = source_text
        self.endpoint = 'https://www.sophia-it.com/content/' + self.text

        self.pathes = Selector()

    # @return contents
    async def search(self):
        html_obj = await self.get_html(self.endpoint)
        soup = self.parse_html(html_obj)
        contents = self.edit_result(soup)
        print(contents)
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
    # @return contents
    def edit_result(self, soup):
        contents = dict()
        contents.update(self.find_selector_one(soup, 'title', self.pathes.term_path()))
        contents.update(self.find_selector(soup, 'description', self.pathes.meaning_path()))
        return contents

    # @param  BeautifulSoupObject
    # @param  contents_key
    # @param  selector_path
    # @return content
    def find_selector_one(self, soup, contents_key, selector_path):
        content = dict()
        value = soup.select_one(selector_path)
        print(value)
        content[contents_key] = value.get_text() if value else ''
        return content

    # @param  BeautifulSoupObject
    # @param  contents_key
    # @param  selector_path
    # @return content
    def find_selector(self, soup, contents_key, selector_path):
        content = dict()
        values = soup.select(selector_path)
        print(values)
        content[contents_key] = '\n'.join([value.get_text() if value else '' for value in values])
        return content
