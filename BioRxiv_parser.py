from time import sleep

from bs4 import BeautifulSoup
from requests import Session, Request

from base_parser import Article, Author, BaseParser


class BioRxivParser(BaseParser):
    def __init__(self, base_url, break_entry=None):
        super().__init__(base_url)
        self.base_url = base_url

        self.current_page = 0

        if break_entry:
            print("Stopping at " + break_entry)
        self._request_session = Session()
        self._current_html = None
        self.max_page = 0
        self.stop = False
        self.break_entry = break_entry

    def _request(self, url):
        req = Request('GET', url, params={"page": str(self.current_page)}, headers=self.headers)
        prepped = self.get_session().prepare_request(req)
        return self.get_session().send(prepped)

    def search(self, topic, max_page=5, req_interval=1):
        url = self.base_url + "search/" + topic
        response = self._request(url)
        yield self.__parse_biorxiv_page(response.content)
        self.current_page += 1
        if self.max_page != 0:
            while self.current_page < self.max_page and self.current_page < max_page and not self.stop:
                response = self._request(url)
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
            if self.break_entry:
                if self.break_entry == a.text:
                    print("Stopping at " + a.text)
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
                doi = i.find("span", "highwire-cite-metadata-doi")
                entries.append(Article(a.text, a.get("href"), authors, doi.text[5:]))

        page = soup.find("li", "pager-last")
        last_page = page.find("a")
        if self.max_page == 0:
            self.max_page = int(last_page.text)
        return entries


