import asyncio

from bot import Onbroid
from config import Config

def main():
    loop = asyncio.get_event_loop()
    config = Config('../token.json')
    onbroid = Onbroid(config)

    loop.create_task(onbroid.setup())
    loop.create_task(onbroid.start())
    loop.run_forever()

if __name__ == "__main__":
    main()
