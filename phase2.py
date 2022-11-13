import pathlib

from bs4 import BeautifulSoup
from requests import Session

import data
from phase1 import load_book_page


def load_category_page(url: str | None, req_session: Session):
    """
    Extrait tous les livres present sur une seule page d'une categorie,
    le nom de la categorie en cours,
    et l'URL d'une page suivante si disponible
    """
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
                req_session
            )
            if book is not None:
                books.append(book)

    next_page = section.select_one('ul.pager li.next a[href]:not([href=""])')
    if next_page is not None:
        next_page_url = data.get_full_url(next_page.attrs['href'].strip(), url)
    else:
        next_page_url = None
    return (books, category_name, next_page_url)


def load_category(url: str | None, req_session: Session):
    """Extrait tous les livres present dans une seule categorie."""
    all_books: list[data.BookData] = []
    category_name = None
    while (res := load_category_page(url, req_session)) is not None:
        books, category_name, url = res
        all_books.extend(books)
    return all_books, category_name


def save_category(destination: pathlib.Path, category_name: str, books: list[data.BookData], req_session: Session, with_images: bool = False):
    """Charge les livres dans un fichier CSV."""
    data.save_data_csv(destination, category_name, books)
    if with_images:
        data.save_data_images(destination / data.slugify(category_name.removesuffix('.csv')), books, req_session)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        with Session() as session:
            books, category_name = load_category(sys.argv[1], session)
            save_category(pathlib.Path.cwd() / "output" / "phase2", category_name or "unknown", books, session)
