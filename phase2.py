import pathlib
from typing import Iterable

from bs4 import BeautifulSoup
from requests import Session

import data
from phase1 import load_book_page


def load_category_page(url: str | None, req_session: Session, indent=0):
    """
    Extrait tous les livres présents sur une seule page d'une catégorie,
    le nom de la catégorie en cours et l'URL d'une page suivante si disponible.
    """
    print('\t'*indent, '-> ', url)
    books: list[data.BookData] = []
    url = data.get_full_url(url, None)
    if url is None:
        return None

    response = req_session.get(url)
    if not response.ok or response.status_code != 200:
        return None
    doc = BeautifulSoup(response.content, 'html.parser')

    category_name = doc.select_one('body>.page>.page_inner .page-header>h1').text.strip()
    section = doc.select_one('body>.page>.page_inner section')
    if section is None:
        return None

    articles = section.select('article.product_pod')
    for article in articles:
        links = article.select('a[href]:not([href=""])')
        if len(links) != 0:
            book = load_book_page(
                data.get_full_url(links[0].attrs["href"].strip(), url),
                req_session, indent=indent+1
            )
            if book is not None:
                books.append(book)

    next_page = section.select_one('ul.pager li.next a[href]:not([href=""])')
    if next_page is not None:
        next_page_url = data.get_full_url(next_page.attrs['href'].strip(), url)
    else:
        next_page_url = None
    return (books, category_name, next_page_url)


def load_category(url: str | None, req_session: Session, indent: int = 0):
    """Extrait tous les livres présent dans une seule catégorie."""
    print('\t'*indent, 'Traitement de la categorie:', sep='')
    count = 0
    category_name = None
    while (res := load_category_page(url, req_session, indent=indent)) is not None:
        books, category_name, url = res
        for book in books:
            count += 1
            yield book
    print('\t'*indent, 'Categorie ', category_name, ' traiter, ', count, ' livres trouvé.', sep='')


def save_category(destination: pathlib.Path, category_name: str, books: Iterable[data.BookData], req_session: Session, with_images: bool = False):
    """Charge les livres dans un fichier CSV."""
    books = list(books)
    data.save_data_csv(destination, category_name, books)
    if with_images:
        print("Extraction des couvertures...")
        data.save_data_images(destination, books, req_session)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with Session() as session:
            books = list(load_category(sys.argv[1], session))
            if len(books) > 0:
                category_name = books[0]['category'].capitalize()
            else:
                category_name = "unknown"
            save_category(pathlib.Path.cwd() / "output" / "phase2", category_name, books, session)
