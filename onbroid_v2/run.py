import asyncio

from bot import Onbroid
from config import Config

if __name__ == "__main__":
    config = Config('../token.json')

    bot = Onbroid(config)
    bot.run()
