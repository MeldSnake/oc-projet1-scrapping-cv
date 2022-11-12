import pathlib
import re

from bs4 import BeautifulSoup, Tag
from requests import Session

import data

AVAILABILITY_RE = re.compile(r'^.*\((?P<count>\d+) available\)')
PRICE_RE = re.compile(r'^.*?(?P<price_value>\d+(?:\.\d+)?)$')


def load_book_page(url: str | None, req_session: Session) -> data.BookData | None:
    url = data.get_full_url(url, None)
    if url is None:
        return None

    response = req_session.get(url)
    if not response.ok or response.status_code != 200:
        return None
    doc = BeautifulSoup(response.content, 'html.parser')

    breadcrumb = doc.select('body>.page>.page_inner ul.breadcrumb li')
    product_page = doc.select_one('body>.page>.page_inner article.product_page')

    book = data.BookData(**{})
    book["category"] = breadcrumb[-2].text.strip()
    cover_img = product_page.select_one('#product_gallery img[src]:not([src=""])')
    book['image_url'] = data.get_full_url(cover_img.attrs["src"].strip(), url) or ""
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
    if prod_desc is not None:
        book['product_description'] = prod_desc.find_next_sibling('p').text.strip()
    else:
        book['product_description'] = ''
    prod_info_table: Tag = product_page.select_one('table.table.table-striped')
    for row in prod_info_table.select('tr'):
        row_name = row.select_one('th').text.strip()
        row_value = row.select_one('td').text.strip()
        match row_name:
            case "UPC":
                book['universal_product_code (upc)'] = row_value
            case "Price (excl. tax)":
                book['price_excluding_tax'] = row_value
            case "Price (incl. tax)":
                book['price_including_tax'] = row_value
            case "Availability":
                if (match := AVAILABILITY_RE.match(row_value)) is not None:
                    book['number_available'] = int(match['count'])
                else:
                    book['number_available'] = 0
            case _:
                pass

    book['product_page_url'] = url
    return book


if __name__ == "__main__":
    import sys
    session = Session()
    if len(sys.argv) > 1:
        book = load_book_page(sys.argv[1], session)
        if book is not None:
            data.save_data_csv(pathlib.Path.cwd() / "output" / "phase1", f"{book['title']}-{book['universal_product_code (upc)']}", [book])
