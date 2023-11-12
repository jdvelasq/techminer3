# pylint: disable=too-few-public-methods
"""Mixin function for sorting."""


class SortingIndicatorsMixin:
    """:meta private:"""

    def sort_indicators_by_metric(
        self,
        indicators,
        metric,
    ):
        """:meta private:"""

        indicators = indicators.copy()
        indicators["_name_"] = indicators.index.tolist()

        columns = {
            # -------------------------------------------
            "OCCGC": [
                "OCC",
                "global_citations",
                "local_citations",
                "_name_",
            ],
            # -------------------------------------------
            "OCC": [
                "OCC",
                "global_citations",
                "local_citations",
                "_name_",
            ],
            # -------------------------------------------
            "global_citations": [
                "global_citations",
                "local_citations",
                "OCC",
                "_name_",
            ],
            # -------------------------------------------
            "local_citations": [
                "local_citations",
                "global_citations",
                "OCC",
                "_name_",
            ],
            # -------------------------------------------
            "h_index": [
                "h_index",
                "global_citations",
                "OCC",
                "_name_",
            ],
            # -------------------------------------------
            "g_index": [
                "g_index",
                "global_citations",
                "OCC",
                "_name_",
            ],
            # -------------------------------------------
            "m_index": [
                "m_index",
                "global_citations",
                "OCC",
                "_name_",
            ],
        }[metric]
        ascending = [False] * (len(columns) - 1) + [True]

        indicators = indicators.sort_values(columns, ascending=ascending)
        indicators = indicators.drop(columns=["_name_"])

        return indicators
