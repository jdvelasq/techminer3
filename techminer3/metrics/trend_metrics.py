# flake8: noqa
# pylint: disable=invalid-name
# pylint: disable=line-too-long
# pylint: disable=missing-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-locals
"""
Trend Metrics
===============================================================================


>>> from techminer3.metrics import TrendMetrics
>>> TrendMetrics(
...     #
...     # DATABASE PARAMS:
...     root_dir="example/", 
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... ).df_
      OCC  cum_OCC  ...  cum_local_citations  mean_local_citations_per_year
year                ...                                                    
2015    1        1  ...                  4.0                           0.80
2016    7        8  ...                 12.0                           0.29
2017   10       18  ...                 23.0                           0.37
2018   17       35  ...                 37.0                           0.41
2019   15       50  ...                 38.0                           0.07
<BLANKLINE>
[5 rows x 11 columns]

>>> from techminer3.metrics import TrendMetrics
>>> TrendMetrics(
...     #
...     # DATABASE PARAMS:
...     root_dir="example/", 
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... ).plot(
...     #
...     # CHART PARAMS:
...     metric_to_plot="OCC",
...     auxiliary_metric_to_plot=None,
...     title="Annual Scientific Production",
...     year_label=None,
...     metric_label=None,
...     textfont_size=10,
...     marker_size=7,
...     line_width=1.5,
...     yshift=4,
... ).write_html("sphinx/_static/metrics/trend_metrics.html")

.. raw:: html

    <iframe src="../_static/metrics/trend_metrics.html"  
    height="600px" width="100%" frameBorder="0"></iframe>



>>> from techminer3.metrics import TrendMetrics
>>> TrendMetrics( 
...     #
...     # DATABASE PARAMS:
...     root_dir="example/", 
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... ).prompt() # doctest: +SKIP
Your task is ... 



"""


import pandas as pd
import plotly.express as px

from .._mixins.prompts import PromptMixin
from .._mixins.read_records import ReadRecordsMixin

MARKER_COLOR = "#7793a5"
MARKER_LINE_COLOR = "#465c6b"


