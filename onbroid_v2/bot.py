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
        super().__init__()
        self.config = config
        self.dictionary = ITDict()
        self.apexRandomCharactor = ApexRandomCharactor()
        self.apexProfile = ApexProfile(self.config.api_key)
        # self.loop = asyncio.get_event_loop()

    def run(self):
        # self.loop.run_until_complete(self.start(self.config.token))
        super().run(self.config.token)

    def make_embed(self, contents='', thumbnail='', fields=[], author={}, footer=''):
        embed = None

        if contents:
            # now = datetime.datetime.utcnow() + datetime.timedelta(hours=9)
            now = datetime.datetime.utcnow()
            embed = discord.Embed(**contents, color=discord.Colour.blue(), timestamp=now)
            embed.set_footer(text=footer)

            thumbnail and embed.set_thumbnail(url=thumbnail)
            fields and [embed.add_field(name=data['name'] , value=data['value']) for data in fields]
            author and embed.set_author(name=author['name'], icon_url=author['icon_url'])
        return embed

    def parse_legends(self, legends):
        return {'name': legends['embed']['description'], 'value': '**'+legends['embed']['title']+'**'}

    async def pex_select_charactor(self, menber):
        if menber and menber.isdecimal():
            thumbnail = 'https://media.contentapi.ea.com/content/dam/apex-legends/common/logos/apex-copyright-sigil-white.png'
            contents = await self.apexRandomCharactor.get_legends(int(menber))
            return self.make_embed({ 'title': ':new: **部隊メンバー**' }, thumbnail , [self.parse_legends(legend) for legend in contents], footer='no pex, no life')
        else:
            contents = await self.apexRandomCharactor.get_legends()
            return self.make_embed(contents[0]['embed'], contents[0]['thumbnail'], contents[0]['fields'], footer='no pex, no life')

    async def pex_profile(self, name):
        result = await self.apexProfile.searchProfile(name)
        if result:
            return self.make_embed(result['embed'], result['thumbnail'], result['fields'], result['author'], footer='no pex, no life')
        else:
            return None

    async def cmd_closeHelesta(self, message, channel, *args):
        print('[cmd_colseHelesta]')
        await self.apexRandomCharactor.close_session()
        await self.apexProfile.close_session()
        await self.close()
    
    async def cmd_help(self, message, channel, *args):
        print('[cmd_help]')
        container = {
            'title': ':question: Help',
            'description': 'Prefix: `'+self.config.prefix+'`'
        }
        fields = [
            {'name': '```'+self.config.prefix+'pex```','value': 'a legend is randomly selected.'},
            {'name': '```'+self.config.prefix+'pex {num}```','value': '{num (1~3)} legends are randomly selected.'},
            {'name': '```'+self.config.prefix+'pex -refresh```','value': 'legends list updated'},
            {'name': '```'+self.config.prefix+'pex -profile {username}```','value': "show {username}'s APEX profile"},
            {'name': '```'+self.config.prefix+'{search_item}```','value': 'search {search_item} in e-words'}
        ]
        embed = self.make_embed(container, fields=fields)
        await channel.send(embed=embed)

    async def cmd_pex(self, message, channel, *args):
        print('[cmd_pex]' + ''.join(args))
        option = ''
        comment = ''
        embed = None

        args = list(args)
        for arg in args:
            print(arg)
            if arg.startswith('-'):
                option = arg.lstrip('-')
                args.remove(arg)
                break

        # どうにかしろ
        arg = args[0] if args else None

        if option:
            if option == 'refresh':
                await self.apexRandomCharactor.refresh_legends()
                return
            if option == 'profile':
                embed = await self.pex_profile(arg)
        else:
            comment = message.author.mention + ' you are ...'
            embed = await self.pex_select_charactor(arg)

        await channel.send(comment, embed=embed)

    async def cmd_search(self, message, channel, *args):
        arg = args[0] if args else None
        embed = None
        print('[search]' + arg)

        embed_contents = await self.dictionary.search(arg)
        if embed_contents:
            embed = self.make_embed(embed_contents)
            await channel.send(embed=embed)
        else:
            await channel.send('てぇてぇ閉廷！')

    async def on_message(self, message):
        message_content = message.content.strip()

        if message.author.bot:
            return

        if not message_content.startswith(self.config.prefix):
            return

        command, *args = message_content.split(' ') 
        command = command[len(self.config.prefix):].lower().strip()

        handler = getattr(self, 'cmd_' + command, None)

        if handler:
            await handler(message, message.channel, *args)
        else:
            await message.channel.send('たわけが')
