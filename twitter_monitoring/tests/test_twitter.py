"""Testing Twitter modules."""
import json
import os
import unittest
from unittest.mock import MagicMock, patch

from twitter.stream_twitter_data import TweetStreamListener
from utils.custom_exceptions import TwitterInvalidCredentialsException

with patch.dict(
    os.environ,
    {
        "CONSUMER_KEY": "Testing_Consumer_Key",
        "CONSUMER_SECRET": "Testing_Consumer_Secret",
        "ACCESS_TOKEN": "Testing_Access_Token",
        "ACCESS_TOKEN_SECRET": "Testing_Access_Token_Secret",
    },
    clear=True,
):
    from twitter.twitter_authenticator import twitter_auth, create_api

tweet = {
    "created_at": "Wed Oct 10 20:19:24 +0000 2018",
    "id": "1050118621198921728",
    "id_str": "1050118621198921728",
    "text": "Testing str tweet text",
    "user": {"screen_name": "Testing screen name"},
    "entities": {},
    "retweeted": False,
}


class TestTwitterAuth(unittest.TestCase):
    """Testing Twitter Auth module."""

    def setUp(self):
        """SetUp."""
        pass

    @patch("twitter.twitter_authenticator.tweepy.OAuthHandler")
    def test_twitter_auth(self, mock_oauth_handler):
        """Twitter auth module test."""
        mock_oauth_handler.return_value.set_access_token = MagicMock()
        twitter_auth()

        mock_oauth_handler.assert_called_once_with(
            consumer_key="Testing_Consumer_Key",
            consumer_secret="Testing_Consumer_Secret",
        )
        mock_oauth_handler.return_value.set_access_token.assert_called_once_with(
            key="Testing_Access_Token", secret="Testing_Access_Token_Secret"
        )

    @patch("twitter.twitter_authenticator.twitter_auth")
    @patch("twitter.twitter_authenticator.tweepy.API")
    def test_create_unsuccessful_api(self, mock_API, mock_twitter_auth):
        """Twitter create api test."""
        mock_API.return_value.verify_credentials.return_value = False
        with self.assertRaises(TwitterInvalidCredentialsException) as ctx:
            create_api()

        self.assertTrue("Invalid credentials.", str(ctx.exception))
        mock_twitter_auth.assert_called_once()
        mock_API.assert_called_once()

    @patch("twitter.twitter_authenticator.twitter_auth")
    @patch("twitter.twitter_authenticator.tweepy.API")
    def test_create_successful_api(self, mock_API, mock_twitter_auth):
        """Twitter create api test."""
        mock_API.return_value.verify_credentials.return_value = True
        create_api()

        mock_twitter_auth.assert_called_once()
        mock_API.assert_called_once()


class TestStreamTwitterData(unittest.TestCase):
    """Testing Stream Twitter Data."""

    def setUp(self):
        """SetUp."""
        self.data_str = json.dumps(tweet)
        self.data = tweet

    @patch("twitter.stream_twitter_data.TweetStreamListener.search_match_in_tweet")
    def test_stream_non_retweeted_data(self, mock_search_match_in_tweet):
        """Testing non retweeted data."""
        TweetStreamListener().on_data(data=self.data_str)

        mock_search_match_in_tweet.assert_called_once_with(tweet=self.data)

    @patch("twitter.stream_twitter_data.TweetStreamListener.search_match_in_tweet")
    def test_stream_retweeted_data(self, mock_search_match_in_tweet):
        """Testing retweeted data."""
        self.data["text"] = "RT Testing retweeted text"
        TweetStreamListener().on_data(data=json.dumps(self.data))
        mock_search_match_in_tweet.assert_not_called()

        self.data["retweeted"] = True
        TweetStreamListener().on_data(data=json.dumps(self.data))
        mock_search_match_in_tweet.assert_not_called()

    @patch("twitter.stream_twitter_data.upload_to_dynamodb")
    @patch("twitter.stream_twitter_data.TweetStreamListener.format_tweet")
    @patch("twitter.stream_twitter_data.STRING_ALERT_NOT_ACTIVATED", "Testing str")
    def test_search_match_in_tweet(self, mock_format_tweet, mock_upload_to_dynamodb):
        """Testing search match in tweets."""
        self.data["text"] = "Testing str not activated."
        TweetStreamListener().search_match_in_tweet(tweet=self.data)

        mock_format_tweet.assert_called_once_with(
            tweet=self.data, tweet_text=self.data["text"]
        )
        mock_upload_to_dynamodb.assert_called_once()

    @patch("twitter.stream_twitter_data.STRING_ALERT_ACTIVATED", "Testing str")
    def test_format_tweet(self):
        """Testing format tweet."""
        expected_tweet = {
            "tweet_text": "Testing str tweet text",
            "id_str": "1050118621198921728",
            "user_screen_name": "Testing screen name",
            "created_at": "Wed Oct 10 20:19:24 +0000 2018",
            "alert_activated": True
        }
        formatted_tweet = TweetStreamListener().format_tweet(
            tweet=self.data, tweet_text=self.data["text"]
        )

        self.assertDictEqual(expected_tweet, formatted_tweet)


if __name__ == "__main__":
    unittest.main(verbosity=2)
