import re
import time
from pathlib import Path

from slicing.stype.gz_slice import GZSlice
from slicing.stype.sql_slice import SQLSlice
from slicing.stype.zip_slice import ZipSlice


class SliceFactory:

    @staticmethod
    def zip(file_path):
        if file_path.name.endswith(".zip") and ZipSlice.magic(file_path):
            return ZipSlice()

    @staticmethod
    def gz(file_path):
        if file_path.name.endswith(".gz") and GZSlice.magic(file_path):
            return GZSlice()

    @staticmethod
    def sql(file_path):
        if file_path.name.endswith(".sql"):
            return SQLSlice()

    @staticmethod
    def is_valid_folder_name(absolute_out_put_folder: Path):
        pattern = r'^[^<>:""/|\?*]*[^<>:""/|\?*]$'
        if re.match(pattern, str(absolute_out_put_folder)):
            return True
        else:
            return False

    @staticmethod
    def slice(absolute_file_path: Path, absolute_out_put_folder: Path):
        """
        分割文件
        :param absolute_file_path: 文件的绝对路径
        :type absolute_file_path: pathlib.Path
        :param absolute_out_put_folder: 输出文件夹的绝对路径
        :type absolute_out_put_folder: pathlib.Path
        :return: 任务的ID
        :rtype: uuid
        """
        if not absolute_file_path.exists(): raise Exception(f'{absolute_file_path} is not exist')
        if not SliceFactory.is_valid_folder_name(absolute_out_put_folder):
            raise Exception(f'{absolute_out_put_folder} is not folder name')
        if absolute_file_path.is_file():
            slicer = SliceFactory.zip(absolute_file_path) \
                     or SliceFactory.gz(absolute_file_path) \
                     or SliceFactory.sql(absolute_file_path)
            slicer.ready(out_put=absolute_out_put_folder)
            slicer.slice(file=absolute_file_path)
            if slicer is None:
                raise Exception(f"Unknown format {absolute_file_path}")
            return slicer.task_id
        else:
            raise Exception(f'{absolute_file_path} is not file')


if __name__ == '__main__':
    start = time.perf_counter()
    # SliceFactory.slice(Path("D:\\workspace\\Resources\\eclinical_design_dev_27_20220822084120.zip"), Path("YYYYY"))
    # SliceFactory.slice(absolute_file_path=Path("D:\\workspace\\Resources\\eclinical_edc_prod_21_20230630025243.sql.gz"),
    #                    absolute_out_put_folder=Path("YYYYY"))
    tid = SliceFactory.slice(Path("D:\\workspace\\Resources\\eclinical_design_dev_27_20220822084120.sql"), Path("YYYYY"))
    print(tid)
    print(time.perf_counter() - start)

