#!/usr/bin/env python3

import json
import logging
import os
import re
import shelve
import sys
from twitter import OAuth, Twitter


token = '908692479431421953-ZxEdzlXblAlQmhoeZRIAWDBVlyOGJLK'
token_secret = 'Kvjb6lRgoRLi3uMAqGYHZXoAptg0BNjpJ34yHdMgqiAiY'
consumer_key = 'PkFAE5amTwFrL5qtfeWhi3P7O'
consumer_secret = 'iuc2x07qFC4gN7W7OYMIe0hMn1bbjOtvVEF9Z7MMKXrIuY4IiR'

BOT_NAME = 'betteridge_bot'
MAX_BATCH_SIZE = 800

t = Twitter(
         auth=OAuth(token, token_secret, consumer_key, consumer_secret), retry=10)


class SinceDbError(Exception):
    pass


class SinceDb():
    def __init__(self, filename='since_db'):
        self.filename = os.path.abspath(filename)
        self.log = logging.getLogger(__name__)
        self.db = None
        self.log.info('Using %s as since db file', self.filename)

    def __enter__(self):
        self.db = shelve.open(self.filename)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def get(self):
        try:
            return int(self.db['since_id'])
        except KeyError:
            self.log.warning('No since_id found.')
            return None
        except ValueError:
            msg = 'Invalid since_id: {}'.format(self.db['since_id'])
            self.log.error(msg)
            raise SinceDbError(msg)

    def set(self, since_id):
        self.db['since_id'] = since_id


def should_retweet(tweet):
    log = logging.getLogger(__name__)
    if tweet['user']['screen_name'] == BOT_NAME:
        log.debug('Skipping own tweet: %s', json.dumps(tweet))
        return False

    log.debug('Processing tweet: %s', json.dumps(tweet))
    tweet_text = tweet['text']
    for url in tweet['entities']['urls']:
        tweet_text = tweet['text'].replace(url['url'], '').strip()

    log.debug('tweet_text: %s', tweet_text)

    possible_beginnings = ('is', 'are', 'could', 'would', 'should', 'will')
    if tweet_text.endswith('?'):
        parts = re.split('\.|:|;', tweet_text)
        log.debug(parts)
        last_part = parts[-1]
        log.debug('last part: %s', last_part)
        if last_part.endswith('?') and str.lower(last_part).startswith(possible_beginnings):
            log.info('Should retweet: %s', tweet)
            return True

    log.debug('Won\'t retweet: %s', tweet)
    return False


def retweet(tweet):
    link = 'https://twitter.com/{screen_name}/status/{id}'.format(
        screen_name=tweet['user']['screen_name'],
        id=tweet['id']
    )
    t.statuses.update


def process_batch(batch):
    log = logging.getLogger(__name__)
    retweeted = 0
    with SinceDb() as since_db:
        # Process batch in reverse order
        for tweet in reversed(batch):
            id = tweet['id']
            if should_retweet(tweet):
                retweet(tweet)
                retweeted += 1

            since_db.set(id)

    log.info('Retweeted %d tweets', retweeted)


def main():
    logging.basicConfig(filename='bot.log',level=logging.DEBUG)
    log = logging.getLogger(__name__)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    log.addHandler(stdout_handler)

    with SinceDb() as since_db:
        since_id = since_db.get()

        max_id = None
        full_batch = []
        while True:
            kwargs = {'count': 200}
            if since_id:
                kwargs['since_id'] = since_id
            if max_id:
                kwargs['max_id'] = max_id

            batch = t.statuses.home_timeline(**kwargs)
            returned = len(batch)
            log.info('Got %d tweets', returned)
            if not returned:
                log.info('Ending batch fetch cycle')
                break

            full_batch.extend(batch)
            if len(full_batch) > MAX_BATCH_SIZE:
                log.info('Ending batch fetch cycle because we hit max fetch size %d', MAX_BATCH_SIZE)
                break

            max_id = batch[-1]['id'] - 1
            log.info('max_id is now: %s', max_id)

        log.info('Full batch size: %d', len(full_batch))

    process_batch(full_batch)

if __name__ == '__main__':
    main()
