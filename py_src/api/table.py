import random
from dataclasses import asdict
from typing import Any, Dict, List

from flask import jsonify, send_from_directory, Blueprint

from py_src.test.mock.extern_api_mock import ServiceMock
from py_src.types import Response, MaterialDB, Segmentation, MaterialFile
from py_src.utils.common import *
from .utils import parse_tags
from py_src.db import table
# from py_src.tools.pexels_func import get_pexels_query
# from py_src.tools.generate import run
# from py_src.tools.tencent_cdn import upload_cdn_ai_image, tencent_list_files

import time

from py_src.config import CDN_URL, public_path


def resort_all(datas: List[dict]):
    for i, data in enumerate(datas):
        id = data["id"]
        table.db.updateById(id, {
            "index": i + 1
        })


def init_table_api(api_group: Blueprint, service: ServiceMock):
    api_table_group = Blueprint('api_table_group', __name__,
                                url_prefix='/table')

    @api_table_group.get('/')
    def get_table():
        # req_data = request.get_json()
        req_data = request.args
        page = int(req_data.get("page", 0))
        per_page = int(req_data.get("perPage", 20))
        print(req_data)
        raw_data = table.getSortedAll()
        page_raw_data = raw_data[(page - 1) * per_page:page * per_page]
        # img_materials = [ImgMaterial(**x) for x in page_raw_data]
        for x in page_raw_data:
            x["id"] = str(x["id"])
            # try:
            #     x["tags"] = ", ".join(x["tags"])
            # except Exception as e:
            #     print(e)
            #     x["tags"] = x["tags"][0]
            x["tags2"] = ", ".join(x["tags2"]) if x["tags2"] else ""
            # x["images"] = []
            # x["style"] = video_style()
        data = {
            "data": {
                "count": len(raw_data),
                "rows": page_raw_data
            }
        }
        # print(page_raw_data)
        return jsonify(data)
        # return jsonify(Response(0, "ok", {}))


