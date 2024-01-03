import aiopypes

import asyncio

import time

from aiopypes.balance import CongestionLoadBalancer, RoundRobinLoadBalancer


app = aiopypes.App()

@app.task(interval=1.0)
async def trigger():
    print("emitting trigger")
    return 1.0


# @app.task(balancer=RoundRobinLoadBalancer())
# async def route_a(input: aiopypes.Stream):
#     async for sleep in input:
#         await asyncio.sleep(sleep)
#         yield 'A'

# @app.task(scale=10)
# async def route_b(input: aiopypes.Stream):
#     async for sleep in input:
#         await asyncio.sleep(sleep)
#         yield 'B'

# @app.task(scale=1)
# async def task1(input: aiopypes.Stream):
#     async for router, sleep in input:
#         await asyncio.sleep(5 * sleep)
#         yield router, 1, input.queue.qsize()

# @app.task(scale=50)
# async def task2(input: aiopypes.Stream):
#     async for router, sleep in input:
#         await asyncio.sleep(5 * sleep)
#         yield router, 2, input.queue.qsize()

@app.task()
async def classify(input: aiopypes.Stream):
    async for _ in input:
        yield 'A', 'message from A'
        yield 'B', 'message from B'

@app.task()
async def mapped_task(input: aiopypes.Stream):
    async for _ in input:
        yield f'in a mapped task with {_}'

@app.task()
async def receive_a(input: aiopypes.Stream):
    async for obj in input:
        yield f"A: received {obj}"

@app.task()
async def receive_b(input: aiopypes.Stream):
    async for obj in input:
        yield f"B: received {obj}"

@app.task()
async def log(input: aiopypes.Stream):
    async for obj in input:
        print(f"received general: {obj}")
        yield 'A', 'whatever_a'
        yield 'B', 'whatever_b'

@app.task()
async def class_func(input: aiopypes.Stream):
    async for obj in input:
        print(f"received class: {obj}")
        yield

if __name__ == '__main__':

    # pipeline = trigger \
    #            .map(classify) \
    #            .fork(receive_a, receive_b, routes=['A', 'B'])
    #            .map([a,b])
    #            .map(receive_a, receive_b, routes=['A', 'B'])
    
    # trigger.map(classify)
    # classify.fork(receive_a, receive_b, routes=['A', 'B'])
    # trigger.run()

    # leg1 = trigger.map(classify)
    # print([s.name for s in leg1.scope])
    # leg2 = leg1.fork(receive_a, receive_b, routes=['A', 'B'])
    # leg2.run()

    pipeline = trigger \
                .map(mapped_task, mapped_task, mapped_task) \
                .reduce(log) \
                .fork(class_func, routes=['A'])


    # trigger.run()

    pipeline.run()