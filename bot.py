#!/usr/bin/env python3

import logging
import os
import shelve
import sys
from twitter import OAuth, Twitter


token = '908692479431421953-ZxEdzlXblAlQmhoeZRIAWDBVlyOGJLK'
token_secret = 'Kvjb6lRgoRLi3uMAqGYHZXoAptg0BNjpJ34yHdMgqiAiY'
consumer_key = 'PkFAE5amTwFrL5qtfeWhi3P7O'
consumer_secret = 'iuc2x07qFC4gN7W7OYMIe0hMn1bbjOtvVEF9Z7MMKXrIuY4IiR'

MAX_FETCH_SIZE = 500


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


def process_tweet(tweet):
    log = logging.getLogger(__name__)
    log.debug('Processing tweet: %s', tweet)
    if tweet['text'].endswith('?'):
        log.info('Would retweet: %s', tweet)


def process_batch(batch):
    with SinceDb() as since_db:
        # Process batch in reverse order
        for tweet in reversed(batch):
            id = tweet['id']
            process_tweet(tweet)
            since_db.set(id)


def main():
    logging.basicConfig(filename='bot.log',level=logging.DEBUG)
    log = logging.getLogger(__name__)
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    log.addHandler(stdout_handler)

    t = Twitter(
         auth=OAuth(token, token_secret, consumer_key, consumer_secret), retry=10)

    with SinceDb() as since_db:
        since_id = since_db.get()

        max_id = None
        full_batch = []
        while True:
            kwargs = {}
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
            if len(full_batch) > MAX_FETCH_SIZE:
                log.info('Ending batch fetch cycle because we hit max fetch size')
                break
            max_id = batch[0]['id'] - 1

        log.info('Full batch size: %d', len(full_batch))

    process_batch(full_batch)

if __name__ == '__main__':
    main()
