import asyncio
from damn_people import ret_people

list_people = ret_people()
#list_people = {'hum1': 'Pain', 'hum2': 'Pain', 'hum3': 'Pain', 'hum4': 'Pain'}
tasks = []

async def teambuild(list_people):
    for hum in list_people:
        if list_people.get(hum) == 'Pain':
            await asyncio.sleep(1)
            print(hum + ' is pain')
            tasks.append(asyncio.ensure_future(healer_pain()))
        elif list_people.get(hum) == 'Thirst':
            await asyncio.sleep(1)
            print(hum + ' is thirst')
            tasks.append(asyncio.ensure_future(healer_thirst()))
        elif list_people.get(hum) == 'Insomnia':
            await asyncio.sleep(1)
            print(hum + ' is insomnia')
            tasks.append(asyncio.ensure_future(healer_insomnia()))
        elif list_people.get(hum) == 'Deadline':
            await asyncio.sleep(1)
            print(hum + ' is deadline')
            tasks.append(asyncio.ensure_future(healer_deadline()))

    await asyncio.wait(tasks)

async def healer_pain():
    await asyncio.sleep(5)
    print('relieved of pain!')

async def healer_thirst():
    await asyncio.sleep(5)
    print('relieved of thirst!')

async def healer_insomnia():
    await asyncio.sleep(5)
    print('relieved of insomnia!')

async def healer_deadline():
    await asyncio.sleep(5)
    print('relieved of deadline!')

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete(teambuild(list_people))
print('\nEveryone is alive!!!')
ioloop.close()