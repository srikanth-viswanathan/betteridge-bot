#!/usr/bin/env python3
import argparse
import shelve

def main():
    parser = argparse.ArgumentParser('Generate shelve file for twitter application credentials')
    parser.add_argument('--consumer_key', required=True)         # What user are you?
    parser.add_argument('--consumer_secret', required=True)      # Prove you are that user
    parser.add_argument('--access_token', required=True)         # What app are you?
    parser.add_argument('--access_token_secret', required=True)  # Prove you are that app
    parser.add_argument('-o', '--output', required=True, help='File to store these credentials in')
    args = parser.parse_args()
    with shelve.open(args.output) as out:
        out['consumer_key']        = args.consumer_key
        out['consumer_secret']     = args.consumer_secret
        out['access_token']        = args.access_token
        out['access_token_secret'] = args.access_token_secret

    print('Wrote credentials to {}'.format(args.output))


if __name__ == '__main__':
    main()