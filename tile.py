import asyncio

from aiohttp import ClientSession

from pytile import Client
from pytile.errors import TileError

import json
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


async def main():
    """Run."""
    global filename
    async with ClientSession() as websession:
        print("Ran once")
        try:
            # Create a client:
            client = Client('royce1998@gmail.com', 'Usable19', websession)
            await client.async_init()

            #print('Showing active Tiles:')
            #print(await client.tiles.all())
            r = await client.tiles.all()
            #print(r)
            #sub_dict = {k:r[k] for k in ('timestamp','latitude','longitude') if k in r}
            #print(sub_dict)
            dicts = []
            for dict in r:
                #print(dict)
                temp_dict = {'uuid':dict['tileState']['uuid'],'timestamp':dict['tileState']['timestamp'], 'latitude':dict['tileState']['latitude'], 'longitude':dict['tileState']['longitude']}
                dicts.append(temp_dict)
            json_input = {'tiles':dicts}
            with open(filename, 'w') as outfile:
                json.dump(json_input, outfile, sort_keys=True, indent=4)

            #print('Showing all Tiles:')
            #print(await client.tiles.all(show_inactive=True))
        except TileError as err:
            print(err)

def job():
    global filename
    filename = datetime.now().strftime("%Y%m%d-%H%M%S.json")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())

scheduler = BlockingScheduler()
#scheduler.add_job(job, 'interval', hours=1)
#scheduler.add_job(job, 'interval', seconds=5)
scheduler.add_job(job, 'interval', minutes=15)
scheduler.start()
