import os
import shutil

from dotenv import load_dotenv

from vk_api import publish
from xkcd_api import download_comics


def main():
    load_dotenv()

    comics, file_path = download_comics()
    publish(
        file_path=file_path,
        message=comics.get("alt"),
        group_id=os.getenv("GROUP_ID"),
        access_token=os.getenv("VK_API_TOKEN"),
        api_version=os.getenv("VK_API_VERSION"),
    )

    dir_path = os.path.dirname(file_path)
    if os.path.isdir(dir_path):
        shutil.rmtree(dir_path)


if __name__ == "__main__":
    main()
