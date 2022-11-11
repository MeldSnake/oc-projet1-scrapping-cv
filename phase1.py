import re
from typing import TypedDict

from bs4 import BeautifulSoup, Tag
from requests import Session

import data

# https://books.toscrape.com/catalogue/sharp-objects_997/index.html

AVAILABILITY_RE = re.compile(r'^.*\((?P<count>\d+) available\)')
PRICE_RE = re.compile(r'^.*?(?P<price_value>\d+(?:\.\d+)?)$')


def load_book_page(url: str, req_session: Session) -> data.BookData | None:
    response = req_session.get(url)
    if not response.ok or response.status_code != 200:
        return None
    doc = BeautifulSoup(response.text, 'html.parser')
    breadcrumb = doc.select('body>.page>.page_inner ul.breadcrumb li')
    product_page = doc.select_one('body>.page>.page_inner article.product_page')
    if product_page is None or len(breadcrumb) == 0:
        return None
    book = data.BookData(**{})
    book["category"] = breadcrumb[-2].text.strip()
    cover_img = product_page.select_one('#product_gallery img[src]:not([src=""])')
    book['image_url'] = cover_img.attrs["src"].strip()
    product_main = product_page.select_one(".product_main")
    book['title'] = product_main.select_one('h1').text.strip()
    rating_classes = product_main.select_one('.star-rating').attrs['class']
    rating: int = 0
    if rating_classes is None:
        rating = 0
    elif isinstance(rating_classes, str):
        rating = data.RATING_MAPPING.get(rating_classes, 0)
    else:
        for rating_class in rating_classes:
            rating = data.RATING_MAPPING.get(rating_class, rating)
    book['review_rating'] = rating
    prod_desc = product_page.select_one('#product_description')
    book['product_description'] = prod_desc.findNextSibling('p').text.strip()
    prod_info_table: Tag = prod_desc.findNextSibling('table')
    for row in prod_info_table.select('tr'):
        row_name = row.select_one('th').text.strip()
        row_value = row.select_one('td').text.strip()
        match row_name:
            case "UPC":
                book['universal_product_code'] = row_value
            case "Price (excl. tax)":
                if (match := PRICE_RE.match(row_value)) is not None:
                    book['price_excluding_tax'] = float(match['price_value'])
                else:
                    book['price_excluding_tax'] = 0.0
            case "Price (incl. tax)":
                if (match := PRICE_RE.match(row_value)) is not None:
                    book['price_including_tax'] = float(match['price_value'])
                else:
                    book['price_including_tax'] = 0.0
            case "Availability":
                if (match := AVAILABILITY_RE.match(row_value)) is not None:
                    book['number_available'] = int(match['count'])
                else:
                    book['number_available'] = 0
            case _:
                pass
    book['product_page_url'] = url
    return book
    # breadcrumb contains the category and the Title?

if __name__ == "__main__":
    import sys
    session = Session()
    if len(sys.argv) > 1:
        book = load_book_page(sys.argv[1], session)
    else:
        book = load_book_page("https://books.toscrape.com/catalogue/sharp-objects_997/index.html", session)
    print(book)