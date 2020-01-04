# -*- coding: utf-8 -*-
# @Time    : 2020/1/4 下午2:21
# @Author  : Wang Junling
# @File    : RefreshToken.py
# @Software: PyCharm
import json
import asyncio
from aiohttp import ClientSession


class Refersh:
    '''
    目前主要用来请求用户信息和延长ｔｏｋｅｎ的有效时间
    '''

    def __init__(self, url: str = r"https://open.douyin.com/", client_key: str = "awus2ha9snrpmf7c"):
        self.url = url
        self.client_key = client_key
        self.return_data = {
            'msg': 'success', 'data': None
        }

    async def asyn_request(self, url):
        Request_Record = 0
        async with ClientSession() as session:
            while Request_Record < 5:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.read()
            Request_Record += 1
        return response.read()

    async def get_newToken(self, refresh_token: str, Resources: str = 'oauth/refresh_token/') -> json:
        """
        用来刷新token的接口，
        :param refresh_token:授权之后会有这个字段，主要用来延长token的有效时间
        :param Resources:请求的资源
        :return: {
            'access_token': '', 不会改变
            'captcha': '',
            'description': '',
            'error_code': 0,
            'expires_in': 1296000,有效期15天
            'open_id': '...',
            'refresh_token': '...',
            'scope': '...'}
        """
        params = f"?refresh_token={refresh_token}&client_key={self.client_key}&grant_type=refresh_token"
        url = self.url + Resources + params
        response_text = await self.asyn_request(url)

        try:
            data = json.loads(response_text)
            self.return_data['data'] = data.get('data')
        except Exception as err:
            self.return_data['msg'] = '返回数据不正确：json解析错误'
            self.return_data['data'] = response_text
            self.return_data['err'] = err
            return self.return_data

        return self.return_data

    async def get_user(self, access_token: str, open_id: str, Resources: str = '/oauth/userinfo/') -> json:
        """
        用来获取用户基本信息
        :param access_token:
        :param open_id:
        :param Resources:
        :return:
        """
        params = f"?access_token={access_token}&open_id={open_id}"
        url = self.url + Resources + params
        response_text = await self.asyn_request(url)

        try:
            data = json.loads(response_text)
            self.return_data['data'] = data.get('data')
        except Exception as err:
            self.return_data['msg'] = '返回数据不正确：json解析错误'
            self.return_data['data'] = response_text
            self.return_data['err'] = err
            return self.return_data
        return self.return_data


if __name__ == '__main__':
    "测试用例"
    import time

    a = time.time()
    run = Refersh()
    tasks = []  # 任务队列
    loop = asyncio.get_event_loop()
    for i in range(5):
        task = asyncio.ensure_future(
            # run.get_newToken(refresh_token='rft.a859cc0fe735c47993589de2c1e6074592BieSnESErUzfYERjqEfKG7hpAW')
            run.get_user(access_token='act.2b75374a6f740ad4e34b2b01af9fa1e3pLhNT5fyVYR1ch8I1WPtCxfPULzn',
                         open_id='78736b39-6a0f-4599-b2e8-eb166c9611cb')
        )
        tasks.append(task)
    result = loop.run_until_complete(asyncio.gather(*tasks))
    print(result)
    print(time.time() - a)
