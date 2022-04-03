import inspect
import pkgutil
from typing import Iterator, NoReturn

from disnake import AllowedMentions, Intents

from . import settings
from bot.bot import Friendo
from bot import cogs


def _get_cogs() -> Iterator[str]:
    """
    Return an iterator going through each cog.

    On each iteration the cog is check for having a setup function raising a more readable error if not found.
    """

    def on_error(name: str) -> NoReturn:
        raise ImportError(name=name)

    for module in pkgutil.walk_packages(cogs.__path__, f"{cogs.__name__}.", onerror=on_error):
        if module.ispkg:
            _import = __import__(module.name)
            if not inspect.isfunction(getattr(_import, "setup", None)):
                continue

        yield module.name


if __name__ == "__main__":
    bot = Friendo(
        command_prefix=settings.COMMAND_PREFIX, help_command=None, intents=Intents.all(),
        allowed_mentions=AllowedMentions(everyone=False),
    )

    for cog in _get_cogs():
        bot.load_extension(cog)

    bot.run(settings.TOKEN)
