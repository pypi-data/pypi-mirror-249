from .base import Body
import asyncio


class Act(Body):
    # 切换当前显示窗口
    async def taskHandoff(self, index):
        pagers = await self.getTaskPagers()
        pager = pagers[index]
        await pager.bringToFront()

    async def newGet(self, url, task_index=0, timeout=30, waituntil='load'):
        pager = (await self.getTaskPagers())[task_index]
        await pager.evaluate('document.getElementsByTagName("html")[0].remove()')
        await pager.goto(url, options={'waitUntil': waituntil, 'timeout': timeout * 1000})

    async def close_page(self, task_index=0):
        pagers = await self.getTaskPagers()
        pager = pagers[task_index]
        await pager.close()
        pagers.remove(pager)

    # 添加所有有效的cookies，提示无效的cookies
    async def addCookies(self, cookies, task_index=0, iftz=True):
        pager = (await self.getTaskPagers())[task_index]
        for cookie in cookies:
            try:
                await pager.setCookie(cookie)
            except:
                if iftz: print('[cookie无效]', cookie)

    async def screenshot(self, filepath, task_index=0):
        pager = (await self.getTaskPagers())[task_index]
        await pager.screenshot({'path': filepath})

    # 跳转至底部
    async def jumpBottom(self, task_index=0):
        pager = (await self.getTaskPagers())[task_index]
        await pager.evaluate('window.scrollBy(0, document.body.scrollHeight)')

    # 模拟下滑至底部
    async def scroll(self, task_index=0):
        pager = (await self.getTaskPagers())[task_index]
        await pager.evaluate('_ => {window.scrollBy(0, window.innerHeight);}')

    # 获取元素属性或文本
    async def getWaitElementValues(self, xpath, task_index=0, attribute=None, minnum=1, timeout=20):
        pager = (await self.getTaskPagers())[task_index]
        elements = []
        for i in range(timeout):
            elements = await pager.xpath(xpath)
            if len(elements) >= minnum:
                break
            else:
                await asyncio.sleep(1)

        assert len(elements) >= minnum, '[超时] %s' % xpath
        if attribute is None:
            return elements
        elif attribute == 'text':
            attribute = 'textContent'
        attributes = list()
        for element in elements:
            # 获取属性值
            attributes.append(await (await element.getProperty(attribute)).jsonValue())

        return attributes

    '''js_str可以为tag、#id.class、.class、#id等形式'''

    # 触发输入事件
    async def keyInput(self, js_str, value, task_index=0, delay=100):
        pager = (await self.getTaskPagers())[task_index]
        await pager.type(js_str, value, {'delay': delay})

    # 触发点击事件
    async def click(self, js_str, task_index=0):
        pager = (await self.getTaskPagers())[task_index]
        # 浏览器不能处于最小化，否则会一直等待
        await pager.click(js_str)

    # 模拟滑块拖动
    async def slideDrag(self, js_str, x, task_index=0, delay=1500):
        pager = (await self.getTaskPagers())[task_index]
        await pager.hover(js_str)  # 不同场景的验证码模块能名字不同。
        await pager.mouse.down()
        await pager.mouse.move(x, 0, {'delay': delay})
        await pager.mouse.up()

    # 聚焦元素，便于直接调用鼠标或键盘操作
    async def focus(self, js_str, task_index=0):
        pager = (await self.getTaskPagers())[task_index]
        await pager.focus(js_str)
