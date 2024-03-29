#python main.py -s="glycosylation glycation lectin carbohydrate glycoprotein glycan glycosyltransferase" --max=3 --to-txt


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
    parser.add_argument("--max", dest="max", type=int, help="Max search page number", default=3)
    parser.add_argument("--bu", dest="bu", type=str, default="https://www.biorxiv.org/", help="BioRxiv base_url value")
    parser.add_argument("--cu", dest="cu", type=str, default="https://chemrxiv.org/engage/api-gateway/chemrxiv/graphql", help="ChemRxiv base_url value")
    parser.add_argument("--stop-article-bio", dest="sb", type=str, default=stop_art["BioRxiv"],
                        help="Indicating at which entry should the search end")
    parser.add_argument("--stop-article-chem", dest="sc", type=str, default=stop_art["ChemRxiv"],
                        help="Indicating at which entry should the search end")
    parser.add_argument("--req-interval", dest="ri", type=int, default=1, help="Interval between page navigation")
    parser.add_argument("--enable-tweet", dest="et", action='store_true', help="Enable tweeting")
    parser.add_argument("--auto-tweet", dest="at", action='store_true', help="Let glycobot automatically send out tweet of new publication")
    parser.add_argument("--auto-tweet-delay", dest="ad", type=int, default=1200,
                        help="Delay interval between tweet")
    parser.add_argument("--to-txt", dest="tt", action='store_true', help="Write into a txt file")


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
    tweets = []
    for i in art_bio + art_chem:
        if len(i.name) > 200:
            tweet = i.name[0:200] + "..."
        else:
            tweet = i.name
        # tweet += " " + i.href
        if i.doi:
            tweet += " " + i.doi
        else:
            tweet += " " + i.href
        tweet += " #glycotime"
        tweets.append(tweet)
        print(tweet)

    if args.et:
        with open("config.json", "rt") as conf:
            config = load(conf)
            auth = tweepy.OAuthHandler(config["consumer_api"], config["consumer_secret"])
            auth.set_access_token(config["access_token"], config["acess_secret"])
            api = tweepy.API(auth)
            print("BioRxiv: {}".format(len(art_bio)))
            print("ChemRxic: {}".format(len(art_chem)))

            for t in tweets:
                if args.at:
                    print(t)

                    logging.info(t)
                    api.update_status(t)

                else:
                    a = input(t + " (y/n/stop):")
                    if a == "y":
                        api.update_status(t)
                        logging.info(t)

                    elif a == "n":
                        pass
                    elif a == "stop":
                        break
                time.sleep(args.ad)

    # For deleting all tweet
    # for status in tweepy.Cursor(api.user_timeline).items():
    #     api.destroy_status(status.id)
