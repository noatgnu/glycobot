import unittest
from BioRxiv_parser import BioRxivParser


class TestBioRxivParser(unittest.TestCase):
    def test_parser(self):
        p = BioRxivParser()
        query = "abstract_title%3A{}%20abstract_title_flags%3Amatch-any%20numresults%3A50%20sort%3Apublication-date" \
                "%20direction%3Adescending".format('glycosylation glycation lectin carbohydrate glycoprotein glycan glycosyltransferase "sialic acid"')
        for i in p.search(query):
            for i2 in i:
                print(i2.id)
        p.get_session().close()
