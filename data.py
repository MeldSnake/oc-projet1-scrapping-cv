from pathlib import Path
import re
import csv
from typing import LiteralString, TypedDict
from urllib.parse import ParseResult, urlparse, urljoin

import requests

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


def save_data_csv(directory: Path, filename: str, books: list[BookData], with_images: bool = False):
    filename = slugify(filename.removesuffix('.csv')) + '.csv'
    directory.mkdir(parents=True, exist_ok=True)
    if not directory.is_dir():
        return
    with open(directory / filename, mode="w", newline='', encoding='utf_8_sig') as fd:
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


def save_data_images(directory: Path, books: list[BookData], req_session: requests.Session):
    directory.mkdir(exist_ok=True)
    if not directory.is_dir():
        return
    for book in books:
        image_url = book['image_url']
        if image_url == '':
            continue
        image_url_info = urlparse(image_url)
        _, extension = image_url_info.path.rsplit('.', 1)
        with req_session.get(image_url) as response:
            if response.ok and response.status_code == 200:
                with open(directory / f"{book['universal_product_code (upc)']}.{extension}", 'wb') as img_fd:
                    for data in response.iter_content(8192):
                        img_fd.write(data)


def slugify(filename: str):
    filename = re.sub(r'[^\w\d\s-]', '', filename) \
        .strip() \
        .lower()
    filename = re.sub(r'[^\w\d]+', '-', filename)
    return filename
