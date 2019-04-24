from base_parser import BaseParser, Author, Article
from requests import Request
from json import loads


base_url = "https://chemrxiv.org/api/items?types=&itemTypes=&licenses=&orderBy=relevant&orderType=desc&limit=40&offset=0&search=glycosylation&institutionId=259"


class ChemRxivParser(BaseParser):
    def __init__(self, base_url="https://chemrxiv.org/api/items", limit=100):
        super().__init__(base_url)
        self.current_offset = 0
        self.limit = limit
        self.current_page = 0

    def search(self, terms, max_page=10, break_entry=None):
        response = self._request(self.base_url, params={
            "offset": str(self.current_offset),
            "types": "",
            "orderBy": "latest",
            "licenses": "",
            "orderType": "desc",
            "limit": str(self.limit),
            "search": terms,
            "institutionId": 259
        })
        entries = []
        content = loads(response.content)
        for i in content:
            if break_entry:
                if break_entry == i["data"]["title"]:
                    break
            authors = []
            for a in i["data"]["authors"]:
                authors.append(Author(a["name"], ""))
            entries.append(Article(i["data"]["title"], i["data"]["publicUrl"], authors))
        yield entries
        if len(content) == self.limit and self.current_page < max_page:
            self.current_offset += self.limit
            yield from self.search(terms, max_page)
            self.current_page += 1


def get_chemrxiv(args):
    stop_art = None
    p = ChemRxivParser(base_url=args.cu)
    a = []
    for n, i in enumerate(p.search("glycosylation", max_page=args.max, break_entry=args.sc)):
        if len(i) > 0:
            if n == 0:
                stop_art = i[0].name
            a += i
    p.close()
    return a, stop_art