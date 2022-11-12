
from typing import TypedDict
from urllib.parse import ParseResult

import pathlib

from bs4 import BeautifulSoup
from requests import Session

import data
from phase2 import load_category


def load_all_categories(destination: pathlib.Path, with_images: bool):
    with Session() as req_session:
        with req_session.get(data.BOOK_TO_SCRAPE_ROOT_URL) as response:
            if not response.ok or response.status_code != 200:
                categories = []
            else:
                doc = BeautifulSoup(response.content, 'html.parser')
                categories = doc.select('.page .side_categories>ul>li>ul>li>a')
        dest_folder = destination / "output" / "phase3_4"
        for category in categories:
            if (href := category.attrs.get('href', '').strip()) != '':
                category_name = category.text.strip()
                category_url = data.get_full_url(href, data.BOOK_TO_SCRAPE_ROOT_URL)
                books, _ = load_category(category_url, req_session)
                data.save_data_csv(dest_folder, category_name, books)
                if with_images:
                    data.save_data_images(
                        dest_folder / data.slugify(category_name),
                        books,
                        req_session
                    )


if __name__ == "__main__":
    books = load_all_categories(pathlib.Path.cwd(), False)
