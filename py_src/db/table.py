import os
import sys
from typing import List

import pysondb

from py_src.types import MaterialDB

# project_path = Path(__file__).parent.parent
sys.path.append(os.path.dirname(__file__))
from py_src.utils.common import *


db = pysondb.getDb(str(db_path / "db.json"))


def getSortedAll():
    all_data = db.getAll()
    all_data = sorted(all_data, key=lambda x: x["index"])
    return all_data

def getSortedAllObj() -> List[MaterialDB]:
    datas = getSortedAll()
    res = []
    for x in datas:
        res.append(MaterialDB.from_dict(x))
    return res

def count():
    return len(db.getAll())





if __name__ == '__main__':
    # db.add({
    # "nihoa":222
    # })
    res = db.getAll()
