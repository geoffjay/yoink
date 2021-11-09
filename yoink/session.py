import asyncio
import logging
import os

from pyppeteer import launch
from pyppeteer.errors import TimeoutError

from yoink import is_true

log = logging.getLogger(__name__)


class Session:
    def __init__(self):
        self.headless = is_true(os.getenv("HEADLESS", "true"))

    def __del__(self):
        asyncio.shield(self.tear_down())

    async def __ainit__(self):
        await self.setup()

    async def setup(self):
        self.browser = await launch(
            {
                "headless": self.headless,
                "args": [
                    "--no-sandbox",
                    "--incognito",
                ],
                "autoClose": False,
            },
        )
        self.page = await self.browser.newPage()

    async def tear_down(self):
        if self.page:
            await asyncio.wait([self.page.close()])
        await self.browser.close()

    async def execute(self, callback):
        try:
            asyncio.run(callback)
        except TimeoutError as e:
            log.error(e)


async def create_session():
    session = Session()
    await session.__ainit__()
    return session
