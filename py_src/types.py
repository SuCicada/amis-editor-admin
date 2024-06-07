from dataclasses import dataclass
from typing import Optional, Dict, List


@dataclass
class Segmentation:
    section: str = None  # 文案段落
    tags: [str] = None  # 描述词
    ai_tags: [str] = None   # Ai生成的描述词


@dataclass
class Response:
    code: int
    msg: str
    data: any = None

@dataclass
class CrudResponseData:
    count: int
    rows: List[any]

@dataclass
class CrudResponse(Response):
    code = 0
    msg = "ok"
    data: CrudResponseData = None


@dataclass
class MaterialFile:
    type: str  # image or video
    path: str


@dataclass
class MaterialDB:
    id: str = None
    index: float = None  # order
    section: str = None  # 文案段落
    tags: List[str] = None  # 描述词
    ai_tags: List[str] = None    # Ai描述词
    images: Dict[int, MaterialFile] = None  # generated images: base64
    selected_image: int = None
    upload_image: str = None  # base64
    tags2: List[str] = None  # generated tags from upload_image
    style: str = ""         # 风格选择

    @staticmethod
    def get_by_id(id):
        from .db import table
        data = table.db.getById(id)
        img_material = MaterialDB(**data)
        return img_material

    @staticmethod
    def from_dict(data):
        a = MaterialDB(**data)
        if a.images is not None:
            a.images = {int(k): MaterialFile(**v) for k, v in a.images.items()}
        return a


@dataclass
class VideoMakeForm:
    title: str = None
    body: str = None
    voice: str = None
    is_read_title: bool = None
    video_make_num: int = None
    cover_image: str = None
    bg_image: str = None
    music: str = None
    # 文段段落数据
    content_materials: List[MaterialDB] = None
    express: str = None
    font: str = None
