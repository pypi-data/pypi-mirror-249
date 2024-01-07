from pyppeteer import launch
import asyncio


class Body:
    def __init__(self, executablePath=None, datapath=None, proxies=None,
                 headless=False, minload=False,
                 is_iphone=False, user_agent=None,
                 ):
        self.browser = None
        self._map_pagers = {}
        self.executablePath = executablePath
        self.datapath = datapath
        self.proxies = proxies
        # self.max_window = max_window
        self.headless = headless
        self.minload = minload
        self.is_iphone = is_iphone
        self.user_agent = user_agent or "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"

    async def getTaskPagers(self):
        task_name = asyncio.current_task().get_name()
        if self._map_pagers.get(task_name) is None:
            self._map_pagers[task_name] = []
        pagers = self._map_pagers[task_name]
        if len(pagers) == 0:
            pager = await self.browser.newPage()
            await self._setPage(pager)
            pagers.append(pager)
        return pagers

    async def _setPage(self, *pagers):
        # if min_window: ()  # 浏览器窗口最小化
        # 防止反爬虫检测
        # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
        for pager in pagers:
            await pager.evaluateOnNewDocument(
                '() =>{Object.defineProperties(navigator,{webdriver:{get: () => undefined}})}')
            # 设置窗口尺寸
            await pager.setViewport({'width': 1920, 'height': 1080})
            # 模拟手机端
            if self.is_iphone:
                await pager.setUserAgent(
                    "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1")
            else:
                await pager.setUserAgent(self.user_agent)

    async def initBrowser(self):
        arglist = ['--enable-automation', '--no-sandbox', '--log-level=30']
        if self.datapath: arglist.append(f'--user-data-dir={self.datapath}')
        if self.proxies: arglist.append('--proxy-server=' + self.proxies)  # 使用代理
        arglist.append("--window-size=1960,1080")
        # 最低资源加载,图片禁用暂不生效
        if self.minload:
            arglist.append('--disable-gpu')
            arglist.append("--disable-javascript")
            arglist.append('blink-settings=imagesEnabled=false')
            arglist.append('--profile.managed_default_content_settings.images=2')
        # 语言默认英文
        # arglist.append('--lang=en_US')
        # 忽略私密链接
        arglist.append('--ignore-certificate-errors')
        # 关闭自动化提示框
        arglist.append('--disable-infobars')
        arglist.append('--permissions.default.stylesheet=2')
        self.browser = await launch(executablePath=self.executablePath, headless=self.headless,
                                    autoClose=False, dumpio=True, args=arglist)
        pagers = await self.browser.pages()
        self._map_pagers['task-0'] = pagers
        await self._setPage(*pagers)

    async def newWindow(self):
        pagers = await self.getTaskPagers()
        pager = await self.browser.newPage()
        await self._setPage(pager)
        pagers.append(pager)
