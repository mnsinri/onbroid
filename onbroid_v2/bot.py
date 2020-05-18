import asyncio
import discord
import datetime
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from ITDict import ITDict
from Apex import ApexRandomCharactor, ApexProfile
from config import Config

class Onbroid(discord.Client):
    def __init__(self, config):
        print('[connect]')
    
        self.config = config
        self.dictionary = ITDict()
        self.apexRandomCharactor = ApexRandomCharactor()
        self.apexProfile = ApexProfile(self.config.api_key)

        self.loop = asyncio.get_event_loop()
        task = self.loop.create_task(self.apexRandomCharactor.refresh_legends())
        self.loop.run_until_complete(task)

        # self.set_interval_for_refresh()

        super().__init__()

    # async def refresh(self):
    #     # self.loop.create_task(self.apex.refresh_legends())
    #     await self.apex.refresh_legends()
    #     print('create task')

    # def run_thread(self):
    #     today = datetime.datetime.today()
    #     delta = datetime.timedelta(days=1)
    #     period = datetime.datetime(today.year, today.month, today.day, 4, 5)
    #     if today.hour >= 4 and today.minute >= 5:
    #         period += delta
    #     print('init date')

    #     while True:
    #         # asyncio.run_coroutine_threadsafe(self.refresh(), self.loop)
    #         print('asyncio.run_coroutine_threadsafe(self.refresh(), self.loop)')
    #         now = datetime.datetime.today()
    #         print('sleep start')
    #         # sleep((period - now).seconds)
    #         sleep(10)
    #         print('sleep end')
    #         period += delta
    
    # def set_interval_for_refresh(self):
    #     self.loop = asyncio.get_event_loop()
    #     self.pool = ThreadPoolExecutor(max_workers=1)
    #     print('thread')
    #     self.refresh_interval_thread = Thread(target=self.run_thread())
    #     self.refresh_interval_thread.start()

    def run(self):
        super().run(self.config.token)

    async def close(self):
        if not super().is_closed():
            await super().close()

    async def search_term(self, source_text):
        return await self.dictionary.search(source_text)

    def select_legends(self):
        return self.apexRandomCharactor.get_legends()

    def make_embed(self, contents='', thumbnail='', fields=[], author={}):
        embed = None
        if contents:
            # now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
            now = datetime.datetime.utcnow()
            embed = discord.Embed(**contents, color=discord.Colour.blue(), timestamp=now)
            embed.set_footer(text='no pex, no life')

            thumbnail and embed.set_thumbnail(url=thumbnail)
            fields and [embed.add_field(name=data['name'] , value=data['value']) for data in fields]
            author and embed.set_author(name=author['name'], icon_url=author['icon_url'])
        return embed

    async def on_message(self, message):
        if message.author.bot \
           or not message.content[:len(self.config.prefix)].startswith(self.config.prefix):
            return

        msg_content = message.content[len(self.config.prefix):].split(' ')
        length = len(msg_content)

        if msg_content[0] == 'close-helesta':
            print('[close]')
            await self.apexRandomCharactor.close_session()
            await self.apexProfile.close_session()
            await self.close()
            return

        if msg_content[0] == 'pex':
            print('[pex]')
            if length >= 2:
                if msg_content[1] == '-refresh':
                    await self.apexRandomCharactor.refresh_legends()

                elif msg_content[1] == '-profile':
                    if length == 3:
                        result = await self.apexProfile.searchProfile(msg_content[2])
                        if result:
                            embed = self.make_embed(result['embed'], result['thumbnail'], result['fields'], result['author'])
                            await message.channel.send(embed=embed)
                            return

                    await message.channel.send('てぇてぇ閉廷！')
            else:
                contents = self.select_legends()
                embed = self.make_embed(contents['embed'], contents['thumbnail'], contents['fields'])
                await message.channel.send(message.author.mention + ' you are ...', embed=embed)

        elif msg_content[0] == 'help':
            print('[help]')
            container = {
                'title': ':question: Help',
                'description': 'Prefix: `'+self.config.prefix+'`'
            }
            fields = [
                {'name': '```'+self.config.prefix+'pex```','value': 'legends are randomly selected.'},
                {'name': '```'+self.config.prefix+'pex -refresh```','value': 'legends list updated'},
                {'name': '```'+self.config.prefix+'pex -profile {USERNAME}```','value': "show {USERNAME}'s APEX profile"},
                {'name': '```'+self.config.prefix+'{SEARCH_ITEM}```','value': 'search {SEARCH_ITEM} in e-words'}
            ]
            embed = self.make_embed(container, fields=fields)
            await message.channel.send(embed=embed)
            
        else:
            print(f'[search] {msg_content[0]}')
            embed_contents = await self.search_term(msg_content[0])
            embed = self.make_embed(embed_contents)
            if embed:
                await message.channel.send(embed=embed)
            else:
                await message.channel.send('てぇてぇ閉廷！')
