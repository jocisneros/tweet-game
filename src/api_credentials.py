class APICredentials:
    def __init__(self, key="", secret="", bearer=""):
        self._key = key;
        self._secret = secret;
        self._bearer = bearer;

    def get_key(self) -> str:
        return self._key;

    def get_secret(self) -> str:
        return self._secret;

    def get_bearer(self) -> str:
        return self._bearer;