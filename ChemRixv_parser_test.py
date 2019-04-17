import unittest
from ChemRxiv_parser import ChemRxivParser


class TestChemRxivParser(unittest.TestCase):
    def test_parser(self):
        p = ChemRxivParser()
        for i in p.search("hydrogen"):
            print(i)
        p.get_session().close()
