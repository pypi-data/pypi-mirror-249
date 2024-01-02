import time
import zipfile
from pathlib import Path

from slicing.stype.slice import Slice


class ZipSlice(Slice):
    MAGIC = b'\x50\x4b\x03\x04'

    @staticmethod
    def magic(file):
        with open(file, 'rb') as f:
            magic_byte = f.read(4)
        return magic_byte == ZipSlice.MAGIC

    def read(self, file: Path):
        if self.writer is None: raise Exception("Slice is not ready")
        with zipfile.ZipFile(file, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            for file_name in file_list:
                with zip_ref.open(file_name, 'r') as file:
                    self.statements(file)



