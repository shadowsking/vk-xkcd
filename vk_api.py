import requests


class VKApiError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return "Error code [{error_code}]: {error_msg}".format(**self.error)


def get_upload_url(group_id: str, access_token: str, api_version: str) -> str:
    response = requests.post(
        "https://api.vk.com/method/photos.getWallUploadServer",
        data={
            "group_id": group_id,
            "access_token": access_token,
            "v": api_version,
        },
    )
    response.raise_for_status()

    uploaded = response.json()
    if uploaded.get("error"):
        raise VKApiError(uploaded.get("error"))

    return uploaded["response"].get("upload_url")


def upload_photo(upload_url: str, file_path: str) -> dict:
    with open(file_path, "rb") as f:
        response = requests.post(upload_url, files={"photo": f})
    response.raise_for_status()
    return response.json()


def save_wall_photo(
    group_id: str, access_token: str, api_version: str, uploaded_photo: dict
) -> dict:
    payload = {
        "group_id": group_id,
        "access_token": access_token,
        "v": api_version,
        "server": uploaded_photo["server"],
        "hash": uploaded_photo["hash"],
        "photo": uploaded_photo["photo"],
    }

    response = requests.post(
        "https://api.vk.com/method/photos.saveWallPhoto", data=payload
    )
    response.raise_for_status()
    saved_photos = response.json()
    if saved_photos.get("error"):
        raise VKApiError(saved_photos.get("error"))

    return saved_photos


def create_wall_post(
    group_id: str,
    access_token: str,
    api_version: str,
    attachments: str,
    message: str = None,
    from_group: int = 1,
) -> dict:
    response = requests.post(
        "https://api.vk.com/method/wall.post",
        data={
            "owner_id": "-{group_id}".format(group_id=group_id),
            "attachments": attachments,
            "access_token": access_token,
            "v": api_version,
            "from_group": from_group,
            "message": message,
        },
    )
    response.raise_for_status()
    posted = response.json()
    if posted.get("error"):
        raise VKApiError(posted.get("error"))

    return posted


def publish(
    file_path: str,
    group_id: str,
    access_token: str,
    api_version: str,
    message: str = None,
):
    upload_url = get_upload_url(group_id, access_token, api_version)
    uploaded_photo = upload_photo(upload_url, file_path)
    saved_photos = save_wall_photo(group_id, access_token, api_version, uploaded_photo)
    create_wall_post(
        group_id,
        access_token,
        api_version,
        attachments="photo{owner_id}_{id}".format(**saved_photos.get("response")[0]),
        message=message,
    )
