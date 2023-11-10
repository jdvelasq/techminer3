# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
# pylint: disable=unused-variable
"""
Query
===============================================================================

>>> from techminer3.tools import Query
>>> Query(  
...     expr="SELECT source_title FROM database LIMIT 5;",
...     #
...     # DATABASE PARAMS:
...     root_dir="example/",
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... ).df_
                                      source_title
0                      Review of Financial Studies
1  International Journal of Information Management
2                             Financial Innovation
3                           China Economic Journal
4                Journal of Economics and Business



"""
import duckdb
import pandas as pd

from .._mixins.read_records import ReadRecordsMixin


class Query(ReadRecordsMixin):
    """:meta private:"""

    def __init__(
        self,
        #
        # QUERY:
        expr: str,
        #
        # DATABASE PARAMS:
        root_dir: str = "./",
        database: str = "main",
        year_filter: tuple = (None, None),
        cited_by_filter: tuple = (None, None),
        **filters,
    ):
        #
        # QUERY:
        self._expr = expr

        #
        # DATABASE PARAMS:
        self._root_dir = root_dir
        self._database = database
        self._year_filter = year_filter
        self._cited_by_filter = cited_by_filter
        self._filters = filters

        #
        # RESULTS:
        self.df_: pd.DataFrame = pd.DataFrame()

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

        self.df_ = duckdb.query(self._expr).df()
