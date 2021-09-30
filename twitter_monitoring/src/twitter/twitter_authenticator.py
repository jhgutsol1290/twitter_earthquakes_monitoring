"""Twitter authenticator module."""
import logging
import os

import tweepy
from utils.custom_exceptions import TwitterInvalidCredentialsException

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

CONSUMER_KEY: str = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET: str = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN: str = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET: str = os.environ.get("ACCESS_TOKEN_SECRET")


def create_api() -> tweepy.API:
    """Create twitter API client.

    :return tweepy.API client.
    :raises TwitterInvalidCredentialsException: Invalid twitter credentials.
    """
    auth = twitter_auth()
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    if not api.verify_credentials():
        logger.error("Invalid credentials")
        raise TwitterInvalidCredentialsException("Invalid credentials. Verify them")
    logger.info("API client created successfully")
    return api


def twitter_auth() -> tweepy.OAuthHandler:
    """Auth to twitter.

    return Twitter authenticator tweepy.OAuthHandler
    """
    logger.info("Authenticating to Twitter")
    auth = tweepy.OAuthHandler(
        consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET
    )
    auth.set_access_token(key=ACCESS_TOKEN, secret=ACCESS_TOKEN_SECRET)
    
    return auth
