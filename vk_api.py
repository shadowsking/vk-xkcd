import requests


def get_wall_upload_server(group_id: str, access_token: str, api_version: str):
    response = requests.post(
        "https://api.vk.com/method/photos.getWallUploadServer",
        data={
            "group_id": group_id,
            "access_token": access_token,
            "v": api_version,
        },
    )
    response.raise_for_status()

    wall_upload_server = response.json()
    if wall_upload_server.get("error"):
        raise Exception(wall_upload_server["error"].get("error_msg"))

    return wall_upload_server["response"].get("upload_url")


def upload_photo(upload_url: str, file_path: str):
    with open(file_path, "rb") as f:
        response = requests.post(upload_url, files={"photo": f})
    response.raise_for_status()
    return response.json()


def save_wall_photo(
    group_id: str, access_token: str, api_version: str, uploaded_photo: dict
):
    payload = {
        "group_id": group_id,
        "access_token": access_token,
        "v": api_version,
    }
    payload.update(uploaded_photo)

    response = requests.post(
        "https://api.vk.com/method/photos.saveWallPhoto", data=payload
    )
    response.raise_for_status()
    return response.json()


def create_wall_post(
    group_id: str,
    access_token: str,
    api_version: str,
    attachments: str,
    message: str = None,
    from_group: int = 1,
):
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
    return response.json()


def publish(
    file_path: str,
    group_id: str,
    access_token: str,
    api_version: str,
    message: str = None,
):
    upload_url = get_wall_upload_server(group_id, access_token, api_version)
    uploaded_photo = upload_photo(upload_url, file_path)
    saved_photos = save_wall_photo(group_id, access_token, api_version, uploaded_photo)

    for photo in saved_photos.get("response"):
        create_wall_post(
            group_id,
            access_token,
            api_version,
            attachments="photo{owner_id}_{id}".format(**photo),
            message=message,
        )
