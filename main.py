import os
import shutil

from dotenv import load_dotenv

from vk_api import publish
from xkcd_api import download_random_comic


def main():
    load_dotenv()

    dir_name = "files"
    try:
        os.makedirs(dir_name, exist_ok=True)
        message, file_path = download_random_comic(dir_name)
        publish(
            file_path=file_path,
            message=message,
            group_id=os.environ["GROUP_ID"],
            access_token=os.environ["VK_API_TOKEN"],
            api_version=os.environ["VK_API_VERSION"],
        )
    finally:
        if os.path.isdir(dir_name):
            shutil.rmtree(dir_name)


if __name__ == "__main__":
    main()
