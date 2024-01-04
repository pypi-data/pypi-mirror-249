import sqlparse.sql


class Identifier:
    def __init__(self, token):
        self._token = token

    @classmethod
    def match(cls, token):
        return token.ttype is None and type(token) == sqlparse.sql.Identifier

    def accept(self, statement):
        if statement.info.get("TableName") == "WaitFill":
            statement.info["TableName"] = self._token.value
