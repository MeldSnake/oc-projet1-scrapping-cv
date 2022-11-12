import re
from typing import LiteralString, TypedDict, NotRequired
from urllib.parse import ParseResult, urlparse, urljoin

BOOK_TO_SCRAPE_ROOT_URL: LiteralString = "http://books.toscrape.com/"
BOOK_TO_SCRAPE_ROOT = urlparse(BOOK_TO_SCRAPE_ROOT_URL)
PAGE_NUMBER_REGEXP = re.compile(r'^page-(?P<page>\d+).html$', re.IGNORECASE)


RATING_MAPPING = {
    "Zero": 0,
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}


class BookData(TypedDict):
    product_page_url: str
    universal_product_code: str
    title: str
    price_including_tax: float
    price_excluding_tax: float
    number_available: int
    product_description: str
    category: str
    review_rating: float
    image_url: str | None

    product_type: NotRequired[str | None]


def check_url_domain(url: str | ParseResult | None):
    if url is None:
        return False
    if isinstance(url, str):
        url = urlparse(url)
    return not bool(url.netloc) or url.netloc == BOOK_TO_SCRAPE_ROOT.netloc


def get_full_url(url: str | ParseResult | None):
    if url is not None:
        if isinstance(url, str):
            url_info = urlparse(url)
        else:
            url_info = url
        if bool(url_info.netloc):
            result = str(url)
        else:
            result = urljoin(BOOK_TO_SCRAPE_ROOT_URL, str(url))
        if check_url_domain(result):
            return result
    return None
