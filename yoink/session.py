import asyncio
import logging
import os

from pyppeteer import launch
from requests.sessions import RequestsCookieJar

from yoink import is_true

logger = logging.getLogger("uvicorn.error")


class Session:
    def __init__(self):
        self.headless = is_true(os.getenv("HEADLESS", "true"))

    def __del__(self):
        asyncio.shield(self.tear_down())

    async def __ainit__(self):
        await self.setup()

    def _get_cookie_value(self, name):
        for cookie in self.cookies:
            if cookie.get("name") == name:
                return cookie["value"]
        return None

    @property
    def cookies(self):
        return self._cookies

    @property
    def cookie_jar(self):
        jar = RequestsCookieJar()
        for cookie in self.cookies:
            jar.set(
                cookie.get("name"),
                cookie.get("value"),
                domain=cookie.get("domain"),
                path=cookie.get("path"),
            )

    @property
    def headers(self):
        return self._headers
        # return {
        #     "XSRF-TOKEN": self._get_cookie_value("XSRF-TOKEN"),
        #     "_session_id": self._get_cookie_value("_session_id"),
        #     "ajs_anonymous_id": self._get_cookie_value("ajs_anonymous_id"),
        # }

    async def setup(self):
        logger.debug("Performing session setup")
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
        logger.debug("Performing session shutdown")
        if self.page:
            await asyncio.wait([self.page.close()])
        await self.browser.close()

    async def login(self, email, password):
        logger.debug("Performing session login")
        logger.debug(f"Login with {email}:{password}")
        await self.page.goto(f"http://app.myclio.ca:3000")
        await self.page.waitForXPath("//main[@class='ui-main']")
        await self.page.waitForXPath("//input[@type='email']")
        await self.page.type("input[type='email']", email)
        await self.page.click("input[type='submit']")
        await self.page.waitForXPath("//main[@class='ui-main']")
        await self.page.waitForXPath("//input[@type='password']")
        await self.page.type("input[type='password']", password)
        await self.page.click("input[type='submit']")
        await self.page.waitForXPath("/html[@ng-app='ApolloApp']")
        response = await self.page.goto(f"http://app.myclio.ca:3000")
        self._cookies = await self.page.cookies()
        self._headers = response.headers if response else {}

    async def who_am_i(self):
        response = await self.page.goto(
            f"http://app.myclio.ca:3000/api/v4/users/who_am_i",
            {"waitUntil": "domcontentloaded"},
        )
        return response

    async def execute(self, *args):
        logger.debug("Executing session")
        tasks = [asyncio.ensure_future(self.login(*args))]
        await asyncio.gather(*tasks)
        # try:
        #     loop.run_until_complete(self.login())
        # except asyncio.CancelledError as e:
        #     logger.error(e)
        # except TimeoutError as e:
        #     logger.error(e)
        # finally:
        #     loop.run_until_complete(loop.shutdown_asyncgens())
        #     loop.close()


async def create_session():
    session = Session()
    await session.__ainit__()
    return session
