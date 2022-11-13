import pathlib

from requests import Session

import phase3

if __name__ == "__main__":
    with Session() as req_session:
        categories = phase3.load_categories_list(req_session)
        cat_books = phase3.load_all_categories(categories, req_session)
        dest_folder = pathlib.Path.cwd() / "output" / "phase4"
        phase3.save_all_categories(dest_folder, cat_books, req_session, True)
