"""
Client class for the Hydra-based JSON API of the German Union Catalogue of Serials (ZDB)

For more information on the interface, have a look at
https://zeitschriftendatenbank.de/services/schnittstellen/json-api

For more information on querying the interface, see
https://zeitschriftendatenbank.de/services/schnittstellen/hilfe-zur-suche
"""

from . import docs
from . import utils


class Hydra:

    def __init__(self, headers={}, loglevel=0):
        self.headers = headers
        self.logger = utils.get_logger("zdbpydra", loglevel=loglevel)
        self.BASE_URL = "https://zeitschriftendatenbank.de/api/tit"
        self.CONTEXT_URL = "https://zeitschriftendatenbank.de/api/context/zdb.jsonld"

    def _fetch(self, url):
        return utils.json_request(url, headers=self.headers)

    def context(self):
        return self._fetch(self.CONTEXT_URL)

    def _title(self, id):
        url = "{0}/{1}.jsonld".format(self.BASE_URL, id)
        response = self._fetch(url)
        if response is not None:
            if "data" in response:  # field is only present if title was found
                return docs.TitleResponseParser(response)
            else:
                self.logger.info("Title with id {0} not found!".format(id))

    def title(self, id, pica=False):
        response = self._title(id)
        if response is not None:
            if pica:
                return response._parser_data
            return response

    def address(self, query, size, page):
        return "{0}.jsonld?q={1}&size={2}&page={3}".format(self.BASE_URL,
                                                           query, size, page)

    def total(self, query):
        url = self.address(query, 1, 1)
        response = self._fetch(url)
        if response is not None:
            return docs.SearchResponseParser(response).total_items
        return 0

    def _search(self, query, size, page):
        url = self.address(query, size, page)
        response = self._fetch(url)
        if response is not None:
            return docs.SearchResponseParser(response)

    def search(self, query, size=10, page=1):
        response = self._search(query, size, page)
        if response is not None:
            if type(response.member) == list:
                if len(response.member) > 0:
                    return [docs.TitleResponseParser(title)
                            for title in response.member]

    def stream(self, query, size=100, page=1):
        total = self.total(query)
        if total == 0:
            return
        url = self.address(query, size, page)
        while url:
            result = self._fetch(url)
            if result is not None:
                result = docs.SearchResponseParser(result)
                titles = result.member
                if titles is not None:
                    for title in titles:
                        yield docs.TitleResponseParser(title)
                url = result.view_next
            else:
                url = None

    def scroll(self, query, size=100, page=1):
        titles = []
        for doc in self.stream(query, size=size, page=page):
            titles.append(doc)
        return titles
