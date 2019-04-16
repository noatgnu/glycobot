import unittest
from ChemRxiv_parser import ChemRxivParser


class TestChemRxivParser(unittest.TestCase):
    def test_parser(self):
        p = ChemRxivParser()
        p.search("glycosylation")