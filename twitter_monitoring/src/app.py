"""Lamnda handler of incoming twitter events."""
import os

from tweepy import Stream
from dotenv import load_dotenv

load_dotenv()

from twitter.stream_twitter_data import TweetStreamListener
from twitter.twitter_authenticator import twitter_auth

TWITTER_ACCOUNT_ID: str = os.getenv("TWITTER_ACCOUNT_ID")


def main() -> None:
    """Main function to be called.

    :return None.
    """
    print(f"Starting streaming tweets from user {TWITTER_ACCOUNT_ID}")
    # @SASMEX -> "135165642"
    stream = Stream(auth=twitter_auth(), listener=TweetStreamListener())
    stream.filter(follow=[TWITTER_ACCOUNT_ID])


if __name__ == "__main__":
    main()
