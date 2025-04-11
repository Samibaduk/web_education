import asyncio

COEFF = 0.01


async def do_task(unit):
    name, time1, timeshow1, time2, timeshow2 = unit
    print(f'{name} started the 1 task.')
    await asyncio.sleep(COEFF * time1)
    print(f'{name} moved on to the defense of the 1 task.')
    await asyncio.sleep(COEFF * timeshow1)
    print(f'{name} completed the 1 task.')
    print(f'{name} is resting.')
    await asyncio.sleep(COEFF * 5)
    print(f'{name} started the 2 task.')
    await asyncio.sleep(COEFF * time2)
    print(f'{name} moved on to the defense of the 2 task.')
    await asyncio.sleep(COEFF * timeshow2)
    print(f'{name} completed the 2 task.')


async def interviews(*args):
    tasks = [
        asyncio.create_task(do_task(x)) for x in args
    ]
    await asyncio.gather(*tasks)