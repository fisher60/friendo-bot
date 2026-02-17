import asyncio
import logging
from typing import TYPE_CHECKING

import arrow
import jwt

from bot import settings

if TYPE_CHECKING:
    import aiohttp


class LoginTokenLoggingFilter(logging.Filter):
    """Logging filter to remove api token from logging for friendo api requests."""

    def filter(self, record: logging.LogRecord) -> bool:
        """Returns False if login token is in logging record."""
        return "token" not in record.getMessage()


log = logging.getLogger(__name__)
log.addFilter(LoginTokenLoggingFilter())


class GraphQLClient:
    """Friendo GraphQL API wrapper."""

    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.token = None
        self.url = settings.FRIENDO_API_URL
        self.headers = None

        self.refresh_task: asyncio.Task = None

    async def close(self) -> None:
        """Close the aiohttp session."""
        await self.session.close()

    async def refresh_token(self) -> None:
        """Get a new token from the Friendo API."""
        query = (
            "mutation auth($username: String!, $password: String!){"
            "   login(data: { username: $username, password: $password }) {"
            "       token"
            "   }"
            "}"
        )
        variables = {
            "username": settings.FRIENDO_API_USER,
            "password": settings.FRIENDO_API_PASS,
        }
        resp = await self._post(json={"query": query, "variables": variables})
        self.token = resp["data"]["login"]["token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
        self.refresh_task = asyncio.create_task(self.refresh_later())

    async def refresh_later(self) -> None:
        """Wait until 2 days before token expires and get a new one."""
        exp = jwt.decode(self.token, options={"verify_signature": False})["exp"]
        seconds_to_exp = int(exp - arrow.utcnow().timestamp())
        sleep_time = seconds_to_exp - 60 * 60 * 24 * 2
        log.info("Will refresh token in %d seconds.", sleep_time)

        await asyncio.sleep(sleep_time)
        await self.refresh_token()

    async def request(self, **kwargs) -> dict:
        """
        Public wrapper for making a call to the GraphQL API.

        This ensures we have a token before calling.
        """
        if not self.token:
            await self.refresh_token()
        return await self._post(**kwargs)

    async def _post(self, **kwargs) -> dict:
        """Make a GraphQL API POST call."""
        async with self.session.post(self.url, headers=self.headers, **kwargs) as resp:
            resp_json = await resp.json()
            log.info("GraphQL response: %s", resp_json)
            return resp_json
