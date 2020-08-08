from bot import Onbroid
from config import Config

def main():
    config = Config('../token.json')
    onbroid = Onbroid(config)

    onbroid.run()

if __name__ == "__main__":
    main()
