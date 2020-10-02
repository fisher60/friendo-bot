import json

from bot.settings import BASE_DIR, MEME_PASSWORD, MEME_USERNAME

MEME_DIR = f"{BASE_DIR}/meme_api/json/meme_list.json"


class Meme:
    """Pulls meme templates from imgfip api and creates memes."""

    def __init__(self, bot):
        self.bot = bot

        self.gen_meme_url = "https://api.imgflip.com/caption_image"
        self.get_all_memes_url = "https://api.imgflip.com/get_memes"

        self.bot.loop.run_until_complete(self.get_all_memes())

        with open(MEME_DIR, "r") as m:
            self.meme_dict = json.load(m)["data"]["memes"]

        self.user_name = MEME_USERNAME
        self.password = MEME_PASSWORD

    async def generate_meme(self, *, name, text=None):
        """Creates a meme given the name of a template."""
        data = {"username": self.user_name, "password": self.password}

        if text:

            for meme in self.meme_dict:
                if meme["name"].lower() == name.lower():
                    data["template_id"] = meme["id"]

                    if len(text) <= meme["box_count"]:
                        for count, each in enumerate(text):
                            data[f"boxes[{count}][text]"] = each
                    else:
                        return f"Too many text boxes for {meme['name']} with count {meme['box_count']}"

        async with self.bot.session.post(self.gen_meme_url, data=data) as resp:
            if resp.status == 200:
                _json = await resp.json()
                return _json["data"]["url"]

    async def get_all_memes(self):
        """Gets the names of all available meme templates."""
        async with self.bot.session.get(self.get_all_memes_url) as resp:
            if resp.status == 200:
                print("updating meme list...")

                _json = await resp.json()

                with open(MEME_DIR, "w+") as f:
                    json.dump(_json, f)
            else:
                print("Failed to update meme list, aborting...")

    def search_meme_list(self, search_words: list):
        """Checks if the input search_words matches any available meme templates."""
        final_dict = {}

        for meme in self.meme_dict:
            name = meme["name"]
            for each in meme["name"].split(" "):

                # Check if any word in he search words matches in a meme name, lazy search
                if any(word in each.lower() for word in search_words):
                    final_dict[name] = meme["box_count"]

        if len(final_dict) > 0:
            return "\n".join(
                [f"Name: {x}, Text Boxes: {final_dict[x]}" for x in final_dict.keys()][
                    :10
                ]
            )
