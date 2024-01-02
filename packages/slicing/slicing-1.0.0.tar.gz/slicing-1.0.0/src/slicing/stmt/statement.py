import sqlparse

from slicing.stmt.tokens.create import Create
from slicing.stmt.tokens.drop import Drop
from slicing.stmt.tokens.identifier import Identifier
from slicing.stmt.tokens.insert import Insert
from slicing.stmt.tokens.into import Into
from slicing.stmt.tokens.table import Table


class Statement:
    def __init__(self, statement):
        self.statement = statement
        self.info = dict()

    def visitor(self):
        parsed = sqlparse.parse(self.statement)
        if len(parsed) == 0: return
        for token in parsed[0].tokens:
            for token_class in [Create, Drop, Identifier, Insert, Table, Into]:
                if token_class.match(token):
                    token_class(token).accept(self)

    def table(self):
        return self.info.get("TableName").replace("`", "")

    def operate(self):
        return self.info.get("Type")

    def ignore(self):
        return self.info.get("Type") is None
