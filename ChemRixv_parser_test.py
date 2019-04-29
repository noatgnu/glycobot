import unittest
from ChemRxiv_parser import ChemRxivParser


class TestChemRxivParser(unittest.TestCase):
    def test_parser(self):
        p = ChemRxivParser()
        for i in p.search("glycosylation"):
            for i2 in i:
                print(i2.id)
        p.get_session().close()
