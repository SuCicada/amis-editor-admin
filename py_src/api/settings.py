from flask import jsonify, Blueprint

from py_src.config import db_bak_path
from py_src.db import table
from py_src.types import *
from py_src.utils.common import *


def get_unused_images():
    used_images = []
    datas = table.getSortedAll()
    for data in datas:
        data = MaterialDB.from_dict(data)
        images = data.images
        if images is None:
            continue
        for image in images.values():
            used_images.append(image.path)
        if data.upload_image:

            used_images.append(data.upload_image)
            type = get_material_type(data.upload_image)
            if type == "video":
                used_images.append(get_video_poster(data.upload_image))

    unused_images = []
    for image in os.listdir(image_path):
        if image not in used_images:
            unused_images.append(image)

    return unused_images


def init_settings_api(api_group: Blueprint):
    api_group_settings = Blueprint('settings', __name__,
                                   url_prefix='/settings')

    @api_group_settings.get("/")
    def get_settings():
        unused_images = get_unused_images()

        db_files = os.listdir(db_bak_path)
        db_files = [x for x in db_files if
                    x.endswith(".json") and
                    # x.startswith("db.") and
                    x != "db.json"]
        old_db_num = len(db_files)

        return jsonify(Response(0, "ok", {
            "unused_images_num": len(unused_images),
            "old_db_num": old_db_num
        }))

    @api_group_settings.post("/clean_unused_images")
    def clean_unused_images():
        unused_images = get_unused_images()
        for image in unused_images:
            image = image_path / image
            print("remove", image)
            os.remove(image)
        return jsonify(Response(0, "ok", {}))

    # ${API_HOST}/api/settings/file_type
    @api_group_settings.get("/file_type")
    def get_file_type():
        return jsonify(Response(0, "ok", {
            "image": IMAGE_SUFFIX,
            "video": VIDEO_SUFFIX
        }))

    api_group.register_blueprint(api_group_settings)
