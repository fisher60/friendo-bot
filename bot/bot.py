import logging
from typing import Union

import aiohttp
import discord
from discord.ext.commands import Bot, CommandError, Context

from bot.disable import DisableApi
from bot.graphql import GraphQLClient
from bot.settings import API_COGS

log = logging.getLogger(__name__)


class Friendo(Bot):
    """Base Class for the discord bot."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        connector: aiohttp.TCPConnector,
        resolver: aiohttp.AsyncResolver,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)

        # Client.login() will call HTTPClient.static_login() which will create a session using
        # this connector attribute.
        self.http.connector = connector

        self.session = session
        self._connector = connector
        self._resolver = resolver
        self.graphql = GraphQLClient(session=session)

    async def setup_hook(self) -> None:
        """Assign an error handler for Interaction commands."""
        self.tree.on_error = self.on_command_error

    async def on_ready(self) -> None:
        """Runs when the bot is connected. Sync Interaction/app_commands when connected to the gateway."""
        log.info('Awaiting...')
        log.info("Bot Is Ready For Commands")
        await self.tree.sync()

    async def on_command_error(
            self,
            ctx: Union[Context, discord.Interaction],
            exception: Union[CommandError, discord.app_commands.AppCommandError]
    ) -> None:
        """Fired when exception happens."""
        log.error(
            "Exception happened while executing command",
            exc_info=(type(exception), exception, exception.__traceback__)
        )

    async def close(self) -> None:
        """Make sure connections are closed properly."""
        await super().close()

        if self.graphql:
            await self.graphql.close()

        if self.session:
            await self.session.close()

        if self._connector:
            await self._connector.close()

        if self._resolver:
            await self._resolver.close()

    async def load_extension(self, name: str) -> None:
        """Loads an extension after checking if it's disabled or not."""
        disable_api = DisableApi()
        cog_name = name.split(".")[-1]

        # If no-api is passed disable API_COGS ie. memes and events
        if disable_api.get_no_api() and cog_name in API_COGS:
            return

        disabled_list = disable_api.get_disable()

        if disabled_list:
            if cog_name in disabled_list:
                return

            # If cog is not disabled, load it
            else:
                await super().load_extension(name)
                return

        enabled_list = disable_api.get_enable()

        if enabled_list:
            # If cog is enabled, load it
            if cog_name in enabled_list:
                await super().load_extension(name)
                return

            # Don't load cogs not passed along with enable
            else:
                return

        # load cogs if no argument is passed
        await super().load_extension(name)
