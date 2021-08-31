from typing import List

from requests import Session, Request


class BaseParser:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.headers = {"User-Agent": "Python, toan.phung@uq.net.au"}
        print("Initiating session")
        self._request_session = Session()

    def _request(self, url, params=None, data=None, request_type = 'GET'):
        if request_type == 'GET':
            req = Request(request_type, url, params=params, headers=self.headers)
        elif request_type == 'POST':
            req = Request(request_type, url, json=data, headers=self.headers)
        prepped = self.get_session().prepare_request(req)
        print(prepped.url)
        return self.get_session().send(prepped)

    def search(self, *args, **kwargs):
        pass

    def get_session(self):
        return self._request_session

    def close(self):
        self.get_session().close()


class Author:
    def __init__(self, given_name: str, last_name: str, first: bool = False):
        self.given_name = given_name
        self.last_name = last_name
        self.first = first

    def __repr__(self):
        return self.given_name + " " + self.last_name

    def __str__(self):
        return self.given_name + " " + self.last_name


class Article:
    def __init__(self, name: str, href: str, authors: List[Author] = None, doi: str = None, **kwargs):
        self.name = name
        self.href = href
        self.authors = authors
        self.doi = doi
        self.id = ""
        self.source = ""
        print(kwargs)
        for k in kwargs:
            if k in self.__dict__:
                setattr(self, k, kwargs[k])

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name