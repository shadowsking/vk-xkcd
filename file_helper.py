import os

import requests


def download_file(url: str, file_path: str, params: dict = None):
    response = requests.get(url, params=params)
    response.raise_for_status()

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(response.content)
