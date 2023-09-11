import os
from random import randint
from typing import Tuple

import requests


def fetch_random_comic() -> dict:
    latest_comic_response = requests.get("https://xkcd.com/info.0.json")
    latest_comic_response.raise_for_status()
    latest_comic = latest_comic_response.json()

    random_comic_id = randint(1, latest_comic.get("num"))
    response = requests.get("https://xkcd.com/{}/info.0.json".format(random_comic_id))
    response.raise_for_status()
    return response.json()


def download_random_comic(dir_name: str) -> Tuple[str, str]:
    random_comic = fetch_random_comic()
    url = random_comic.get("img")
    file_path = os.path.join(dir_name, os.path.basename(url))

    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, "wb") as f:
        f.write(response.content)

    return random_comic.get("alt"), file_path