class TrendMetrics(
    ReadRecordsMixin,
    PromptMixin,
):
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

        #
        # COMPUTE METRICS:

        records = records.assign(OCC=1)

        columns = ["OCC", "year"]

        if "local_citations" in records.columns:
            columns.append("local_citations")
        if "global_citations" in records.columns:
            columns.append("global_citations")
        records = records[columns]

        records["year"] = records["year"].astype(int)
        records = records.groupby("year", as_index=True).sum()
        records = records.sort_index(ascending=True, axis=0)
        records = records.assign(cum_OCC=records.OCC.cumsum())
        records.insert(1, "cum_OCC", records.pop("cum_OCC"))

        current_year = records.index.max()
        records = records.assign(citable_years=current_year - records.index + 1)

        if "global_citations" in records.columns:
            records = records.assign(
                mean_global_citations=records.global_citations / records.OCC
            )
            records = records.assign(
                cum_global_citations=records.global_citations.cumsum()
            )
            records = records.assign(
                mean_global_citations_per_year=records.mean_global_citations
                / records.citable_years
            )
            records.mean_global_citations_per_year = (
                records.mean_global_citations_per_year.round(2)
            )

        if "local_citations" in records.columns:
            records = records.assign(
                mean_local_citations=records.local_citations / records.OCC
            )
            records = records.assign(
                cum_local_citations=records.local_citations.cumsum()
            )
            records = records.assign(
                mean_local_citations_per_year=records.mean_local_citations
                / records.citable_years
            )
            records.mean_local_citations_per_year = (
                records.mean_local_citations_per_year.round(2)
            )

        self.df_ = records

    def plot(
        self,
        #
        # CHART PARAMS:
        metric_to_plot: str = "OCC",
        auxiliary_metric_to_plot: str = "",
        title: str = "",
        year_label: str = "",
        metric_label: str = "",
        textfont_size: int = 10,
        marker_size: float = 7,
        line_width: float = 1.5,
        yshift: int = 4,
    ):
        """:meta private:"""

        data_frame = self.df_.copy()

        column_names = {
            column: column.replace("_", " ").title()
            for column in data_frame.columns
            if column not in ["OCC", "cum_OCC"]
        }
        column_names["OCC"] = "OCC"
        column_names["cum_OCC"] = "cum OCC"
        data_frame = data_frame.rename(columns=column_names)

        if metric_to_plot == "OCC":
            pass
        elif metric_to_plot == "cum_OCC":
            metric_to_plot = "cum OCC"
        else:
            metric_to_plot = metric_to_plot.replace("_", " ").title()

        if auxiliary_metric_to_plot is not None:
            if auxiliary_metric_to_plot == "OCC":
                pass
            elif auxiliary_metric_to_plot == "cum_OCC":
                auxiliary_metric_to_plot = "cum OCC"
            else:
                auxiliary_metric_to_plot = auxiliary_metric_to_plot.replace(
                    "_", " "
                ).title()

        fig = px.line(
            data_frame,
            x=data_frame.index,
            y=metric_to_plot,
            title=title,
            markers=True,
            hover_data=data_frame.columns.to_list(),
        )
        fig.update_traces(
            marker={
                "size": marker_size,
                "line": {"color": MARKER_LINE_COLOR, "width": 2},
            },
            marker_color=MARKER_COLOR,
            line={"color": MARKER_LINE_COLOR, "width": line_width},
        )
        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
        )
        fig.update_yaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
            title=metric_to_plot if metric_label is None else metric_label,
        )
        fig.update_xaxes(
            linecolor="gray",
            linewidth=2,
            gridcolor="lightgray",
            griddash="dot",
            tickangle=270,
            title="Year" if year_label is None else year_label,
            tickmode="array",
            tickvals=data_frame.index,
        )

        if auxiliary_metric_to_plot is not None:
            for index, row in data_frame.iterrows():
                fig.add_annotation(
                    x=index,
                    y=row[metric_to_plot],
                    text=format(int(row[auxiliary_metric_to_plot]), ","),
                    showarrow=False,
                    textangle=-90,
                    yanchor="bottom",
                    font={"size": textfont_size},
                    yshift=yshift,
                )

        return fig

    def prompt(self):
        """:meta private:"""

        data_frame = self.df_.copy()

        main_text = (
            "Your task is to generate a short summary for a research paper about "
            "the annual performance metrics of a bibliographic dataset. The table "
            "below provides data on: "
        )

        for col in data_frame.columns:
            if col == "OCC":
                main_text += "the number of publications per yeear (OCC); "
            if col == "cum_OCC":
                main_text += "the cummulative number of publications per yeear (OCC); "
            if col == "local_citations":
                main_text += (
                    "the number of local citations per year (local_citations); "
                )
            if col == "global_citations":
                main_text += "the number of citations per year (global_citations); "
            if col == "citable_years":
                main_text += "the number of citable years (citable_years); "
            if col == "mean_global_citations":
                main_text += "the average number of citations per document for each year (mean_global_citations); "
            if col == "cum_global_citations":
                main_text += "the cummulative number of citations per document for each year (cum_global_citations); "
            if col == "mean_global_citations_per_year":
                main_text += "the average number of citations per document divided by the age of the documents (mean_global_citations_per_year); "
            if col == "mean_local_citations":
                main_text += "the average number of local citations per document for each year (mean_local_citations); "
            if col == "cum_local_citations":
                main_text += "the cummulative number of local citations per document for each year (cum_local_citations); "
            if col == "mean_local_citations_per_year":
                main_text += "the average number of local citations per document divided by the age of the documents (mean_local_citations_per_year); "

        main_text += (
            " Use the the information in the table "
            "to draw conclusions about the impact per year. In your analysis, be "
            "sure to describe in a clear and concise way, any trends or patterns "
            "you observe, and identify any outliers or anomalies  in the data. "
            "Limit your description to one paragraph with no more than 250 words. "
        )

        table_text = data_frame.to_markdown()

        prompt = self.format_prompt_for_dataframes(main_text, table_text)

        print(prompt)
