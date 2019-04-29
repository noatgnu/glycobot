from time import sleep

from bs4 import BeautifulSoup
from requests import Session, Request

from base_parser import Article, Author, BaseParser


class BioRxivParser(BaseParser):
    def __init__(self, base_url="https://www.biorxiv.org/"):
        super().__init__(base_url)

        self.current_page = 0

        self._request_session = Session()
        self._current_html = None
        self.max_page = 0
        self.stop = False
        self.break_entry = None

    def search(self, topic, max_page=5, req_interval=1, break_entry=None):
        self.break_entry = break_entry
        if break_entry:
            print("Stopping at " + break_entry)
        url = self.base_url + "search/" + topic
        response = self._request(url, params={"page": str(self.current_page)})
        yield self.__parse_biorxiv_page(response.content)
        self.current_page += 1
        if self.max_page != 0:
            while self.current_page < self.max_page and self.current_page < max_page and not self.stop:
                response = self._request(url, params={"page": str(self.current_page)})
                sleep(req_interval)
                yield self.__parse_biorxiv_page(response.content)
                self.current_page += 1
        self.stop = False

    def __parse_biorxiv_page(self, html_content):
        soup = BeautifulSoup(html_content, "lxml")
        content = soup.find_all("li", "search-result")
        entries = []
        for i in content:
            search_result = i.find("span", "highwire-cite-title")
            a = search_result.find("a", "highwire-cite-linked-title")
            doi = i.find("span", "highwire-cite-metadata-doi")
            if self.break_entry:
                if self.break_entry == doi.text[5:].strip():
                    self.stop = True
                    return entries
            if a:
                authors_search = i.find("span", "highwire-citation-authors")
                authors = []
                for au in authors_search.find_all("span", "highwire-citation-author"):
                    given_name = au.find("span", "nlm-given-names")
                    last_name = au.find("span", "nlm-surname")
                    first = False
                    if "first" in au.attrs["class"]:
                        first = True
                    author = Author(given_name.text, last_name.text, first)
                    authors.append(author)
                biorxiv_id = i.find("span", "highwire-cite-metadata-pages")
                entries.append(Article(a.text, a.get("href"), authors, doi.text[5:].strip(),
                                       id=biorxiv_id[:-2].strip(), source="BioRxiv"))

        pager = soup.find("ul", "pager-items")

        page = pager.find("li", "pager-last")
        if not page:

            page = pager.find("li", "last")
        last_page = page.find("a")
        if self.max_page == 0:
            self.max_page = int(last_page.text)
        return entries


def get_biorxiv(args):
    stop_art = None
    p = BioRxivParser(base_url=args.bu)
    a = []
    query = "abstract_title%3A{}%20abstract_title_flags%3Amatch-all%20numresults%3A50%20sort%3Apublication-date" \
            "%20direction%3Adescending".format(args.s)
    for n, i in enumerate(p.search(query, max_page=args.max, req_interval=args.ri, break_entry=args.sb)):
        if len(i) > 0:
            if n == 0:
                stop_art = i[0].doi
            a += i
    p.close()
    return a, stop_art