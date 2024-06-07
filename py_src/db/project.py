from dataclasses import dataclass
from typing import List

import pysondb
from py_src.utils.common import db_path, get_user_id
from py_src.config import WENXIN_PROMPT_CONTENT


@dataclass
class ProjectDB:
    id: str = None
    user_id: str = None
    title: str = ""
    body: str = ""
    selected_cover_image: str = None
    selected_bg_image: str = None
    created_video_result: List[str] = None
    video_generate_progress: float = 0.0
    wenxin: str = ""
    wenxin_prompt: str = WENXIN_PROMPT_CONTENT

db = pysondb.getDb(str(db_path / "project.json"))

# project_db = ProjectDB()
def get_current_project() -> ProjectDB:
    user_id = get_user_id()
    if user_id is None:
        return None
    data = db.getByQuery({"user_id": get_user_id()})
    if data is None or len(data) == 0:
        return None
    else:
        data = data[0]
        return ProjectDB(**data)

def update_current_project_progress(progress: float) -> float:
    """update progress"""
    user_id = get_user_id()
    if user_id is None:
        return 0.0
    query_id = db.getByQuery({"user_id": get_user_id()})[0].get("id")
    db.update({'user_id': user_id, 'id': query_id}, {'video_generate_progress': progress})
