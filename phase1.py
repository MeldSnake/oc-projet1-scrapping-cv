import pathlib
import re

from bs4 import BeautifulSoup, Tag
from requests import Session

import data

AVAILABILITY_RE = re.compile(r'^.*\((?P<count>\d+) available\)')
"""Expression reguliere permettant d'extraire le nombre de produit disponible."""


def load_book_page(url: str | None, req_session: Session, indent: int = 0) -> data.BookData | None:
    """
    Extrait les données de la page d'un livre et les restituent dans un dictionnaire.
    """
    url = data.get_full_url(url, None)
    if url is None:
        return None

    print('\t'*indent, 'Traitement du livre: ', url, ' ... ', sep='', end='')
    response = req_session.get(url)
    if not response.ok or response.status_code != 200:
        print('Echec')
        print('\t'*indent, 'Livre non traiter: ', response.reason, sep='')
        return None
    print('Succès')
    doc = BeautifulSoup(response.content, 'html.parser')

    breadcrumb = doc.select('body>.page>.page_inner ul.breadcrumb li')
    product_page = doc.select_one('body>.page>.page_inner article.product_page')

    book = data.BookData(**{})
    book["category"] = breadcrumb[-2].text.strip().lower()
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
    _, cover_extension = book['image_url'].rsplit('.', 1)
    book['image_path'] = str(pathlib.Path(book['category']) / data.slugify_book_name(book)) + '.' + cover_extension.lower()
    return book


def save_single_book(destination: pathlib.Path, book: data.BookData | None):
    """Charge un seul livre dans son propre fichier CSV."""
    if book is not None:
        data.save_data_csv(destination, data.slugify_book_name(book), [book])


if __name__ == "__main__":
    import sys
    session = Session()
    if len(sys.argv) > 1:
        book = load_book_page(sys.argv[1], session)
        save_single_book(pathlib.Path.cwd() / "output" / "phase1", book)
