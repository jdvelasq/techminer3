# pylint: disable=too-few-public-methods
"""
SummarySheet
===============================================================================


>>> from techminer3.tools import SummarySheet
>>> SummarySheet(
...     #
...     # DATABASE PARAMS:
...     root_dir="example/", 
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... ).df_.head()
                 column  number of terms coverage (%)
0     abbr_source_title               50         1.0%
1              abstract               48        0.96%
2  abstract_nlp_phrases               48        0.96%
3          affiliations               49        0.98%
4                art_no               50         1.0%

"""
import pandas as pd

from .._mixins.read_records import ReadRecordsMixin


class SummarySheet(ReadRecordsMixin):
    """:meta private:"""

    def __init__(
        self,
        #
        # DATABASE PARAMS:
        root_dir: str = "./",
        database: str = "main",
        year_filter: tuple = (None, None),
        cited_by_filter: tuple = (None, None),
        **filters,
    ):
        #
        # DATABASE PARAMS:
        self._root_dir = root_dir
        self._database = database
        self._year_filter = year_filter
        self._cited_by_filter = cited_by_filter
        self._filters = filters

        #
        # RUN:
        self.__post_init__()

    def __post_init__(self):
        #
        # DATABASE:
        database = self.read_records(
            root_dir=self._root_dir,
            database=self._database,
            year_filter=self._year_filter,
            cited_by_filter=self._cited_by_filter,
            **self._filters,
        )

        #
        # Compute stats per column
        columns = sorted(database.columns)

        n_documents = len(database)

        report = pd.DataFrame({"column": columns})

        report["number of terms"] = [
            n_documents - database[col].isnull().sum() for col in columns
        ]

        report["coverage (%)"] = [
            f"{(n_documents - database[col].isnull().sum()) / n_documents:5.2}%"
            for col in columns
        ]

        self.df_ = report
