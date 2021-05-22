from sys import stderr
import schedule as sch
import requests as rq
import tweepy as tw
import asyncio

from .secrets import hijacked_tweet
from datetime.date import today
from time import time as now

async def daily():
    try:
        r = rq.get("http://localhost:5000/load")
        res = "DONE" if r.ok else "ERR!"
        print(f"Reload... [{res}]", file=stderr)

async def hourly():
    try:
        r = rq.get("http://localhost:5000/talk").raw
        if r.ok:
            api.update_status(sms.raw)
            print(f'tweeted:\n\t{sms.raw}' , file=stederr)
    except Exception as e:
        print(e, file=stderr)

if __name__=="__main__":
    auth = tweepy.OAuthHandler(hijacked_tweet.api_token.access, hijacked_tweet.api_token.secret)
    api = tweepy.API(auth)
    auth.set_access_token(hijacked_tweet.user.access], hijacked_tweet.user.secret])

    # Who am I
    print(f"Account ID: " + str(api.me()._json['id']),   file=stderr)
    print(f"Username:   " + str(api.me()._json['name']), file=stderr)

    while true:
        if last_date < today():
            last_date = today()
            asyncio.create_task(daily)
        delta = now() - last_time
        if delta >= 3600:
            last_time = now()
            asyncio.create_task(hourly)
        sleep(3600 - delta)
