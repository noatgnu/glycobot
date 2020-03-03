import unittest
from ChemRxiv_parser import ChemRxivParser


class TestChemRxivParser(unittest.TestCase):
    def test_parser(self):
        p = ChemRxivParser()
        for i in p.search('glycosylation or lectin or carbohydrate or glycoprotein or glycan or glycosyltransferase or sialic', break_entry="11911209"):
            for i2 in i:
                print(i2.id)
        p.get_session().close()
