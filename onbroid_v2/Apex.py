import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup

from selector import Selector

class ApexRandomCharactor():
    def __init__(self):
        self.pathes = Selector()
        self.legends = []

    async def get_html(self, endpoint):
        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint) as response:
                return await response.text()

    def parse_html(self, htmlObject):
        return BeautifulSoup(htmlObject, 'html.parser')

    async def get_soup(self, endpoint):
        return self.parse_html(await self.get_html(endpoint))

    def fetch_text(self, soup, selector_path):
        value = soup.select_one(selector_path)
        return value.get_text('', strip=True) if value else ''
    
    def fetch_tag(self, soup, selector_path, tag):
        value = soup.select_one(selector_path)
        return value[tag]

    def parse_details(self, legend):
        name = self.fetch_text(legend, self.pathes.legend_details_name())
        value = self.fetch_text(legend, self.pathes.legend_details_value())
        return {'name': name, 'value': value}

    async def parse_legends_list(self, legendData):
        embed = {}
        embed['title'] = '**' + self.fetch_text(legendData, self.pathes.legends_name())[3:-4] + '**'
        embed['description'] = self.fetch_text(legendData, self.pathes.legends_copy())

        legendObj = {}
        legendObj['embed'] = embed
        legendObj['thumbnail'] = self.fetch_tag(legendData, self.pathes.legends_thumbnail(), 'media')

        soup = await self.get_soup('https://www.ea.com/' + self.fetch_tag(legendData, self.pathes.legends_url(), 'href'))
        details = soup.select(self.pathes.legend_details())
        fields = [self.parse_details(legend) for legend in details]
        legendObj['fields'] = fields
        

        return legendObj

    async def parse_legends(self, soupOfCharacters):
        legendsList = soupOfCharacters.select(self.pathes.catalog_container())
        legendsObjArray = [await self.parse_legends_list(data) for data in legendsList]
        return legendsObjArray

    async def refresh_legends(self):
        soupOfCharacters = await self.get_soup('https://www.ea.com/ja-jp/games/apex-legends/about/characters')
        self.legends = await self.parse_legends(soupOfCharacters)
        print('[ApexRandomCharactor] refresh')
        
    def get_legends(self):
        return self.legends[random.randint(0, len(self.legends) - 1)]
