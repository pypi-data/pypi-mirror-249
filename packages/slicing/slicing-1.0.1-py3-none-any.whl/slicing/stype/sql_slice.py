import time
from pathlib import Path

from slicing.stype.slice import Slice


class SQLSlice(Slice):
    def read(self, file: Path):
        if self.writer is None: raise Exception("Slice is not ready")
        with open(file, 'rb') as file:
            self.statements(file)



