import unittest
from BioRxiv_parser import BioRxivParser


class TestBioRxivParser(unittest.TestCase):
    def test_parser(self):
        p = BioRxivParser()
        for i in p.search("glycosylation"):
            for i2 in i:
                print(i2.id)
        p.get_session().close()
