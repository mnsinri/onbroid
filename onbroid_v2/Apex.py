import asyncio
import aiohttp
import random
from bs4 import BeautifulSoup

from selector import Selector

class ApexRandomCharactor():
    def __init__(self):
        self.pathes = Selector()
        self.session = aiohttp.ClientSession()
        self.legends = []

    async def close_session(self):
        await self.session.close()

    async def get_html(self, endpoint):
        async with self.session.get(endpoint) as response:
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
        
    def get_legend(self):
        return self.legends[random.randint(0, len(self.legends)-1)]
    
    def get_legends(self, team=1):
        indexList = list(range(len(self.legends)))
        popedList = random.sample(indexList, len(indexList))[:min(3, team)]
        return [self.legends[i] for i in popedList]

class ApexProfile():
    def __init__(self, api_key):
        self.pathes = Selector()
        self.api_key = api_key
        self.session = aiohttp.ClientSession()
        self.endpoint = "https://public-api.tracker.gg/v2/apex/standard/profile/origin/"

    async def close_session(self):
        await self.session.close()

    async def get_profile(self, endpoint, ):
        async with self.session.get(endpoint, headers={'TRN-Api-Key': self.api_key}) as response:
            return await response.json()

    def isAvailableUsername(self, res):
        return res.get('data')

    def parse_profile(self, res):
        if not self.isAvailableUsername(res):
            return {}

        resultObj = {}

        author = {}
        author['name'] = res['data']['platformInfo']['platformUserHandle']
        author['icon_url'] = res['data']['platformInfo']['avatarUrl']
        resultObj['author'] = author
        
        buf = res['data']['segments'][0]['stats']
        level = buf.pop('level')
        resultObj['fields'] = [{'name': k, 'value': v["displayValue"]} for k, v in buf.items()]

        resultObj['thumbnail'] = res['data']['segments'][0]['stats']['rankScore']['metadata']['iconUrl']
        
        embed = {}
        embed['title'] = '**Rank Point**: `' + res['data']['segments'][0]['stats']['rankScore']['displayValue'] + '`'
        embed['description'] = '**Account Level**: `' + level['displayValue'] + '`'
        resultObj['embed'] = embed

        return resultObj

    async def searchProfile(self, username):
        response = await self.get_profile(self.endpoint + username)
        return self.parse_profile(response)
        