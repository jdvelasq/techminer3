# pylint: disable=too-few-public-methods
"""Mixin function to read records from a file."""

import os

import pandas as pd

from ..constants import DATABASE_NAMES_TO_FILE_NAMES


class ReadRecordsMixin:
    """Read records from a file."""

    def read_records(
        self,
        #
        # DATABASE PARAMS:
        root_dir="./",
        database="main",
        year_filter=(None, None),
        cited_by_filter=(None, None),
        **filters,
    ):
        """:meta private:"""

        records = self._get_records_from_file(root_dir, database)
        records = self._filter_records_by_year(records, year_filter)
        records = self._filter_records_by_citations(records, cited_by_filter)
        records = self._apply_filters_to_records(records, **filters)

        return records

    def _get_records_from_file(self, root_dir, database):
        """Read raw records from a file."""

        file_name = DATABASE_NAMES_TO_FILE_NAMES[database]
        file_path = os.path.join(root_dir, "databases", file_name)
        records = pd.read_csv(file_path, sep=",", encoding="utf-8", compression="zip")
        records = records.drop_duplicates()

        return records

    def _filter_records_by_year(self, records, year_filter):
        """Filter records by year."""

        if year_filter is None:
            return records

        if not isinstance(year_filter, tuple):
            raise TypeError("The year_filter parameter must be a tuple of two values.")

        if len(year_filter) != 2:
            raise ValueError("The year_filter parameter must be a tuple of two values.")

        start_year, end_year = year_filter

        if start_year is not None:
            records = records[records.year >= start_year]

        if end_year is not None:
            records = records[records.year <= end_year]

        return records

    def _filter_records_by_citations(self, records, cited_by_filter):
        """Filter records by year."""

        if cited_by_filter is None:
            return records

        if not isinstance(cited_by_filter, tuple):
            raise TypeError(
                "The cited_by_range parameter must be a tuple of two values."
            )

        if len(cited_by_filter) != 2:
            raise ValueError(
                "The cited_by_range parameter must be a tuple of two values."
            )

        cited_by_min, cited_by_max = cited_by_filter

        if cited_by_min is not None:
            records = records[records.global_citations >= cited_by_min]

        if cited_by_max is not None:
            records = records[records.global_citations <= cited_by_max]

        return records

    def _apply_filters_to_records(self, records, **filters):
        """Apply user filters in order."""

        for filter_name, filter_value in filters.items():
            #
            # Split the filter value into a list of strings
            database = records[["article", filter_name]]
            database[filter_name] = database[filter_name].str.split(";")

            # Explode the list of strings into multiple rows
            database = database.explode(filter_name)

            # Remove leading and trailing whitespace from the strings
            database[filter_name] = database[filter_name].str.strip()

            # Keep only records that match the filter value
            database = database[database[filter_name].isin(filter_value)]
            records = records[records["article"].isin(database["article"])]

        return records
