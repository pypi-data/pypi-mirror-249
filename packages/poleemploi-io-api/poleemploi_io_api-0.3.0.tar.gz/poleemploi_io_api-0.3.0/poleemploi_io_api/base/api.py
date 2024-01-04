import requests
from .schemas import Token


class Api:
    def __init__(self, **kwargs):
        # params
        self._token_url = kwargs.get("url", "https://entreprise.pole-emploi.fr")
        self._client_secret = kwargs.get("client_secret", None)
        self._client_id = kwargs.get("client_id", None)

        self._access_token = None

    def scope(self) -> str:
        """This method enables you to define the scope for your api.

        Raises:
            NotImplementedError: You must define this function to define the scope of the token
        """
        raise NotImplementedError(
            "You must define this function to define the scope of the token"
        )

    def _get_access_token(self):
        """This method sets the access token to be used on your api.

        Raises:
            ValueError: If poleemploi.io raises a status_code different from 200
        """
        scope = self.scope()

        params = {
            "grant_type": "client_credentials",
            "scope": scope,
        }
        data = {"client_secret": self._client_secret, "client_id": self._client_id}

        r = requests.post(
            self._token_url + "/connexion/oauth2/access_token?realm=%2Fpartenaire",
            params=params,
            data=data,
            timeout=10,
        )

        if r.status_code != 200:
            raise ValueError(
                f"Could not read token from api. status_code={r.status_code} response={r.content}"
            )

        self._access_token = Token(**r.json())

    def get_auth_header(self, header=None):
        """If an access token was found, this method returns the provided header
        with the Authorization added.

        Args:
            header (dict, optional): this is the header you want to use for your api call.
        """
        if not self._access_token:
            self._get_access_token()

        if not header:
            header = {}

        header[
            "Authorization"
        ] = f"{self._access_token.token_type} {self._access_token.access_token}"

        return header
