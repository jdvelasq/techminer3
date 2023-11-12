"""Mixin functions to load stopwords."""

import os

import pkg_resources


class StopwordsMixin:
    """Mixin class for stopwords management."""

    def load_user_stopwords(self):
        """:meta private:"""

        stopwords_file_path = os.path.join(self._root_dir, "my_keywords/stopwords.txt")

        if not os.path.isfile(stopwords_file_path):
            raise FileNotFoundError(f"The file '{stopwords_file_path}' does not exist.")

        with open(stopwords_file_path, "r", encoding="utf-8") as file:
            stopwords = [line.strip() for line in file.readlines()]

        return stopwords

    def load_package_stopwords(self):
        """:meta private:"""

        file_path = pkg_resources.resource_filename(
            "techminer2", "word_lists/stopwords.txt"
        )
        with open(file_path, "r", encoding="utf-8") as file:
            stopwords = file.read().split("\n")
        stopwords = [w.strip() for w in stopwords]
        stopwords = [w for w in stopwords if w != ""]
        return stopwords
