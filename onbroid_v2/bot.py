import asyncio
import discord
import datetime
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from ITDict import ITDict
from Apex import ApexRandomCharactor
from config import Config

class Onbroid(discord.Client):
    def __init__(self, config):
        print('[connect]')
    
        self.config = config
        self.dictionary = ITDict()
        self.apex = ApexRandomCharactor()

        self.loop = asyncio.get_event_loop()
        task = self.loop.create_task(self.apex.refresh_legends())
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
        return self.apex.get_legends()

    def make_embed(self, contents='', thumbnail='', fields=[]):
        embed = None
        if contents:
            # now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
            now = datetime.datetime.utcnow()
            embed = discord.Embed(**contents, color=discord.Colour.blue(), timestamp=now)
            embed.set_footer(text='no pex, no life')

            thumbnail and embed.set_thumbnail(url=thumbnail)
            fields and [embed.add_field(name=data['name'] , value=data['value']) for data in fields]
        return embed

    async def on_message(self, message):
        if message.author.bot \
           or not message.content[:len(self.config.prefix)].startswith(self.config.prefix):
            return

        msg_content = message.content[len(self.config.prefix):].split(' ')

        if msg_content[0] == 'close-helesta':
            print('[close]')
            await self.close()
            return

        if msg_content[0] == 'pex':
            if len(msg_content) == 2 and msg_content[1] == '--refresh':
                await self.apex.refresh_legends()
                return

            print('[pex]')
            contents = self.select_legends()
            embed = self.make_embed(contents['embed'], contents['thumbnail'], contents['fields'])

            await message.channel.send(message.author.mention + ' you are ...', embed=embed)

        elif msg_content[0] == 'help':
            print('[help]')
            
        else:
            print(f'[search] {msg_content[0]}')
            embed_contents = await self.search_term(msg_content[0])
            embed = self.make_embed(embed_contents)
            if embed:
                await message.channel.send(embed=embed)
            else:
                await message.channel.send('てぇてぇ閉廷！')
