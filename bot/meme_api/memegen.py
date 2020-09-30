"""Pulls meme templates from imgfip api and creates memes"""
import requests
import json
from bot.settings import BASE_DIR, MEME_USERNAME, MEME_PASSWORD


class Meme:
    meme_dir = f"{BASE_DIR}/meme_api/json/meme_list.json"
    updated = False

    def __init__(self):
        self.gen_meme_url = "https://api.imgflip.com/caption_image"
        self.get_memes_url = "https://api.imgflip.com/get_memes"

        if not self.updated:
            self.get_all_memes()
            self.updated = True

        with open(self.meme_dir, "r") as m:
            self.meme_dict = json.load(m)["data"]["memes"]

        self.user_name = MEME_USERNAME
        self.password = MEME_PASSWORD

    def generate_meme(self, *, name, text=None):
        """Creates a meme given the name of a template."""
        data = {"username": self.user_name, "password": self.password}

        if text is not None:

            for meme in self.meme_dict:
                if meme["name"].lower() == name.lower():
                    data["template_id"] = meme["id"]

                    if len(text) <= meme["box_count"]:
                        for count, each in enumerate(text):
                            data[f"boxes[{count}][text]"] = each
                    else:
                        return f"Too many text boxes for {meme['name']} with count {meme['box_count']}"

        resp = requests.post(url=self.gen_meme_url, data=data).json()

        if resp["success"]:
            return resp["data"]["url"]
        return None

    def get_all_memes(self):
        """Gets the names of all available meme templates."""
        resp = requests.get(url=self.get_memes_url)
        resp = resp.json()

        if resp["success"]:
            print("updating meme list...")

            with open(self.meme_dir, "w+") as f:
                json.dump(resp, f)
        else:
            print("Failed to update, aborting...")

    def search_meme_list(self, search_words: list):
        """Checks if the input search_words matches any available meme templates."""
        final_dict = {}

        for meme in self.meme_dict:
            name = meme["name"]
            for each in meme["name"].split(" "):
                if any(word in each.lower() for word in search_words):
                    final_dict[name] = meme["box_count"]

        if len(final_dict) > 0:
            return "\n".join(
                [f"Name: {x}, Text Boxes: {final_dict[x]}" for x in final_dict.keys()][
                    :10
                ]
            )
        return None
