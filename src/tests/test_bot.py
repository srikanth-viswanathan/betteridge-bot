from .. import bot
import json
import unittest

class TestBot(unittest.TestCase):
    def test_process_one_tweet(self):
        test_tweet = '''{
    "favorite_count": 9,
    "source": "<a href=\\"https://www.sprinklr.com\\" rel=\\"nofollow\\">Sprinklr</a>",
    "favorited": false,
    "is_quote_status": false,
    "contributors": null,
    "in_reply_to_user_id": null,
    "text": "Would you like to take a ride in this? https://t.co/1xsNa8lztL",
    "in_reply_to_status_id_str": null,
    "truncated": false,
    "possibly_sensitive_appealable": false,
    "in_reply_to_screen_name": null,
    "retweeted": false,
    "created_at": "Sat Sep 16 22:33:00 +0000 2017",
    "id_str": "909183363675717632",
    "id": 909183363675717632,
    "retweet_count": 7,
    "geo": null,
    "coordinates": null,
    "entities": {
        "symbols": [],
        "user_mentions": [],
        "urls": [
            {
                "display_url": "thetim.es/2xpW83U",
                "expanded_url": "http://thetim.es/2xpW83U",
                "indices": [
                    39,
                    62
                ],
                "url": "https://t.co/1xsNa8lztL"
            }
        ],
        "hashtags": []
    },
    "in_reply_to_status_id": null,
    "user": {
        "translator_type": "none",
        "is_translation_enabled": false,
        "statuses_count": 156536,
        "profile_text_color": "000000",
        "url": "http://t.co/GAsNZkMcoP",
        "following": true,
        "name": "The Times of London",
        "friends_count": 664,
        "geo_enabled": true,
        "profile_sidebar_fill_color": "FFFFFF",
        "description": "The best of our journalism.\\nSubscribe here: https://t.co/Kq4ItERnQC\\nSpeak to our customer service team: https://t.co/VIDSflmdIL",
        "protected": false,
        "has_extended_profile": false,
        "profile_use_background_image": true,
        "profile_sidebar_border_color": "FFFFFF",
        "profile_background_tile": true,
        "default_profile": false,
        "location": "London",
        "is_translator": false,
        "profile_image_url": "http://pbs.twimg.com/profile_images/881879546101891073/KoNl5qpa_normal.jpg",
        "notifications": false,
        "profile_background_image_url_https": "https://pbs.twimg.com/profile_background_images/787983049/045c3fadaacbb35147cac3fa14bbda6d.png",
        "created_at": "Thu May 17 13:35:19 +0000 2007",
        "listed_count": 9063,
        "id": 6107422,
        "default_profile_image": false,
        "profile_link_color": "000000",
        "profile_banner_url": "https://pbs.twimg.com/profile_banners/6107422/1421312022",
        "profile_background_color": "EFEFEF",
        "entities": {
            "description": {
                "urls": [
                    {
                        "display_url": "thetim.es/subscribe",
                        "expanded_url": "http://thetim.es/subscribe",
                        "indices": [
                            44,
                            67
                        ],
                        "url": "https://t.co/Kq4ItERnQC"
                    },
                    {
                        "display_url": "thetimes.co.uk/livechat",
                        "expanded_url": "http://thetimes.co.uk/livechat",
                        "indices": [
                            104,
                            127
                        ],
                        "url": "https://t.co/VIDSflmdIL"
                    }
                ]
            },
            "url": {
                "urls": [
                    {
                        "display_url": "thetimes.co.uk",
                        "expanded_url": "http://www.thetimes.co.uk",
                        "indices": [
                            0,
                            22
                        ],
                        "url": "http://t.co/GAsNZkMcoP"
                    }
                ]
            }
        },
        "id_str": "6107422",
        "contributors_enabled": false,
        "follow_request_sent": false,
        "followers_count": 1034056,
        "time_zone": "London",
        "screen_name": "thetimes",
        "utc_offset": 3600,
        "profile_image_url_https": "https://pbs.twimg.com/profile_images/881879546101891073/KoNl5qpa_normal.jpg",
        "profile_background_image_url": "http://pbs.twimg.com/profile_background_images/787983049/045c3fadaacbb35147cac3fa14bbda6d.png",
        "lang": "en",
        "favourites_count": 1740,
        "verified": true
    },
    "possibly_sensitive": false,
    "in_reply_to_user_id_str": null,
    "place": null,
    "lang": "en"
}'''
        self.assertTrue(bot.App.should_retweet(json.loads(test_tweet)))


