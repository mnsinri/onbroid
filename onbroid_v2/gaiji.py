from Apex import ApexProfile
import asyncio.events

async def main():
    apex = ApexProfile("40ef9dbe-a6af-4e99-a15e-3302a2f87892")
    name = input('name >')
    print(await apex.searchProfile(name))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())