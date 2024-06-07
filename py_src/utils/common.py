import base64
from io import BufferedReader
from typing import BinaryIO, Union
from urllib.parse import urlparse

import json5
import os
from flask import request
from werkzeug.datastructures import FileStorage
# from ..config import *
from py_src.config import site_json_path, db_path, image_path
# from py_src.tools.tencent_cdn import upload_user_image

# project_path = Path(__file__).parent.parent.parent
# print("Main path", project_path)
# image_path = project_path / "db/image"
# public_path = project_path / "public"
# db_path = project_path / "db"
# db_bak_path = db_path / "db_bak"
# pages_gen_path = project_path / "pages/gen"
# pages_path = project_path / "pages"
# site_json_path = project_path / "pages/site.json5"
# site_prod_json_path = project_path / "pages/site.prod.json5"
#
#
# load_dotenv(project_path / ".env")
# # load_dotenv(project_path / ".env.development")
# ENVIRONMENT = os.getenv("ENVIRONMENT", "prod")
# IS_DEV = ENVIRONMENT == "dev"

IMAGE_SUFFIX = ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp"]
VIDEO_SUFFIX = ["mp4", "mkv", "flv", "avi", "mov", "wmv", "3gp"]


def init():
    os.makedirs(db_path, exist_ok=True)
    os.makedirs(image_path, exist_ok=True)

# def is_env_dev():
#     return ENVIRONMENT == "dev"
# # def get_host():


def get_enable_types():
    return ", ".join(["." + x for x in
                      [*IMAGE_SUFFIX, *VIDEO_SUFFIX]])


def get_material_type(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    file_extension = file_extension[1:]
    if file_extension in IMAGE_SUFFIX:
        return "image"
    elif file_extension in VIDEO_SUFFIX:
        return "video"
    else:
        return None


def get_video_poster(video_path):
    return str(video_path) + ".jpg"


def extract_video_poster(video_path):
    import cv2
    video_path = str(video_path)
    print("extract_video_poster", video_path)
    video_capture = cv2.VideoCapture(video_path)  # 替换成你的视频文件路径
    # 检查视频是否成功打开
    if not video_capture.isOpened():
        print("无法打开视频文件")
        return False
    # 读取第一帧
    success, first_frame = video_capture.read()
    # 关闭视频文件
    video_capture.release()
    # 检查是否成功读取第一帧
    if success:
        # 保存第一帧为图像文件
        output_path = get_video_poster(video_path)
        cv2.imwrite(output_path, first_frame)
        print("第一帧已保存为 ", output_path)
        return True
    else:
        print("无法读取第一帧")
    return False


def save_extern_file(origin_file: Union[FileStorage, BinaryIO, str]):
    extern_path = None

    if isinstance(origin_file, FileStorage):
        extern_path = origin_file.filename
    elif isinstance(origin_file, BufferedReader):
        extern_path = origin_file.name
    elif isinstance(origin_file, str):
        extern_path = origin_file
        origin_file = open(extern_path, "rb")
    else:
        raise Exception("save_extern_file: origin_file type error", type(origin_file))
    print("save_extern_file", extern_path)
    # extern_path = origin_file.filename
    file_name = os.path.basename(extern_path)
    # file_name = upload_user_image(origin_file, file_name)
    # output = str(image_path / file_name)
    # with open(output, "wb") as f:
    #     f.write(origin_file.read())

    # m_type = get_material_type(output)
    # TODO: 这里设置一下视频如何处理
    # if m_type == "video":
    #     extract_video_poster(output)
    return file_name


def get_user_id():
    user_id = request.cookies.get('user_id', "test")
    return user_id


def save_base64_file(file_base64: str, output_name: str):
    base64_bytes = file_base64.split(',')[1].encode('utf-8')
    decoded_data = base64.b64decode(base64_bytes)
    file_extension = file_base64.split(';')[0].split('/')[-1]
    file_name = f"{output_name}.{file_extension}"
    with open(image_path / file_name, 'wb') as f:
        f.write(decoded_data)
        print("video_make_cover add:", file_name)
        return os.path.abspath(f.name)


def get_site_pages():
    site_pages = {}
    with open(site_json_path, "r", encoding="utf8") as f:
        data = json5.loads(f.read())
        pages = data["data"]["pages"][0]["children"]
        for x in pages:
            name = x["url"]
            if not name.startswith("/"):
                name = "/" + name
            if name.endswith("/"):
                name = name[:-1]
            site_pages[name] = x
    return site_pages


def get_api_host():
    # API_HOST = os.getenv("API_HOST")
    API_HOST = None
    if API_HOST is None:
        o = urlparse(request.base_url)
        API_HOST = f"{o.scheme}://{o.netloc}"
    return API_HOST

def get_file_type(filename):
    res = get_material_type(filename)
    if res is None:
        return "unknown"  # 如果不是图片或视频，返回未知
    return res
