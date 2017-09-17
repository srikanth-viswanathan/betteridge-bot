Betteridge's Bot

betteridge-bot is a bot that tries to honor Betterige's Law by posting 'No' in response to headlines that are posed as questions. The output can be seen on twitter (here)[https://twitter.com/betteridge_bot]


### Tech

This bot uses the awesome (python-twitter)[https://pypi.python.org/pypi/twitter] library to get and post tweets.

### Running the bot

First, generate a credentials file using the `generate_credentials.py` script. Like so:
```
./generate_credentials.py --access_token yourtoken \
                          --access_token_key yourtokenkey \
                          --consumer_key yourconsumerkey  \
                          --consumer_seret yourconsumersecret \
                          --output credentials.dat

Then, run the bot using the credentials file:
./bot.py -c credentials.dat

### Development

TBD

### Todos

 - Write MORE Tests
 - Add additional parsing of twitter cards so we can parse beyond just the tweet text

License
----

TBD
