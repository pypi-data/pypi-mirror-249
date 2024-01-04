# https://pole-emploi.io/data/api/rome?tabgroup-api=documentation&doc-section=api-doc-section-caracteristiques
import requests
from ...base import Api as BaseApi


class ApiMetier(BaseApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # params
        self.url = kwargs.get(
            "url", "https://api.pole-emploi.io/partenaire/rome-metiers/v1/metiers"
        )

    def scope(self) -> str:
        return "api_rome-metiersv1 nomenclatureRome"

    def _get(self, url: str, kwargs: dict):
        # headers
        headers = kwargs.pop("headers", {})
        headers = self.get_auth_header(headers)

        # params
        params = [(k, kwargs[k]) for k in kwargs.keys()]

        return requests.get(url, params=params, headers=headers, timeout=10)

    def theme(self, **kwargs):
        """Call to endpoint : [https://api.pole-emploi.io/partenaire/rome/v1/theme](https://api.pole-emploi.io/partenaire/rome/v1/theme)
        Rules:
            If `code` in kwargs then the call will be made to `theme/code`

            Else the endpoint will be `theme/`

        Returns:
            response (requests.Response):
        """
        url = self.url + "/theme"

        code: str = kwargs.pop("code", None)
        if code:
            url += f"/{code.upper()}"

        return self._get(url, kwargs)

    def metier(self, **kwargs):
        """Call to endpoint : [https://api.pole-emploi.io/partenaire/rome/v1/metier](https://api.pole-emploi.io/partenaire/rome/v1/metier)
        Rules:
            If `code` in kwargs then the call will be made to `metier/code`

            Else the endpoint will be `metier/`

        Returns:
            response (requests.Response):
        """
        url = self.url + "/metier"
        code: str = kwargs.pop("code", None)
        if code:
            url += f"/{code.upper()}"
        return self._get(url, kwargs)

    def granddomain(self, **kwargs):
        """Call to endpoint : [https://api.pole-emploi.io/partenaire/rome/v1/grand-domaine](https://api.pole-emploi.io/partenaire/rome/v1/grand-domaine)
        Rules:
            If `code` in kwargs then the call will be made to `grand-domaine/code`

            Else the endpoint will be `grand-domaine/`

        Returns:
            response (requests.Response):
        """
        url = self.url + "/grand-domaine"
        code: str = kwargs.pop("code", None)
        if code:
            url += f"/{code.upper()}"
        return self._get(url, kwargs)

    def domaineprofessionnel(self, **kwargs):
        """Call to endpoint : [https://api.pole-emploi.io/partenaire/rome/v1/domaine-professionnel](https://api.pole-emploi.io/partenaire/rome/v1/domaine-professionnel)
        Rules:
            If `code` in kwargs then the call will be made to `domaine-professionnel/code`

            Else the endpoint will be `domaine-professionnel/`

        Returns:
            response (requests.Response):
        """
        url = self.url + "/domaine-professionnel"
        code: str = kwargs.pop("code", None)
        if code:
            url += f"/{code.upper()}"
        return self._get(url, kwargs)

    def appellation(self, **kwargs):
        """Call to endpoint : [https://api.pole-emploi.io/partenaire/rome/v1/appellation](https://api.pole-emploi.io/partenaire/rome/v1/appellation)
        Rules:
            If `code` in kwargs then the call will be made to `appellation/code`

            If `q` in kwargs then the call will be made to `appellation/requete`

            Otherwise the endpoint will be `appellation/`

        Returns:
            response (requests.Response):
        """
        url = self.url + "/appellation"
        code: int = kwargs.pop("code", None)
        query = kwargs.get("q")
        if code:
            url += f"/{code}"
        elif query:
            url += "/requete"

        return self._get(url, kwargs)
