class Create:
    def __init__(self, token):
        self._token = token

    @classmethod
    def match(cls, token):
        return str(token.ttype) == "Token.Keyword.DDL" and token.value.upper() == "CREATE"

    def accept(self, statement):
        statement.info["Type"] = self._token.value.upper()
