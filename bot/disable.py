import argparse
import logging

logger = logging.getLogger(__name__)
parser = argparse.ArgumentParser()

# no-api argument can be used to disable api cogs ie. events and memes currently
parser.add_argument("--no-api", help="disable api cogs in the bot", action="store_true")
# enable argument can be used to enable certain cogs and disable all others
parser.add_argument("--enable", help="enable certain cogs in the bot", default=[], nargs="+")
# disable argument can be used to disable certain cogs and enable all others
parser.add_argument("--disable", help="disable certain cogs in the bot", default=[], nargs="+")


class DisableApi:
    """Checks the abilities of an API."""

    def __init__(self) -> None:
        self.args = parser.parse_args()
        # Both enable and disable arguments can be passed
        if self.args.enable and self.args.disable:
            msg = "Cannot pass both enable and disable"
            raise ValueError(msg)

    def get_no_api(self) -> bool:
        """Sees if there's an API at all."""
        return self.args.no_api

    def get_enable(self) -> bool:
        """Is the API enabled?"""
        return self.args.enable

    def get_disable(self) -> bool:
        """Is the API disabled?"""
        return self.args.disable


if __name__ == "__main__":
    api_disabler = DisableApi()
    logger.info(api_disabler.get_no_api())
    logger.info(api_disabler.get_enable())
    logger.info(api_disabler.get_disable())
