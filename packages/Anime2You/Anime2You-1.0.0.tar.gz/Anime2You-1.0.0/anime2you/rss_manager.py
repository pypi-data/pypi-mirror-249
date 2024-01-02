from datetime import datetime
from os import PathLike, path, makedirs
from typing import Union, List

import feedparser

from feed import Feed

_last_feed_date_file = "/a2y_last_feed_date.txt"


class RSSManager:
    FEED_COMPLETE = "https://www.anime2you.de/feed/"
    FEED_ARTICLES = "https://www.anime2you.de/news/feed/"
    FEED_STREAMS = "https://www.anime2you.de/video-on-demand/feed/"

    def __init__(self, feed_type: str = "https://www.anime2you.de/feed/", use_cache: bool = False, cache_path: Union[
        str, PathLike] = "./cache"):
        """
        :param feed_type:
        :param use_cache:
        :param cache_path:
        :param custom_functions:
        """
        assert feed_type in [
            RSSManager.FEED_COMPLETE,
            RSSManager.FEED_ARTICLES,
            RSSManager.FEED_STREAMS
        ], "Invalid feed type"

        self._feed_url = feed_type

        self._use_cache = use_cache
        self._cache_path = cache_path
        if use_cache:
            if not path.exists(self._cache_path):
                makedirs(self._cache_path)

    def get_feed(self) -> List[Feed]:
        """
        Get the current feed with all entries
        :return:
        """
        parsed = feedparser.parse(self._feed_url)
        feeds = Feed.load_feed(parsed.entries)
        if self.use_cache:
            self.set_cache_feed_published(feeds[0].published)
        return feeds

    def get_new_feed(self):
        """
        Get all new feed entries
        :return:
        """
        if not self.use_cache:
            return self.get_feed()

        newest_feed_published = self.get_cache_feed_published()
        feeds = self.get_feed()
        for feed in feeds.copy():
            if feed.published <= newest_feed_published:
                feeds.remove(feed)
        return feeds

    def set_cache_feed_published(self, date: datetime):
        """
        Need a datetime
        :param date:
        :return:
        """
        with open(self._cache_path + _last_feed_date_file, mode='w') as cf:
            cf.write(date.isoformat())

    def get_cache_feed_published(self) -> datetime:
        """
        Returns a valid datetime
        :return:
        """
        try:
            with open(self._cache_path + _last_feed_date_file, mode='r') as cf:
                return datetime.fromisoformat(cf.read())
        except FileNotFoundError:
            return datetime.fromisoformat("2000-01-01T00:00:00+00:00")

    @property
    def feed_url(self) -> str:
        return self._feed_url

    @property
    def use_cache(self) -> bool:
        return self._use_cache

    @property
    def cache_path(self) -> str:
        return self._cache_path
