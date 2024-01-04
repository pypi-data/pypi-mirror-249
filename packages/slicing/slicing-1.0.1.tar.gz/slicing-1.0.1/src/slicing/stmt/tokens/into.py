class Into:
    def __init__(self, token):
        self._token = token

    @classmethod
    def match(cls, token):
        return str(token.ttype) == "Token.Keyword" and token.value.upper() == "INTO"

    def accept(self, statement):
        statement.info["TableName"] = "WaitFill"
