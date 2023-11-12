# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods
"""Filtering mixin."""


class FilterMixin:
    """:meta private:"""

    def generate_custom_items(
        self,
        indicators,
        metric,
        top_n,
        occ_range,
        gc_range,
    ):
        """:meta private:"""

        def filter_by_top_n(indicators, top_n):
            """Returns the table of indicators filtered by top_n."""

            return indicators.head(top_n)

        def filter_by_occ_range(indicators, occ_range):
            """Returns the table of indicators filtered by occurrence range."""

            if occ_range[0] is not None:
                indicators = indicators[indicators["OCC"] >= occ_range[0]]
            if occ_range[1] is not None:
                indicators = indicators[indicators["OCC"] <= occ_range[1]]
            return indicators

        def filter_by_gc_range(indicators, gc_range):
            """Returns the table of indicators filtered by global citations range."""

            if gc_range[0] is not None:
                indicators = indicators[indicators["global_citations"] >= gc_range[0]]
            if gc_range[1] is not None:
                indicators = indicators[indicators["global_citations"] <= gc_range[1]]
            return indicators

        #
        # Main code:
        #
        # This is a complex filter for the indicators dataframe. It is based on
        # the requirements of ScientoPy for calculating the top trending items.
        #

        #
        # 1. Filters the dataframe by OCC y GCS ranges. With this step,
        #    items with very low frequency are ignored.
        if gc_range is not None:
            indicators = filter_by_gc_range(indicators, gc_range)

        if occ_range is not None:
            indicators = filter_by_occ_range(indicators, occ_range)

        #
        # 2. Sort the dataframe by metric.
        indicators = self.sort_indicators_by_metric(indicators, metric)

        #
        # 3. Filters the dataframe by top_n.
        if top_n is not None:
            indicators = filter_by_top_n(indicators, top_n)

        return indicators.index.to_list()

    def filter_indicators_by_items(
        self,
        indicators,
        metric,
        #
        # ITEM FILTERS:
        top_n=None,
        occ_range=(None, None),
        gc_range=(None, None),
        custom_items=None,
    ):
        """:meta private:"""

        indicators = indicators.copy()

        if custom_items is None:
            #
            if self._metric == "OCCGC":
                #
                # In this case not is possibe to use trend_analysis
                #
                # Selects the top_n items by OCC
                custom_items_occ = self.generate_custom_items(
                    indicators=indicators,
                    metric="OCC",
                    top_n=self._top_n,
                    occ_range=self._occ_range,
                    gc_range=self._gc_range,
                )

                #
                # Selects the top_n items by GCS
                custom_items_gc = self.generate_custom_items(
                    indicators=indicators,
                    metric="global_citations",
                    top_n=self._top_n,
                    occ_range=self._occ_range,
                    gc_range=self._gc_range,
                )

                custom_items = custom_items_occ[:]
                custom_items += [
                    item for item in custom_items_gc if item not in custom_items_occ
                ]

            else:
                #
                # Default custom items selection
                custom_items = self.generate_custom_items(
                    indicators=indicators,
                    metric=metric,
                    top_n=top_n,
                    occ_range=occ_range,
                    gc_range=gc_range,
                )

        indicators = indicators[indicators.index.isin(custom_items)]
        indicators = self.sort_indicators_by_metric(indicators, self._metric)

        return indicators
