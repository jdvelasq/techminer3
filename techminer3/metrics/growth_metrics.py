        # -------------------------------------------------------------------------------
        def compute_growth_indicators(indicators):
            """Computes growth indicators."""

            #
            # Computes item occurrences by year
            items_by_year = items_occurrences_by_year(
                #
                # FUNCTION PARAMS:
                field=field,
                cumulative=False,
                #
                # DATABASE PARAMS:
                root_dir=root_dir,
                database=database,
                year_filter=year_filter,
                cited_by_filter=cited_by_filter,
                **filters,
            )

            #
            # Computes the range of years in the time window
            year_end = items_by_year.columns.max()
            year_start = year_end - time_window + 1
            year_columns = list(range(year_start, year_end + 1))

            #
            # TODO: CHECK
            if items_by_year.columns.max() - items_by_year.columns.min() <= time_window:
                return indicators
            #

            #
            # Computes the number of documents per period by item
            between = f"between_{year_start}_{year_end}"
            before = f"before_{year_start}"
            between_occ = items_by_year.loc[:, year_columns].sum(axis=1)
            before_occ = items_by_year.sum(axis=1) - between_occ
            indicators.loc[between_occ.index, between] = between_occ
            indicators.loc[before_occ.index, before] = before_occ

            indicators = indicators.assign(
                growth_percentage=(
                    100 * indicators[between].copy() / indicators["OCC"].copy()
                ).round(2)
            )

            #
            # sort the columns
            columns = ["OCC", before, between, "growth_percentage"] + [
                col
                for col in indicators.columns
                if col not in ["OCC", before, between, "growth_percentage"]
            ]
            indicators = indicators[columns]

            #
            # selects the columns of interest
            items_by_year = items_by_year.loc[:, [year_columns[0] - 1] + year_columns]

            # agr: average growth rate
            agr = items_by_year.diff(axis=1)
            agr = agr.loc[:, year_columns]
            agr = agr.sum(axis=1) / time_window
            indicators.loc[agr.index, "average_growth_rate"] = agr

            # ady: average documents per year
            ady = items_by_year.loc[:, year_columns].sum(axis=1) / time_window
            indicators.loc[ady.index, "average_docs_per_year"] = ady

            # pdly: percentage of documents in last year
            indicators = indicators.assign(
                percentage_docs_last_year=(
                    indicators.average_docs_per_year.copy() / indicators.OCC.copy()
                )
            )

            return indicators

        indicators = compute_growth_indicators(indicators)
