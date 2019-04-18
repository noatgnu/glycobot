import os
import argparse
from BioRxiv_parser import get_biorxiv
from ChemRxiv_parser import get_chemrxiv
from json import load, dump
import tweepy

if __name__ == "__main__":
    with open("config.json", "rb") as conf:
        config = load(conf)
        auth = tweepy.OAuthHandler(config["consumer_api"], config["consumer_secret"])
        auth.set_access_token(config["access_token"], config["acess_secret"])
        api = tweepy.API(auth)

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
    parser.add_argument("--bu", dest="bu", type=str, default="https://www.biorxiv.org/", help="BioRxiv base_url value")
    parser.add_argument("--")
    parser.add_argument("--stop-article-bio", dest="sb", type=str, default=stop_art["BioRxiv"],
                        help="Indicating at which entry should the search end")
    parser.add_argument("--stop-article-chem", dest="sc", type=str, default=stop_art["ChemRxiv"],
                        help="Indicating at which entry should the search end")
    parser.add_argument("--req-interval", dest="ri", type=int, default=1, help="Interval between page navigation")

    args = parser.parse_args()
    art_bio, stop_art["BioRxiv"] = get_biorxiv(args)
    art_chem, stop_art["ChemRxiv"] = get_chemrxiv(args)

    with open("last_seen.json", "wb") as last:
        dump(stop_art, last)

    print("Complete.")
