import os
import threading
import uuid
from pathlib import Path
from queue import Queue


from slicing.stmt.statement import Statement


class Writer(threading.Thread):
    def __init__(self, slice_ins):
        super().__init__()
        self._slice_ins = slice_ins
        self.__out_path_folder = Path(slice_ins.out_put).joinpath(slice_ins.task_id)
        self.sql_statements = Queue()
        self._finish = False
        self.stop_event = threading.Event()

    def add_statements(self, statements: list[bytes]):
        self.sql_statements.put(statements)

    def write_file(self, sql_statement_bytes: list[bytes]):
        sql_statement = sql_statement_bytes[0][0:200].decode()
        statement = Statement(sql_statement)
        statement.visitor()
        if not statement.ignore():
            folder = self.create_folder(statement.operate())
            table_name = statement.table()

            file_id = str(uuid.uuid4()).replace("-", "")
            file_name = f'{table_name}-{file_id}'
            with open(folder.joinpath(Path(f'{file_name}.sql')), 'ab') as f:
                if statement.operate().upper() == "CREATE":
                    f.write(f'DROP TABLE IF EXISTS `{table_name}`;\n'.encode("UTF-8"))
                for sql_bytes in sql_statement_bytes:
                    f.write(sql_bytes)
            size = os.path.getsize(folder.joinpath(Path(f'{file_name}.sql')))
            self._slice_ins.file_list_writer.add_sql(file_id, statement, size )

    def create_folder(self, operate):
        path = self.__out_path_folder.joinpath(operate)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return path

    def run(self):
        try:
            while not self.stop_event.is_set():
                if self.sql_statements.qsize() > 0 or not self._finish:
                    sql_statement_bytes = self.sql_statements.get()
                    if sql_statement_bytes == "Thread Stop": continue
                    self.write_file(sql_statement_bytes)
        except Exception as e:
            raise e

    def finish(self):
        self.stop_event.set()
        self._finish = True
        self.sql_statements.put("Thread Stop")

    def stop(self):
        self.finish()

