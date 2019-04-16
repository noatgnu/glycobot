from requests import Session, Request

class BaseParser:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {"User-Agent": "Python, toan.phung@uq.net.au"}
        print("Initiating session")
        self._request_session = Session()

    def search(self, *args, **kwargs):
        pass

    def get_session(self):
        return self._request_session

class Article:
    def __init__(self, name, href, authors=None, doi=None):
        self.name = name
        self.href = href
        self.authors = authors
        self.doi = doi

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class Author:
    def __init__(self, given_name, last_name, first=False):
        self.given_name = given_name
        self.last_name = last_name
        self.first = first

    def __repr__(self):
        return self.given_name + " " + self.last_name

    def __str__(self):
        return self.given_name + " " + self.last_name