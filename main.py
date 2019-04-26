import os
import argparse
from BioRxiv_parser import get_biorxiv
from ChemRxiv_parser import get_chemrxiv
from json import load, dumps
import tweepy
import logging
import time
if __name__ == "__main__":
    logging.basicConfig(filename="bot.log", level=logging.DEBUG)
    if os.path.isfile("last_seen.json"):
        with open("last_seen.json", "rt") as last:
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
    parser.add_argument("--cu", dest="cu", type=str, default="https://chemrxiv.org/api/items", help="ChemRxiv base_url value")
    parser.add_argument("--stop-article-bio", dest="sb", type=str, default=stop_art["BioRxiv"],
                        help="Indicating at which entry should the search end")
    parser.add_argument("--stop-article-chem", dest="sc", type=str, default=stop_art["ChemRxiv"],
                        help="Indicating at which entry should the search end")
    parser.add_argument("--req-interval", dest="ri", type=int, default=1, help="Interval between page navigation")
    parser.add_argument("--enable-tweet", dest="et", action='store_true', help="Enable tweeting")
    parser.add_argument("--auto-tweet", dest="at", action='store_true', help="Let glycobot automatically send out tweet of new publication")

    args = parser.parse_args()
    print(args.__dict__)
    art_bio, last_bio = get_biorxiv(args)
    art_chem, last_chem = get_chemrxiv(args)
    if last_bio:
        stop_art["BioRxiv"] = last_bio
    if last_chem:
        stop_art["ChemRxiv"] = last_chem

    with open("last_seen.json", "wt") as last:
        s = dumps(stop_art)
        last.write(s)

    print("Complete.")

    if args.et:
        with open("config.json", "rt") as conf:
            config = load(conf)
            auth = tweepy.OAuthHandler(config["consumer_api"], config["consumer_secret"])
            auth.set_access_token(config["access_token"], config["acess_secret"])
            api = tweepy.API(auth)
            print("BioRxiv: {}".format(len(art_bio)))
            print("ChemRxic: {}".format(len(art_chem)))
            for i in art_bio + art_chem:
                if len(i.name) > 100:
                    tweet = i.name[0:100] + "..."
                else:
                    tweet = i.name

                if i.doi:
                    tweet += " " + i.doi
                else:
                    tweet += " " + i.href
                tweet += " #glycotime"

                if args.at:
                    print(tweet)
                    logging.info(tweet)
                    api.update_status(tweet)
                else:
                    a = input(tweet + " (y/n/stop):")
                    if a == "y":
                        api.update_status(tweet)
                        logging.info(tweet)
                    elif a == "n":
                        pass
                    elif a == "stop":
                        break
                time.sleep(1)

    # For deleting all tweet
    # for status in tweepy.Cursor(api.user_timeline).items():
    #     api.destroy_status(status.id)
