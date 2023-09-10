import os
from random import randint

import requests

import file_helper


def fetch_random_comics():
    latest_comics_response = requests.get("https://xkcd.com/info.0.json")
    latest_comics_response.raise_for_status()
    latest_comics = latest_comics_response.json()

    random_comics_id = randint(1, latest_comics.get("num"))
    response = requests.get("https://xkcd.com/{}/info.0.json".format(random_comics_id))
    response.raise_for_status()
    return response.json()


def download_comics():
    random_comics = fetch_random_comics()
    url = random_comics.get("img")
    file_path = os.path.join("files", os.path.basename(url))
    file_helper.download_file(url, file_path)
    return random_comics, file_path
