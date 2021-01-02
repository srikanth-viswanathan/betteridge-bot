# Betteridge's Bot

[![Build Status](https://travis-ci.org/srikanth-viswanathan/betteridge-bot.svg?branch=master)](https://travis-ci.org/srikanth-viswanathan/betteridge-bot)

betteridge-bot is a bot that tries to honor Betteridge's Law by posting 'No' in response to headlines that are posed as questions. The output can be seen on twitter [here](https://twitter.com/betteridge_bot).


### Tech

This bot uses the awesome [python-twitter](https://pypi.python.org/pypi/twitter) library to get and post tweets.

### Running the bot

First, generate a credentials file using the `generate_credentials.py` script. Like so:

```
./generate_credentials.py --access_token yourtoken \
                          --access_token_secret yourtokensecret \
                          --consumer_key yourconsumerkey  \
                          --consumer_secret yourconsumersecret \
                          --output credentials.dat
```

Then, run the bot using the credentials file:
```
./bot.py -c credentials.dat
```

### Development

TBD

License
----

TBD
