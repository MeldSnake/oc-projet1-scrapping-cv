import re
import csv
from os import PathLike
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


BookData = TypedDict('BookData', {
    'product_page_url': str,
    'universal_product_code (upc)': str,
    'title': str,
    'price_including_tax': str,
    'price_excluding_tax': str,
    'number_available': int,
    'product_description': str,
    'category': str,
    'review_rating': float,
    'image_url': str,
})


def check_url_domain(url: str | ParseResult):
    if isinstance(url, str):
        url = urlparse(url)
    return url.netloc != ''


def get_full_url(url: str | ParseResult | None, parent_url: str | ParseResult | None):
    if isinstance(parent_url, str):
        parent_url = urlparse(parent_url)
    if url is not None:
        if isinstance(url, str):
            url_info = urlparse(url)
        else:
            url_info = url
        if bool(url_info.netloc):
            result = url_info.geturl()
        else:
            if parent_url is None:
                parent_url = BOOK_TO_SCRAPE_ROOT
            result = urljoin(parent_url.geturl(), url_info.geturl())
        if check_url_domain(result):
            return result
    return None


def write_csv(filepath: str, books: list[BookData]):
    with open(filepath, mode="w", newline='', encoding='utf_8_sig') as fd:
        csv_writer = csv.DictWriter(fd, fieldnames=[
            'product_page_url',
            'universal_product_code (upc)',
            'title',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'product_description',
            'category',
            'review_rating',
            'image_url',
        ])
        csv_writer.writeheader()
        csv_writer.writerows(books)
