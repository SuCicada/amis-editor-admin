import os
import sys
from dataclasses import asdict
from pathlib import Path

import pysondb

sys.path.append(str(Path(__file__).parent.parent.parent))
from py_src.db import video_make_cover, images_db
from py_src.db.images_db import ImageDB

# print(sys.path)
from py_src.api.video_make import init_video_make_data
from py_src.server_api import service
from py_src.utils.common import *


# extract_video_poster("/Users/peng/PROGRAM/GitHub/amis-admin/db/image/[Reaktor] Serial Experiments Lain - E12 [1080p][x265][10-bit][Dual-Audio]-cut-merged-1687536837080.mp4")
def insert_image():
    # video_make_cover.db.deleteAll()
    # init_video_make_data(service
    # )
    images_db.db.add(asdict(ImageDB(
        type="网络图片",
        style="widget 风格",
        is_from_ai=True,
        ai_tags={"model": "AW Portrait", "width": 100},
        content_tags=["房子", "锁", "电话"],
        meaning_tags=["债券", "资金", "资产"],
        is_from_user=False,
        use_count=3,
        deleted=False,
        vector="vvvv.vvv",
        path="/image/08a95550065b815311a8c2656db7e7a2.jpg"
    )))
    images_db.db.add(asdict(ImageDB(
        type="漫画图片",
        style="漫画风格",
        is_from_ai=False,
        ai_tags={"model": "AW Painting", "width": 100},
        content_tags=["老公", "老婆", "小三", "开门"],
        meaning_tags=["回家", "出轨"],
        is_from_user=True,
        use_count=3,
        deleted=False,
        vector="vvvv.vvv",
        path="/image/100831957231418270_0_1699255839..jpg"
    )))
    images_db.db.add(asdict(ImageDB(
        type="漫画图片",
        style="真人风格",
        is_from_ai=False,
        ai_tags={"model": "AW Painting", "width": 100},
        content_tags=["打电话", "馅饼", "男人"],
        meaning_tags=["诈骗"],
        is_from_user=True,
        use_count=0,
        deleted=False,
        vector="vvvv.vvv",
        path="/image/128290486259603144_1_1698829155..jpg"
    )))


if __name__ == '__main__':
    # print(get_enable_types())
    # test()
    insert_image()
