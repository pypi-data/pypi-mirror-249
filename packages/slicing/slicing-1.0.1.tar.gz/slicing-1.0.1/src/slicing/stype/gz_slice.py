import time
from pathlib import Path
import gzip

from slicing.stype.slice import Slice


class GZSlice(Slice):
    MAGIC = b'\x1f\x8b'

    @staticmethod
    def magic(file):
        with open(file, 'rb') as f:
            magic_byte = f.read(2)
        return magic_byte == GZSlice.MAGIC


    def read(self, file: Path):
        if self.writer is None: raise Exception("Slice is not ready")
        with gzip.open(file, mode='rb') as f:
            self.statements(f)



