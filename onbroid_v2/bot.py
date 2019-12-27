import asyncio
import discord

from ITDict import ITDict
from config import Config

class Onbroid(discord.Client):
    def __init__(self, config):
        self.config = config
        super().__init__()

    def run(self):
        super().run(self.config.token)

    async def close(self):
        if not super().is_closed():
            await super().close()

    async def search_term(self, source_text):
        ITdictionary = ITDict(source_text)
        return await ITdictionary.search()

    async def on_message(self, message):
        if message.author.bot \
           or not message.content[:len(self.config.prefix)].startswith(self.config.prefix):
            return

        msg_content = message.content[len(self.config.prefix):].split(' ')

        if not len(msg_content) == 1:
            #Will be added
            return

        print(f"[search] {msg_content[0]}")

        if msg_content[0] == 'onbroid':
            await self.close()
            return

        embed_contents = await self.search_term(msg_content[0])
        print(f"[return] {embed_contents}")
        embed = discord.Embed(**embed_contents)
        # embed.add_field(name='name', value='value', inline=True)
        await message.channel.send(embed=embed)
