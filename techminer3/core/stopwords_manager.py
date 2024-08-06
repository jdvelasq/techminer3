"""Stopwords Manager."""


class StopwordsManager:
    """Stopwords Manager."""

    file_path = "./my_keywords/stopwords.txt"

    def __init__(self):
        self.stopwords = self._load_stopwords()

    def _load_stopwords(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            stopwords = [line.strip() for line in f]
        return stopwords

    def _save_stopwords(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.stopwords))

    def sort_stopwords(self, reverse=False):
        """Sort stopwords."""
        self.stopwords = sorted(set(self.stopwords), reverse=reverse)
        self._save_stopwords()

    def add_term(self, term):
        """Add a term to stopwords."""
        if term not in self.stopwords:
            self.stopwords.append(term)
            self._save_stopwords()

    def get_stopwords(self):
        """Get stopwords."""
        return self.stopwords[:]
