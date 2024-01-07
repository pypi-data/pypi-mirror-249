from .base import Body
import asyncio


class Req(Body):

    # 发送get请求
    async def request_get(self, url, task_index=0):
        pager = (await self.getTaskPagers())[task_index]
        await pager.evaluate("""
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '%s', true);
            window.text=-1;
            xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            xhr.onload = function () {
                window.text= this.responseText;
            };
            xhr.send();
        """ % url)

    # 发送post请求
    async def request_post(self, url, data, task_index=0):
        pager = (await self.getTaskPagers())[task_index]
        if type(data) == dict:
            data = '&'.join(["{key}={value}".format(key=key, value=data[key]) for key in data.keys()])
        await pager.evaluate("""
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '%s', true);
            window.text=-1;
            xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
            xhr.onload = function () {
                window.text= this.responseText;
            };
            xhr.send(%s);
        """ % (url, data))

    # 等待获取发送后的返回值
    async def wait_getResponse(self, maxci=10, mintime=0.5, task_index=0):
        pager = (await self.getTaskPagers())[task_index]
        for i in range(maxci):
            await asyncio.sleep(mintime)
            text = await pager.evaluate("return window.text;")
            if text is None:
                print("没有进行发送请求，无返回值")
                return ""
            if text != -1: return text
        print('等待时间已过，没有获取到返回值...')
        return ""
