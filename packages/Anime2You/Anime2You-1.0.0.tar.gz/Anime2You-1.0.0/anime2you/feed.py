from datetime import datetime
import re
from html.parser import HTMLParser

from typing import Dict, List


def _extract_image_url(html_string: str) -> str:
    pattern = '<img[^>]+src="([^">]+)"'
    match = re.search(pattern, html_string)
    if match:
        return match.group(1)
    else:
        raise ValueError("Could not extract the image url from html string")


def _extract_text_from_html(html_content: str) -> str:
    text = []

    class TextExtractor(HTMLParser):
        def handle_data(self, data):
            text.append(data)

    parser = TextExtractor()
    parser.feed(html_content)
    return ''.join(text).strip()


class Feed:

    def __init__(self, rss_item: Dict[str, any]):
        self._short_id = rss_item["id"].split("=")[1]
        self._id = rss_item["id"]
        self._link = rss_item["link"]
        self._title = rss_item["title"]
        self._description = _extract_text_from_html(rss_item["description"])
        self._published = datetime.strptime(rss_item["published"], '%a, %d %b %Y %H:%M:%S %z')
        self._image_url = _extract_image_url(rss_item["summary"])
        self._authors = [x["name"] for x in rss_item["authors"]]
        self._tags = [x["term"] for x in rss_item["tags"]]
        self._raw_rss_item = rss_item.copy()

    @property
    def short_id(self):
        return self._short_id

    @property
    def id(self):
        return self._id

    @property
    def link(self):
        return self._link

    @property
    def title(self):
        return self._title

    @property
    def description(self):
        return self._description

    @property
    def published(self):
        return self._published

    @property
    def image_url(self):
        return self._image_url

    @property
    def authors(self):
        return self._authors

    @property
    def tags(self):
        return self._tags

    @property
    def raw_rss_item(self):
        return self._raw_rss_item

    def __iter__(self):
        yield 'id', self._id
        yield 'link', self._link
        yield 'title', self._title
        yield 'description', self._description
        yield 'published', self._published
        yield 'image_url', self._image_url

    def to_dict(self):
        return dict(self)

    @staticmethod
    def load_feed(items: List[Dict[str, str]]) -> List['Feed']:
        feed_items: List['Feed'] = []
        for item in items:
            feed_items.append(Feed(item))
        return feed_items
