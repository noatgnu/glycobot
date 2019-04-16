from base_parser import BaseParser
from requests import Session, Request
from json import loads


base_url = "https://chemrxiv.org/api/items?types=&itemTypes=&licenses=&orderBy=relevant&orderType=desc&limit=40&offset=0&search=glycosylation&institutionId=259"


class ChemRxivParser(BaseParser):
    def __init__(self, base_url="https://chemrxiv.org/api/items", limit=100):
        super().__init__(base_url)
        self.current_offset = 0
        self.limit = limit

    def _request(self, url, search):
        req = Request('GET', url, params={
            "offset": str(self.current_offset),
            "types": "",
            "orderBy": "latest",
            "licenses": "",
            "orderType": "desc",
            "limit": str(self.limit),
            "search": search,
            "institutionId": 259
        }, headers=self.headers)
        prepped = self.get_session().prepare_request(req)
        return self.get_session().send(prepped)

    def search(self, terms):
        response = self._request(self.base_url, terms)
        for i in loads(response.content):
            print(i)


