class Table:
    def __init__(self, token):
        self._token = token

    @classmethod
    def match(cls, token):
        return str(token.ttype) == "Token.Keyword" and token.value.upper() == "TABLE"

    def accept(self, statement):
        statement.info["TableName"] = "WaitFill"
