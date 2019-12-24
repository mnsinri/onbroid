from weblioDict import WeblioDict
import asyncio

gt = WeblioDict('TCP')
print(gt.endpoint)

loop = asyncio.get_event_loop()
f = asyncio.wait([gt.search()])
loop.run_until_complete(f)

print(f)
