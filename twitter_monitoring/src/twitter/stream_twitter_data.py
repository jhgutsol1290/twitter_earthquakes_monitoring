"""Streaming twitter data."""
import json
from typing import Dict

from aws_utils.dynamodb import upload_to_dynamodb
from tweepy.streaming import StreamListener

STRING_ALERT_NOT_ACTIVATED: str = "NO AMERITÓ ALERTA SÍSMICA"
# STRING_ALERT_ACTIVATED = "#TenemosSismo, se activó la #AlertaSismica"
STRING_ALERT_ACTIVATED: str = "#Python is the best programming language"


class TweetStreamListener(StreamListener):
    """Class to liste stream Twitter data."""

    def on_data(self, data: str) -> None:
        """Raw data received from Twitter.

        :param: data: str: Streamed tweet.
        :return None.
        """
        tweet = json.loads(data)
        try:
            if not tweet["retweeted"] and not tweet["text"].startswith("RT"):
                self.search_match_in_tweet(tweet=tweet)
        except (AttributeError, Exception) as e:
            print("Exception found", e)

    def on_error(self, status):
        """Error handler."""
        print(status)

    def search_match_in_tweet(self, tweet: Dict) -> None:
        """If match exists in tweet text, uploads to DyanmoDB.

        :param: tweet: Dict: Tweet streamed by a user.
        :return None
        """
        tweet_text = (
            tweet.get("extended_tweet", {}).get("full_text", "")
            if "extended_tweet" in tweet.keys()
            else tweet.get("text", "")
        )
        if (
            STRING_ALERT_NOT_ACTIVATED in tweet_text
            or STRING_ALERT_ACTIVATED in tweet_text
        ):
            upload_to_dynamodb(
                tweet=self.format_tweet(tweet=tweet, tweet_text=tweet_text)
            )

    @staticmethod
    def format_tweet(tweet: Dict, tweet_text: str) -> Dict:
        """Format tweet to be saved into DynamoDB.

        :param: tweet: Dict: Filtered tweet.
        :param: tweet_text: str: Text of the tweet, either extended or normal.
        :return Dict: formatted tweet.
        """
        return {
            "tweet_text": tweet_text,
            "id_str": tweet.get("id_str"),
            "user_screen_name": tweet.get("user", {}).get("screen_name", None),
            "created_at": tweet.get("created_at"),
        }
