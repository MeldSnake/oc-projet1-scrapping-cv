import re
from typing import LiteralString, TypedDict, NotRequired

BOOK_TO_SCRAPE_URL: LiteralString = "http://books.toscrape.com/"
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
