"""
    Structure that coordinates the internals of reading in streamed data (through a `Stream`),
    coordinating scaled processing of it (with a `Scaler`), and sending it to downstream
    tasks (through a `Balancer`).

    .. image:: _static/task_design.png

    The design describes how data processing is coordinated within a Task object.
"""
import asyncio

from typing import Callable

from .stream import Stream
from .pipeline import Pipeline
from .balance import AbstractLoadBalancer, DefaultLoadBalancer
from .scale import AbstractTaskScaler, DefaultTaskScaler, StaticTaskScaler
from .signal import Signal


class Task:

    def __init__(self,
                 name: str,
                 function: Callable,
                 lock: asyncio.Lock = None,
                 scale: int = None,
                 scaler: AbstractTaskScaler = None,
                 balancer: AbstractLoadBalancer = None,
                 interval: float = None,
                 pipeline: Pipeline = None):
        """_summary_

        Args:
            name (str): _description_
            function (Callable): _description_
            lock (asyncio.Lock, optional): _description_. Defaults to None.
            scale (int, optional): _description_. Defaults to None.
            scaler (AbstractTaskScaler, optional): _description_. Defaults to None.
            balancer (AbstractLoadBalancer, optional): _description_. Defaults to None.
            interval (float, optional): _description_. Defaults to None.
        """
        self.name = name
        self.function = function
        self.lock = lock
        self.scaler = scaler
        self.balancer = balancer
        self.interval = interval
        self.pipeline = pipeline

        if not self.scaler:
            if not scale or scale <= 0:
                self.scaler = DefaultTaskScaler()
            else:
                self.scaler = StaticTaskScaler(scale)
        if not balancer:
            self.balancer = DefaultLoadBalancer()
        self.input = Stream()
        self.output = []
        self.runners = []
        self.locks = []
        self.routes = []

    def run(self, **kwargs):
        """_summary_

        Returns:
            _type_: _description_
        """
        pipeline = self.get_pipeline()
        return getattr(pipeline, "run")(**kwargs)

    def copy(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.__class__(
            name=self.name,
            function=self.function,
            lock=self.lock,
            scaler=self.scaler.copy(),
            balancer=self.balancer.copy(),
            interval=self.interval,
            pipeline=self.pipeline
        )

    def get_pipeline(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        if not self.pipeline:
            self.pipeline = Pipeline(tasks=[self])
        return self.pipeline

    def pipe(self, *tasks):
        """_summary_

        Args:
            routes (list, optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """
        pipeline = self.get_pipeline()

        for task in tasks:
            pipeline.tasks.append(task)
            self.output.append(task)
            task.pipeline = pipeline
            task.lock = pipeline.lock

        pipeline.scope = [*tasks]

        return pipeline

    def fork(self, *tasks, routes: list = []):
        """_summary_

        Args:
            routes (list, optional): _description_. Defaults to [].

        Returns:
            _type_: _description_
        """
        pipeline = self.get_pipeline()

        for task in tasks:
            pipeline.tasks.append(task)
            self.output.append(task)
            task.pipeline = pipeline
            task.lock = pipeline.lock

        pipeline.scope = [*tasks]

        self.routes = routes

        return pipeline
        
    def map(self, *tasks):
        """
        The `map` function takes a list of tasks and routes, creates new tasks based on the input tasks,
        and adds them to the scope.
        
        Args:
          routes (list): The `routes` parameter is a list that specifies the routes that the tasks should
        follow. It is an optional parameter and its default value is an empty list.
        
        Returns:
          The `map` method is returning `self`.
        """
        pipeline = self.get_pipeline()
        
        new_scope = []
        for task in tasks:
            task_copy = task.copy()
            pipeline.tasks.append(task_copy)
            self.output.append(task_copy)
            new_scope.append(task_copy)
            task_copy.pipeline = pipeline
            task_copy.lock = pipeline.lock

        pipeline.scope = new_scope

        return pipeline

    def reduce(self, task):
        """_summary_

        Returns:
            _type_: _description_
        """
        pipeline = self.get_pipeline()

        pipeline.tasks.append(task)
        self.output.append(task)
        task.pipeline = pipeline
        task.lock = pipeline.lock

        pipeline.scope = [task]

        return pipeline

    def get_timer_iter(self, *args, **kwargs):
        """_summary_
        """
        async def timer():
            while True:
                await asyncio.sleep(self.interval)
                yield await self.function(*args, **kwargs)
        
        return timer()

    def get_function_iter(self, *args, **kwargs):
        """_summary_

        Returns:
            _type_: _description_
        """
        return self.function(self.input, *args, **kwargs)

    def iterator(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        if self.interval != None:
            return self.get_timer_iter()

        else:
            return self.get_function_iter()

    def multiplex(self, route, output):
        """_summary_

        Args:
            route (_type_): _description_
            output (_type_): _description_

        Returns:
            _type_: _description_
        """
        if route in self.routes:
            index = self.routes.index(route)
            return [self.output[index]]
        else:
            return []

    async def send(self, obj: object):
        """_summary_

        Args:
            obj (object): _description_
        """
        output = self.output

        if self.routes:
            output = self.multiplex(obj[0], output)
            if len(obj[1:]) == 1:
                obj = obj[1]
            else:
                obj = obj[1:]

        elif self.balancer:
            output = self.balancer.balance(self.output)

        enqueue = [o.input.enqueue(obj) for o in output]

        await asyncio.gather(*enqueue)

    async def run_async_single(self, name: str, lock: asyncio.Lock):
        """_summary_

        Args:
            name (str): _description_
            lock (asyncio.Lock): _description_
        """
        async def iterator(*args, **kwargs):
            async for f in self.iterator(*args, **kwargs):
                if (lock.locked() or self.lock.locked()):
                    return
                else:
                    yield f

        async for o in iterator():
            await self.send(o)

    async def add_runner(self):
        """_summary_
        """
        ct = len(self.runners)
        name = f"{self.name}-{ct}"
        lock = asyncio.Lock()
        runner = asyncio.create_task(self.run_async_single(name, lock), name=name)
        self.locks.append(lock)
        self.runners.append(runner)

    async def remove_runner(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        runner = self.runners.pop()
        lock = self.locks.pop()
        try:
            await lock.acquire()
            await asyncio.wait_for(runner, timeout=10)
            return runner
        except (asyncio.TimeoutError, asyncio.CancelledError) as e:
            runner.cancel()
            await asyncio.wait_for(runner, timeout=30)

    async def shutdown(self):
        """_summary_
        """
        sigterms = [self.input.enqueue(Signal.TERM) for _ in self.runners]
        closures = [self.remove_runner() for _ in self.runners]
        await asyncio.gather(*closures, *sigterms)

    async def run_async(self):
        """_summary_
        """
        while not self.lock.locked():
            scale = self.scaler.scale(self.runners, self.input)
            if scale > 0:
                for _ in range(scale):
                    await self.add_runner()
            if scale < 0:
                for _ in range(abs(scale)):
                    await self.remove_runner()
            await asyncio.sleep(self.scaler.sleep())

        await self.shutdown()
