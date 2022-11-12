from phase3 import load_all_categories
import pathlib


if __name__ == "__main__":
    books = load_all_categories(pathlib.Path.cwd(), True)
