# https://pole-emploi.io/data/api/rome?tabgroup-api=documentation&doc-section=api-doc-section-caracteristiques
from typing import List
import requests
from ...base import Api as BaseApi


class Api(BaseApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # params
        self.url = kwargs.get("url", "https://api.pole-emploi.io/partenaire/rome/v1/")

    def scope(self) -> str:
        return "api_romev1 nomenclatureRome"

    def appellation(self, codes: List[str] = [], code: str = None, **kwargs):
        """Call to endpoint : [https://api.pole-emploi.io/partenaire/rome/v1/appellation](https://api.pole-emploi.io/partenaire/rome/v1/appellation)

        Parameters:
            codes: list of codes to search

            code: specific code to search

        Returns:
            response: The request object response from the api
        """

        url = self.url + "/appellation"

        # get auth header
        headers = kwargs.pop("headers", {})
        headers = self.get_auth_header(headers)

        # priority given to search by code
        if code:
            url += f"/{code}"
            return requests.get(url, headers=headers, timeout=10)

        # codes search

        # transform into params
        params = [(k, kwargs[k]) for k in kwargs.keys()]

        # add the codes
        for code in codes:
            params.append(("code", code))

        return requests.get(url, params=params, headers=headers, timeout=10)

    def metier(self, **kwargs):
        """Call to endpoint : [https://api.pole-emploi.io/partenaire/rome/v1/metier](https://api.pole-emploi.io/partenaire/rome/v1/metier)

        Returns:
            response (requests.Response):
        """
        url = self.url + "/metier"

        # get auth header
        headers = kwargs.pop("headers", {})
        headers = self.get_auth_header(headers)

        return requests.get(url, params=kwargs, headers=headers, timeout=10)

    def domaineprofessionnel(self, **kwargs):
        """Call to endpoint : [https://api.pole-emploi.io/partenaire/rome/v1/domaineprofessionnel](https://api.pole-emploi.io/partenaire/rome/v1/domaineprofessionnel)

        Returns:
            response (requests.Response):
        """
        url = self.url + "/domaineprofessionnel"

        # get auth header
        headers = kwargs.pop("headers", {})
        headers = self.get_auth_header(headers)

        # params
        return requests.get(url, params=kwargs, headers=headers, timeout=10)
