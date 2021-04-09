import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple

from aiohttp import ClientResponse
from discord import Color, Embed, Member, RawReactionActionEvent, Reaction
from discord.ext.commands import Cog, Context, group

from bot import settings
from bot.bot import Bot, Friendo

log = logging.getLogger(__name__)


class QueryError(Exception):
    """Error containing all query errors."""

    errors: Tuple[Any]

    def __init__(self, *errors, **kwargs):
        self.errors = errors


@dataclass
class DogeBoardData:
    """Dataclass to hold the data retrieved from the API."""

    guild_id: int
    channel_id: int
    emoji: str
    reactions_required: int


class DogeBoard(Cog):
    """Starboard Copy."""""

    def __init__(self, bot: Friendo) -> None:
        self.bot = bot
        self._cache: Dict[int, DogeBoardData] = {}
        self._token: Optional[str] = None
        self._url = settings.FRIENDO_API_URL

    @property
    def headers(self) -> Dict[str, str]:
        """Get headers used in API calls."""
        if self._token:
            return {"Authorization": f"Bearer {self._token}"}

    @staticmethod
    async def _handle_request(resp: ClientResponse) -> Dict[str, Any]:
        """Handle the request errors and status codes."""
        if resp.status != 200:
            raise ConnectionError(f"Error: {resp.status} | Cannot connect to GraphQL Database")

        data = await resp.json()
        if errors := data.get("errors"):
            raise QueryError([error["message"] for error in errors])
        return data

    async def _login(self) -> None:
        """Login to the GraphQL database and store the token."""
        query = """mutation {
          login(data: { username: "%s", password: "%s" }) {
            token
          }
        }
        """ % (settings.FRIENDO_API_USER, settings.FRIENDO_API_PASS)

        async with self.bot.session.post(self._url, json={"query": query}) as resp:
            data = await self._handle_request(resp)
            try:
                self._token = data["data"]["login"]["token"]
            except QueryError as e:
                log.error(f"Couldn't login: {e}")

    async def _get_guild_data(self, guild_id: int) -> DogeBoardData:
        """
        Attempt to get the dogeboard_data from cache using guild_id.

        if the data is not in the cache, it will request it from the GraphQL DB.
        if the data doesn't exist in the database it will be created and send to GraphQL DB
        """
        if dogeboard_data := self._cache.get(guild_id):
            return dogeboard_data
        elif dogeboard_data := await self._fetch_guild_data(guild_id):
            return dogeboard_data
        else:
            return await self._create_new_dogeboard(guild_id)

    async def _fetch_guild_data(self, guild_id: int) -> Optional[DogeBoardData]:
        """Attempt to fetch guild data from the GraphQL database."""
        query = """mutation {
            server(data: { server_id: "%d", }) {
                dogeboard_id
                dogeboard_emoji
                dogeboard_reactions_required
              }
            }
           """ % guild_id

        async with self.bot.session.post(self._url, json={"query": query}, headers=self.headers) as resp:
            try:
                data = await self._handle_request(resp)
                dogeboard_data = DogeBoardData(**data)
                self._cache[guild_id] = dogeboard_data
                return dogeboard_data
            except QueryError as e:
                log.error(f"Query Errors: {e}")

    async def _create_new_dogeboard(self, guild_id: int) -> DogeBoardData:
        """Create a new guild DogeBoard, this is sent to the GraphQL DB."""
        query = """mutation {
            server(data: { server_id: "%d", }) {
                dogeboard_id
                dogeboard_emoji
                dogeboard_reactions_required
              }
            }
           """ % guild_id

        async with self.bot.session.post(self._url, json={"query": query}, headers=self.headers) as resp:
            try:
                data = await self._handle_request(resp)
                return DogeBoardData(**data)
            except QueryError as e:
                log.error(f"Query Errors: {e}")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        """Handle event when users add reactions."""
        if self._token is None:
            await self._login()

        # dogeboard_data = await self._get_guild_data(payload.guild_id)
        # emoji = payload.emoji

    @group(brief="Collate the best message of the server using reactions")
    async def dogeboard(self, ctx: Context) -> None:
        """Command group for DogeBoard."""
        if not ctx.subcommand_passed:
            embed = Embed(title="DogeBoard", description="commands", color=Color.orange())
            embed.add_field(name="emoji", value="Set the emoji used for the DogeBoard")
            embed.add_field(name="channel", value="Set the DogeBoard channel")
            embed.add_field(name="required", value="Set the reactions required for the DogeBoard")
            await ctx.send(embed=embed)

    @dogeboard.command(brief="Set the emoji used for the DogeBoard, Custom Emojis Only")
    async def emoji(self, ctx: Context) -> None:
        """Set the emoji used for the DogeBoard."""
        reaction_msg = await ctx.send(content="> React with the new emoji")

        def check(reaction: Reaction, member: Member) -> bool:
            return member == ctx.author and reaction_msg == reaction.message

        try:
            reaction, member = await self.bot.wait_for("reaction_add", check=check, timeout=5)
        except asyncio.TimeoutError:
            return await reaction_msg.edit(content="> You didn't react, Canceling emoji change.")
        finally:
            await reaction_msg.delete(delay=5)

    @dogeboard.command(brief="Set the reactions required for the DogeBoard")
    async def required(self, ctx: Context, amount: int) -> None:
        """Set the amount of required emojis to trigger the DogeBoard."""
        await ctx.send(str(amount))


def setup(bot: Bot) -> None:
    """Adding the help cog."""
    if not settings.FRIENDO_API_USER:
        raise EnvironmentError("Missing environment variable: FRIENDO_API_USER")
    if not settings.FRIENDO_API_PASS:
        raise EnvironmentError("Missing environment variable: FRIENDO_API_PASS")

    bot.add_cog(DogeBoard(bot))
