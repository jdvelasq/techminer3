# pylint: disable=too-many-statements
# pylint: disable=too-many-locals
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-arguments
"""
Performance Metrics
===============================================================================

>>> from techminer3.metrics import PerformanceMetrics
>>> PerformanceMetrics(
...     #
...     # ITEMS PARAMS:
...     field='author_keywords',
...     metric='OCCGC',
...     #
...     # ITEM FILTERS:
...     top_n=20,
...     occ_range=(None, None),
...     gc_range=(None, None),
...     custom_items=None,
...     #
...     # DATABASE PARAMS:
...     root_dir="example/", 
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... ).df_.head()
                      rank_occ  rank_gcs  rank_lcs  ...  h_index  g_index  m_index
author_keywords                                     ...                           
FINTECH                      1         1         1  ...       31       12     7.75
INNOVATION                   2         2         2  ...        7        7     1.75
FINANCIAL_SERVICES           3         4        40  ...        4        4     1.00
FINANCIAL_INCLUSION          4         5         3  ...        3        3     0.75
FINANCIAL_TECHNOLOGY         5        15        41  ...        3        3     1.00
<BLANKLINE>
[5 rows x 9 columns]



>>> from techminer3.metrics import PerformanceMetrics
>>> PerformanceMetrics(
...     #
...     # ITEMS PARAMS:
...     field='author_keywords',
...     metric='OCCGC',
...     #
...     # ITEM FILTERS:
...     top_n=20,
...     occ_range=(None, None),
...     gc_range=(None, None),
...     custom_items=None,
...     #
...     # DATABASE PARAMS:
...     root_dir="example/", 
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... ).prompt()
Your task is ...



"""
import pandas as pd

from .._mixins.filtering import FilterMixin
from .._mixins.load_stopwords import StopwordsMixin
from .._mixins.metrics import MetricsMixin
from .._mixins.prompts import PromptMixin
from .._mixins.read_records import ReadRecordsMixin
from .._mixins.sorting import SortingIndicatorsMixin

MARKER_COLOR = "#7793a5"
MARKER_LINE_COLOR = "#465c6b"


class PerformanceMetrics(
    ReadRecordsMixin,
    PromptMixin,
    StopwordsMixin,
    SortingIndicatorsMixin,
    MetricsMixin,
    FilterMixin,
):
    """:meta private:"""

    def __init__(
        self,
        #
        # PERFORMANCE PARAMS:
        field,
        metric=None,
        #
        # ITEM FILTERS:
        top_n=None,
        occ_range=(None, None),
        gc_range=(None, None),
        custom_items=None,
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
        # PERFORMANCE PARAMS:
        self._field = field
        self._metric = metric
        #
        # ITEM FILTERS:
        self._top_n = top_n
        self._occ_range = occ_range
        self._gc_range = gc_range
        self._custom_items = custom_items

        #
        # RESULTS:
        self.df_: pd.DataFrame

        #
        # RUN:
        self.__post_init__()

    def __post_init__(self):
        #
        # DATABASE:
        records = self.read_records(
            root_dir=self._root_dir,
            database=self._database,
            year_filter=self._year_filter,
            cited_by_filter=self._cited_by_filter,
            **self._filters,
        )

        field = self._field

        global_indicators = self.global_metrics_by_field(
            field=field,
            records=records,
        )

        filtered_indicators = self.filter_indicators_by_items(
            indicators=global_indicators,
            metric=self._metric,
            #
            # ITEM FILTERS:
            top_n=self._top_n,
            occ_range=self._occ_range,
            gc_range=self._gc_range,
            custom_items=self._custom_items,
        )

        selected_indicators = self.select_columns(filtered_indicators)

        #
        # EXIT:
        #
        self.df_ = selected_indicators

    def select_columns(self, indicators):
        """:meta private:"""

        indicators = indicators.copy()

        if self._metric == "OCCGC":
            columns = [
                "rank_occ",
                "rank_gcs",
                "rank_lcs",
                "OCC",
                "global_citations",
                "local_citations",
                "h_index",
                "g_index",
                "m_index",
            ]

        if self._metric == "OCC":
            columns = [
                "rank_occ",
                "OCC",
                indicators.columns[4],
                indicators.columns[5],
                "growth_percentage",
            ]

        if self._metric in [
            "global_citations",
            "local_citations",
        ]:
            columns = [
                "rank_gcs",
                "rank_lcs",
                "global_citations",
                "local_citations",
                "global_citations_per_document",
                "local_citations_per_document",
                "global_citations_per_year",
            ]

        if self._metric in [
            "h_index",
            "g_index",
            "m_index",
        ]:
            columns = [
                "h_index",
                "g_index",
                "m_index",
            ]

        return indicators[columns]

    def prompt(self):
        """:meta private:"""

        if self._metric == "OCCGC":
            metric = "OCC"
        else:
            metric = self._metric

        main_text = (
            "Your task is to generate an analysis about the bibliometric indicators of the "
            f"'{self._field}' field in a scientific bibliography database. Summarize the "
            f"table below, sorted by the '{metric}' metric, and delimited by triple backticks, "
            "identifyany notable patterns, trends, or outliers in the data, and discuss their "
            "implications for the research field. Be sure to provide a concise summary "
            "of your findings in no more than 150 words. "
        )

        prompt = self.format_prompt_for_dataframes(
            main_text=main_text,
            df_text=self.df_.to_markdown(),
        )

        print(prompt)
