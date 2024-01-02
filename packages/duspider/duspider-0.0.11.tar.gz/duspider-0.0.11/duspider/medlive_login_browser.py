# -*- coding: utf-8 -*-
# @project: duspider
# @Author：dyz
# @date：2023/12/22 16:02
# 医脉通登录
import json
import time
from pathlib import Path
from random import choice
from typing import List
import logging

import requests
from parsel import Selector
from playwright.async_api import async_playwright

from duspider.tools import get_ua

logger = logging.getLogger("duspider.medlivelogin")


class MedLiveLogin:
    def __init__(self, auth: list, ws=None, max_retry=5, timeout=20):
        self.login_url = 'https://www.medlive.cn/auth/login'
        self.download_url = 'https://guide.medlive.cn/guide/download'
        self.params = {'service': 'https://www.medlive.cn/'}
        self.headers = {'user-agent': get_ua()}
        self.ws = ws
        self.max_retry = max_retry
        self.timeout = timeout
        self.headers = {
            'DNT': '1',
            'Origin': 'https://www.medlive.cn',
            'Pragma': 'no-cache',
            # 'Referer': url,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': get_ua(),
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'}
        self.user_list: List[(str, str)] = auth
        self.cookies_path = Path('cookies.json')
        if not self.cookies_path.exists():
            self.cookies_path.touch()
        self.cookies = None
        self.browser = None
        self.context = None
        self.page = None

        self.sess = None

        self.path = Path(__file__).parent

    def get_user(self):
        return choice(self.user_list)

    async def login(self, url=None):
        cookies = None
        with open(self.cookies_path, 'r', encoding='utf-8') as f:
            data = f.read()
            if data:
                cookies = json.loads(data)
                self.cookies = cookies
                if self.sess:
                    self.sess.close()
                self.sess = requests.Session()
                self.sess.headers = self.headers
                self.sess.max_redirects = 80
                # self.sess.cookies = dict_from_cookiejar(cookies)
                # if url:
                #     await self.page.goto(url)
                # if not await self.test():
                #     cookies = None
                return

        async with async_playwright() as playwright:
            # self.browser = await playwright.chromium.connect_over_cdp(self.ws)
            # self.context = await self.browser.new_context()
            # self.page = await self.context.new_page()
            # js = """Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});"""
            # await self.page.add_init_script(js)

            # self.browser = await playwright.chromium.connect_over_cdp(self.ws)
            self.browser = await playwright.chromium.launch(headless=False)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            js = """Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});"""
            await self.page.add_init_script(js)

            await self.page.goto(self.login_url)
            await self.page.click('div.rightTab-R')
            user, pwd = self.get_user()
            await self.page.fill('#username', user)
            await self.page.fill('#showPassword', pwd)
            time.sleep(2)
            await self.page.click('#loginsubmit')
            if url:
                await self.page.goto(url)
            await self.page.reload()
            cookies = await self.context.cookies()
            cookies_dict = {}
            for row in cookies:
                if 'medlive' in row["domain"]:
                    cookies_dict[row["name"]] = row["value"]
            item = {
                'browserCookies': cookies,
                'Cookies': cookies_dict,
            }
            # 保存cookie信息到文件
            with open('cookies.json', 'w', encoding='utf-8') as f:
                json.dump(item, f, ensure_ascii=False)

            # self.cookies = cookies
            # if self.sess:
            #     self.sess.close()
            # self.sess = requests.Session()
            # self.sess.headers = self.headers
            #
            # with open(self.cookies_path, 'w', encoding='utf-8') as f:
            #     json.dump(cookies_dict, f, ensure_ascii=False)
            return

    async def load_sess(self, url=None):
        if not self.sess:
            await self.login(url)


if __name__ == '__main__':
    import asyncio

    auth = [('13530391013', '123456')]
    ws = 'ws://10.168.2.57:3000'
    url = 'https://guide.medlive.cn/guideline/30632'
    # auth = [('123456', '000000')]  # 账号密码
    # ws = 'ws://127.0.0.1:3000'  # 如使用浏览器 登录 传入浏览器地址
    med = MedLiveLogin(auth=auth, ws=ws)
    asyncio.run(med.login(url=url))
