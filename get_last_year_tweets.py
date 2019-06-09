import tweepy
import datetime
from datetime import date
import json
from config import *
import string

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))

def add_days(d, days):
    try:
        return d.replace(day = d.day + days)
    except ValueError:
        return d + (date(2019, 1, d.day + days) - date(2019, 1, 1))


def get_last_year_tweets():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API(auth)
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    same_day_last_year = add_years(today,-1)
    tomorrow_last_year = add_days(same_day_last_year,11)
    print same_day_last_year, tomorrow_last_year

    urls = []
    limited_tweets = api.user_timeline(username)

    while (limited_tweets[-1].created_at > same_day_last_year):
        print("Last Tweet @", limited_tweets[-1].created_at, " - fetching some more")
        limited_tweets = api.user_timeline(username, max_id = limited_tweets[-1].id)
        for tweet in limited_tweets:
            if tweet.created_at < tomorrow_last_year and tweet.created_at > same_day_last_year:
                urls.append((tweet.entities['urls'][0]))

    for url in urls:
        full_url = url[url_key]
        full_url = string.replace(full_url,medium,blog)
        tweet_text = text % full_url

        print tweet_text

        publish = input(user_query)

        if publish == yes:
            print before_publishing, tweet_text
            api.update_status(tweet_text)
            print after_publishing
        else:
            print not_publishing, tweet_text
get_last_year_tweets()
