import json
import uuid
from pathlib import Path


class FileInfoWriter:
    def __init__(self, out_put: Path):
        self.content = dict(CREATE=[], INSERT=[], id=-1)
        self._out_put = out_put

    def set_id(self, value):
        self.content["id"] = value

    def add_sql(self, file_id, statement, size):
        table_name = statement.table()
        file_name = f'{table_name}-{file_id}'
        self.content[statement.operate()].append(dict(sqlType=statement.operate(),
                                                      name=file_name,
                                                      id=file_id,
                                                      table=table_name,
                                                      size=size))

    def write(self):
        with open(self._out_put.joinpath("file_list.json"), 'w') as f:
            json.dump(self.content, f)
