import urllib.parse

import aiohttp

from asynctradier.exceptions import BadRequestException


class WebUtil:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token

    async def make_request(
        self, url: str, method: str, params: dict = None, data: dict = None
    ):
        async with aiohttp.ClientSession() as session:
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            async with session.request(
                method, url, params=params, headers=headers, data=data
            ) as resp:
                if resp.status != 200:
                    raise BadRequestException(resp.status, await resp.text())
                response = await resp.json()

                if "errors" in response:
                    raise BadRequestException(
                        400, response["errors"]["error"]["description"]
                    )
                return response

    async def get(self, path: str, params: dict = None):
        url = urllib.parse.urljoin(self.base_url, path)
        return await self.make_request(url, "GET", params=params)

    async def post(self, path: str, data: dict = None):
        url = urllib.parse.urljoin(self.base_url, path)
        return await self.make_request(url, "POST", data=data)

    async def delete(self, path: str):
        url = urllib.parse.urljoin(self.base_url, path)
        return await self.make_request(url, "DELETE")

    async def put(self, path: str, data: dict = None):
        url = urllib.parse.urljoin(self.base_url, path)
        return await self.make_request(url, "PUT", data=data)
