"""Twitter search."""
from twitter.twitter_authenticator import create_api

api = create_api()


def twitter_search(q: str) -> None:
    """Searching Twitter data given a query string.

    :param: q: str: query string to search for.
    :return None
    """
    for tweet in api.search(q=q, lang="en", rpp=10):
        print(f"{tweet.user.name}:{tweet.text}")