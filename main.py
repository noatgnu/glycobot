import os
import argparse
from BioRxiv_parser import BioRxivParser
from ChemRxiv_parser import ChemRxivParser
from json import load, dump
base_url = "https://www.biorxiv.org/"

if __name__ == "__main__":

    if os.path.isfile("last_seen.json"):
        with open("last_seen.json", "rb") as last:
            stop_art = load(last)
    else:
        stop_art = {
            "BioRxiv": None,
            "ChemRxiv": None
        }
    parser = argparse.ArgumentParser(description="An application for scraping BioRxiv")

    parser.add_argument("s", type=str, help="BioRxiv search string")
    parser.add_argument("--max", dest="max", type=int, help="Max search page number", default=10)
    parser.add_argument("--bu", dest="bu", type=str, default=base_url, help="BioRxiv base_url value")

    parser.add_argument("--stop-article-bio", dest="sb", type=str, default=stop_art["BioRxiv"],
                        help="Indicating at which entry should the search end")
    parser.add_argument("--stop-article-chem", dest="sc", type=str, default=stop_art["ChemRxiv"],
                        help="Indicating at which entry should the search end")
    parser.add_argument("--req-interval", dest="ri", type=int, default=1, help="Interval between page navigation")

    args = parser.parse_args()
    p = BioRxivParser()
    a = []

    query = "abstract_title%3A{}%20abstract_title_flags%3Amatch-all%20numresults%3A50%20sort%3Apublication-date" \
            "%20direction%3Adescending".format(args.s)
    for n, i in enumerate(p.search(query, max_page=args.max, req_interval=args.ri, break_entry=args.sb)):
        if n == 0:
            stop_art["BioRxiv"] = i[0].name
        print(i)
        a.append(i)
    p.close()
    p = ChemRxivParser()
    for n, i in enumerate(p.search("glycosylation", max_page=args.max, break_entry=args.sc)):
        if n == 0:
            stop_art["ChemRxiv"] = i[0].name
        print(i)
        
    with open("last_seen.json", "wb") as last:
        dump(stop_art, last)
    print("Complete.")
