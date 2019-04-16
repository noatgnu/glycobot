import os
import argparse
from BioRxiv_parser import BioRxivParser

"https://www.biorxiv.org/search/abstract_title%3Aglycosylation%20abstract_title_flags%3Amatch-all%20jcode%3Abiorxiv%20subject_collection_code%3ABiochemistry%2CBioinformatics%2CCell%20Biology%2CMolecular%20Biology%20toc_section%3ANew%20Results%2CContradictory%20Results%2CConfirmatory%20Results%20numresults%3A50%20sort%3Apublication-date%20direction%3Adescending%20format_result%3Acondensed"
"https://www.biorxiv.org/search/glycosylation%20numresults%3A10%20sort%3Apublication-date%20direction%3Adescending"
base_url = "https://www.biorxiv.org/"

if __name__ == "__main__":

    if os.path.isfile("last_seen.txt"):
        with open("last_seen.txt", "rt") as last:
            stop_art = last.readline().strip()
    else:
        stop_art = ""
    parser = argparse.ArgumentParser(description="An application for scraping BioRxiv")

    parser.add_argument("s", type=str, help="BioRxiv search string")
    parser.add_argument("--max", dest="max", type=int, help="Max search page number", default=10)
    parser.add_argument("--bu", dest="bu", type=str, default=base_url, help="BioRxiv base_url value")
    parser.add_argument("--stop-article", dest="sa", type=str, default=stop_art, help="Indicating at which entry should the search end")
    parser.add_argument("--req-interval", dest="ri", type=int, default=1, help="Interval between page navigation")

    args = parser.parse_args()
    p = BioRxivParser(
        base_url=base_url,
        break_entry=args.sa
    )
    a = []
    query = "abstract_title%3A{}%20abstract_title_flags%3Amatch-all%20numresults%3A50%20sort%3Apublication-date" \
            "%20direction%3Adescending".format(args.s)
    for n, i in enumerate(p.search(query, max_page=args.max, req_interval=args.ri)):
        if n == 0:
            with open("last_seen.txt", "wt") as last:
                last.write(i[0].name)
        print(i)
        a.append(i)

    print("Complete.")
