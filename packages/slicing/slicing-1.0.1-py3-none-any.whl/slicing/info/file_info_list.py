import json
from pathlib import Path

from slicing.info.file_info import FileInfo


class FileInfoList:
    INSERT_LIST = "INSERT"
    CREATE_LIST = "CREATE"
    ALL_LIST = "ALL"

    def __init__(self, where: Path):
        self._where = where

    def id(self):
        return self.read().get("id")

    def read(self):
        with open(self._where.joinpath("file_list.json")) as f:
            return json.load(f)

    def create_files(self) -> list[FileInfo]:
        return [FileInfo(file.get("sqlType"), file.get("name"),
                         file.get("table"), file.get("id"))
                for file in self.read().get(FileInfoList.CREATE_LIST)]

    def insert_files(self) -> list[FileInfo]:
        return [FileInfo(file.get("sqlType"), file.get("name"),
                         file.get("table"), file.get("id"))
                for file in self.read().get(FileInfoList.INSERT_LIST)]

    def lists(self, mode: str = "ALL_LIST") -> list[FileInfo]:
        """
        返回 SQL 的文件名列表
        :param mode:
        FileInfoList.INSERT_LIST 插入数据的 SQL
        FileInfoList.CREATE_LIST 创建表单的 SQL
        FileInfoList.ALL_LIST 创建和插入数据的 SQL

        :type mode:
        :return: sql 文件的列表
        :rtype:
        """
        if mode == FileInfoList.INSERT_LIST:
            return self.insert_files()
        elif mode == FileInfoList.CREATE_LIST:
            return self.create_files()
        elif mode == FileInfoList.ALL_LIST:
            all_list = self.create_files()
            all_list.extend(self.insert_files())
            return all_list

    def table(self, mode: str = "INSERT_LIST") -> list[str]:
        """
        返回 表名
        :param mode:
        FileInfoList.INSERT_LIST 插入数据的 SQL 的表名
        FileInfoList.CREATE_LIST 创建表单的 SQL 的表名
        FileInfoList.ALL_LIST 创建和插入数据的 SQL交集 的表名
        :type mode:
        :return: 表名的列表
        :rtype:
        """
        files = self.lists(mode=mode)
        tables = set()
        for info in files:
            tables.add(info.table)
        return list(tables)

    def find(self, table: str, mode: str = "INSERT_LIST") -> list[FileInfo]:
        """

        :param table:
        :type table:
        :param mode:
        :type mode:
        :return:
        :rtype:
        """
        files = self.lists(mode=mode)
        return list(filter(lambda info: info.table == table, files))



