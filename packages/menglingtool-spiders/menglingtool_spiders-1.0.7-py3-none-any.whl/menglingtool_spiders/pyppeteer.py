import asyncio
from .__pyppeteer__.action import Act
from .__pyppeteer__.request import Req


# 不支持非主线程调用
class PyppTool(Act, Req):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._loop = asyncio.get_event_loop()
        # asyncio.set_event_loop(self._loop)
        self.run(self.initBrowser())

    def run(self, *tasks):
        tasks = [self._loop.create_task(task, name=f'task-{i}') for i, task in enumerate(tasks)]
        self._loop.run_until_complete(asyncio.wait(tasks))

    def close(self):
        self.run(self.browser.close())
        self._loop.close()
