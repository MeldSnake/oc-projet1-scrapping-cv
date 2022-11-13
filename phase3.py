
import pathlib
from typing import Iterable

from bs4 import BeautifulSoup
from requests import Session

import data
from phase2 import load_category, save_category


def load_categories_list(req_session: Session):
    """Extrait toutes les URLs des categories depuis le site de books.toscrap.com."""
    with req_session.get(data.BOOK_TO_SCRAPE_ROOT_URL) as response:
        if not response.ok or response.status_code != 200:
            categories: dict[str, str | None] = dict()
        else:
            doc = BeautifulSoup(response.content, 'html.parser')
            cat_links = [x for x in doc.select('.page .side_categories>ul>li>ul>li>a') if x is not None]
            categories = dict([(x.text.strip().lower(), x.attrs.get('href', '').strip()) for x in cat_links])
    return categories


def load_all_categories(categories: dict[str, str | None], req_session: Session):
    """
    Extrait toutes les catégories depuis la liste de catégorie donnée.
    :param catégories Contient un dictionnaire liant une catégorie à son URL.
    """
    for category_name, category_url in categories.items():
        if category_url is not None and category_url != '':
            category_url = data.get_full_url(category_url, data.BOOK_TO_SCRAPE_ROOT_URL)
            books = load_category(category_url, req_session)
            yield (category_name, books)


def save_all_categories(dest_folder: pathlib.Path, categories: Iterable[tuple[str, Iterable[data.BookData]]], req_session: Session, with_images: bool = False):
    """
    Charge toutes les catégories dans leurs fichiers respectifs.
    Optionnellement charge toutes les images de couvertures de chacun des livres dans un dossier respectif à leurs catégories.
    """
    for name, books in categories:
        save_category(dest_folder, name, books, req_session, with_images)


if __name__ == "__main__":
    with Session() as req_session:
        categories = load_categories_list(req_session)
        cat_books = load_all_categories(categories, req_session)
        dest_folder = pathlib.Path.cwd() / "output" / "phase3"
        save_all_categories(dest_folder, cat_books, req_session, False)
