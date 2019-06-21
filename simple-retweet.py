import tweepy,datetime,json,string,requests,sys
from datetime import date
from config import *
import xml.etree.cElementTree as ET

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


def get_last_year_tweets(years):
    print years
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API(auth)
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    same_day_last_year = add_years(today,years)
    tomorrow_last_year = add_days(same_day_last_year,days)
    print same_day_last_year, tomorrow_last_year

    urls = []
    limited_tweets = api.user_timeline(screen_name = username, count = 200)
    print("Last Tweet @", limited_tweets[-1].created_at, " - in initial pull")
    for tweet in limited_tweets:
        if tweet.created_at < tomorrow_last_year and tweet.created_at > same_day_last_year:
            urls.append((tweet.entities['urls'][0]))


    while (limited_tweets[-1].created_at > same_day_last_year):
        print("Last Tweet @", limited_tweets[-1].created_at, " - fetching some more")
        limited_tweets = api.user_timeline(screen_name = username, max_id = limited_tweets[-1].id, count = 200)
        for tweet in limited_tweets:
            if tweet.created_at < tomorrow_last_year and tweet.created_at > same_day_last_year:
                urls.append((tweet.entities['urls'][0]))
    count = 1
    for url in urls:
        full_url = url[url_key]
        full_url = string.replace(full_url,medium,blog)
        publish_tweet(api,full_url,count)
        count = count + 1


def publish_tweet(api,url,count):
    if count == 1:
        tweet_text = text % url
    else:
        tweet_text = multi_text % url

    print tweet_text
    publish = input(user_query)

    if publish == yes:
        print before_publishing
        api.update_status(tweet_text)
        print after_publishing
    else:
        print not_publishing

def convert_date(date):
    return date.split('T')[0]

def get_past_posts(years):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)

    api = tweepy.API(auth)
    url = blog + sitemap
    resp = requests.get(url)
    xml = resp.content
    today = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    same_day_last_year = str(add_years(today,years)).split(" ")[0]
    print same_day_last_year

    root = ET.fromstring(xml)
    print root.tag

    count = 1
    for url in root.iter(namespace + url_str):
        lastmod =  url.find(namespace + lastmod_str)
        loc = url.find(namespace + loc_str)
        if lastmod != None:
            post_date =  lastmod.text
            correct_format = convert_date(post_date)
            if correct_format == same_day_last_year:
                publish_tweet(api,loc.text,count)
                count = count + 1

def simple_retweet():
    current_year = -1
    while current_year >= no_of_years:
        if mode_twitter:
            get_last_year_tweets(current_year)
        else:
            get_past_posts(current_year)
            current_year = current_year - 1

simple_retweet()
