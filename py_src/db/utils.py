import os
import shutil
from pathlib import Path
from typing import List

from pysondb.db import JsonDatabase


def clean(db: JsonDatabase):
    from datetime import datetime
    if os.path.exists(db.filename):
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d_%H-%M-%S")
        base = os.path.basename(db.filename)
        backup_file = Path(db.filename).parent / "db_bak" / f"{base}.{formatted_time}.json"
        os.makedirs(backup_file.parent, exist_ok=True)
        shutil.copyfile(db.filename, backup_file)
        db.deleteAll()


def get_page_data_from_db(db: JsonDatabase, page, per_page):
    raw_data = db.getAll()
    count, page_data = get_page_data(raw_data, page, per_page)  # raw_data[(page - 1) * per_page:page * per_page]
    for x in page_data:
        x["id"] = str(x["id"])
    return count, page_data


def get_page_data(raw_data: List[any], page, per_page):
    page_data = raw_data[(page - 1) * per_page:page * per_page]
    return len(raw_data), page_data
