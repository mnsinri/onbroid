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

    async def setup(self):
        await self.apexRandomCharactor.refresh_legends()

    async def start(self):
        # self.loop.run_until_complete(self.start(self.config.token))
        await super().start(self.config.token)

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
            contents = self.apexRandomCharactor.get_legends(int(menber))
            return self.make_embed({'title': ':new: **部隊メンバー**'}, thumbnail , [self.parse_legends(legend) for legend in contents], footer='no pex, no life')
        else:
            contents = self.apexRandomCharactor.get_legends()
            return self.make_embed(contents[0]['embed'], contents[0]['thumbnail'], contents[0]['fields'], footer='no pex, no life')

    async def pex_profile(self, name):
        result = await self.apexProfile.searchProfile(name)
        if result:
            return self.make_embed(result['embed'], result['thumbnail'], result['fields'], result['author'], footer='no pex, no life')
        else:
            return None

    def pex_info(self, arg):
        url = 'https://www.ea.com/ja-jp/games/apex-legends'
        items = [
            {'name': 'Legends', 'pass': '/about/characters'},
            {'name': 'Battlepass', 'pass': '/battle-pass'},
            {'name': 'News', 'pass': '/news'}
        ]
        contents = {
            'title': '',
            'description': ''
        }

        if arg:
            arg = arg.lower()
            if 'season' in arg:
                seasonIndex = arg[len('season'):]
                nowSeason = self.apexRandomCharactor.get_season()
                seasonIndex = seasonIndex if seasonIndex.isdecimal() and int(seasonIndex) > 0 and int(seasonIndex) <= nowSeason else nowSeason
                url += '/season-' + str(seasonIndex)
                contents['title'] = f'**Season{seasonIndex} Infomation**'
            else:
                for item in items:
                    if item['name'].lower() == arg:
                        about = item['name']
                        url += item['pass']
                        contents['title'] = f'**{about} Infomation**'
                        break

        if not contents['title']:
            contents['title'] = '**Apex Infomation**'
        contents['description'] += f':point_right: [link here]({url})'

        return self.make_embed(contents, footer='no pex, no life')

    async def cmd_close_helesta(self, message, channel, *args):
        print('[cmd_colse_helesta]')
        print('self.apexRandomCharactor.close_session()')
        await self.apexRandomCharactor.close_session()
        print('self.apexProfile.close_session()')
        await self.apexProfile.close_session()
        print('self.close()')
        await self.close()
    
    async def cmd_help(self, message, channel, *args):
        print('[cmd_help]')
        container = {
            'title': ':question: Help',
            'description': 'Prefix: `'+self.config.prefix+'`'
        }
        fields = [
            {'name': '```'+self.config.prefix+'pex```','value': 'A legend is randomly selected.'},
            {'name': '```'+self.config.prefix+'pex {num}``','value': '__num (1~3)__ legends are randomly selected.'},
            {'name': '```'+self.config.prefix+'pex -refresh```','value': 'Legends list is updated'},
            {'name': '```'+self.config.prefix+'pex -profile {username}```','value': "show __username__'s APEX profile"},
            {'name': '```'+self.config.prefix+'pex -info {contents}```','value': 'show link about __contents__'},
            {'name': '```'+self.config.prefix+'search {search_item}```','value': 'search __search_item__ in e-words'}
        ]
        embed = self.make_embed(container, fields=fields)
        await channel.send(embed=embed)

    async def cmd_pex(self, message, channel, *args):
        print('[cmd_pex]' + ' '.join(args))
        option = ''
        comment = ''
        embed = None

        args = list(args)
        for arg in args:
            if arg.startswith('-'):
                option = arg.lstrip('-')
                args.remove(arg)
                break

        # どうにかしろ
        arg = args[0] if args else None

        if option:
            if option == 'refresh':
                await self.apexRandomCharactor.refresh_legends()()
                comment = 'きちゃー！'
            elif option == 'profile':
                embed = self.pex_profile(arg)
                if not embed:
                    comment = f'{arg}さん...?'
            elif option == 'info':
                embed = self.pex_info(arg)
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
