class Insert:
    def __init__(self, token):
        self._token = token

    @classmethod
    def match(cls, token):
        return str(token.ttype) == "Token.Keyword.DML" and token.value.upper() == "INSERT"

    def accept(self, statement):
        statement.info["Type"] = self._token.value.upper()
