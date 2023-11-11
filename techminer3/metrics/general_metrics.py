# pylint: disable=too-few-public-methods
# pylint: disable=too-many-stance-attributes
# pylint: disable=too-many-instance-attributes
"""
General Metrics
===============================================================================

>>> from techminer3.metrics import GeneralMetrics
>>> GeneralMetrics(
...     #
...     # DATABASE PARAMS:
...     root_dir="example/", 
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... ).df_
                                                            value
category       item                                              
GENERAL        Timespan                                 2015:2019
               Documents                                       50
               Annual growth rate %                        118.67
               Document average age                          5.24
               Num References                                1275
               Average references per document              26.02
               Average citations per document               162.7
               Average citations per document per year      32.54
               Sources                                         41
               Average documents per source                  1.22
DOCUMENT TYPES Article                                         37
               Book                                             1
               Conference paper                                 4
               Editorial                                        2
               Review                                           6
AUTHORS        Authors                                        115
               Authors of single-authored documents            12
               Single-authored documents                       12
               Multi-authored documents                        38
               Authors per document                          2.52
               Co-authors per document                        3.0
               International co-authorship %                30.61
               Author appearances                             126
               Documents per author                           0.4
               Collaboration index                            1.0
               Organizations                                   91
               Organizations (1st author)                      43
               Countries                                       24
               Countries (1st author)                          18
KEYWORDS       Raw author keywords                            148
               Cleaned author keywords                        148
               Raw index keywords                             179
               Cleaned index keywords                         179
               Raw keywords                                   279
               Cleaned keywords                               279
NLP PHRASES    Raw title NLP phrases                          124
               Cleaned title NLP phrases                      124
               Raw abstract NLP phrases                      1461
               Cleaned abstract NLP phrases                  1461
               Raw NLP phrases                               1501
               Cleaned NLP phrases                           1501
DESCRIPTORS    Raw descriptors                               1668
               Cleaned descriptors                           1668


>>> from techminer3.metrics import GeneralMetrics
>>> GeneralMetrics( # doctest: +ELLIPSIS
...     #
...     # DATABASE PARAMS:
...     root_dir="example/", 
...     database="main",
...     year_filter=(None, None),
...     cited_by_filter=(None, None),
... ).prompt()
Your task is ...

    


"""
import datetime

import numpy as np
import pandas as pd

from .._mixins.prompts import PromptMixin
from .._mixins.read_records import ReadRecordsMixin


class GeneralMetrics(
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
        # COMPUTATIONS:
        self._records: pd.DataFrame = pd.DataFrame()
        self._stats: list = []

        #
        # RESULTS:
        self.df_: pd.DataFrame = pd.DataFrame()

        #
        # RUN:
        self.__post_init__()

    def __post_init__(self):
        #
        # DATABASE:
        self._records = self.read_records(
            root_dir=self._root_dir,
            database=self._database,
            year_filter=self._year_filter,
            cited_by_filter=self._cited_by_filter,
            **self._filters,
        )

        #
        #
        # COMPUTE STATS
        #
        #
        self._compute_general_information_stats()
        self._compute_document_types_stats()
        self._compute_authors_stats()
        self._compute_keywords_stats()
        self._compute_nlp_phrases_stats()
        self._compute_descriptors_stats()

        #
        # Create a dataframe:
        self.df_ = pd.DataFrame(self._stats)
        self.df_ = self.df_.set_index(["category", "item"])

    #
    #
    # PROMPT
    #
    #
    def prompt(self):
        """:meta private:"""

        main_text = (
            "Your task is to generate a short summary for a research paper of a "
            "table with record and field statistics for a dataset of scientific "
            "publications. The table below, delimited by triple backticks, "
            "provides data on the main characteristics of the records and fields "
            "of the bibliographic dataset. Use the the information in the table "
            "to draw conclusions. Limit your description to one paragraph in at "
            "most 100 words. "
        )

        table_text = self.df_.dropna().to_markdown()

        prompt = self.format_prompt_for_dataframes(main_text, table_text)

        print(prompt)

    #
    #
    # AUXILIARY METHODS
    #
    #
    def insert_stats(self, category, item, value):
        """Inserts stats"""

        self._stats.append(
            {
                "category": category,
                "item": item,
                "value": value,
            }
        )

    def count_unique_items(self, field):
        """Computes the number of unique items in a field."""

        if field not in self._records:
            return 0

        records = self._records[field].copy()
        records = records.dropna()
        records = records.str.split(";")
        records = records.explode()
        records = records.str.strip()
        records = records.drop_duplicates()

        return len(records)

    #
    #
    # GENERAL INFORMATION STATS
    #
    #
    def _compute_general_information_stats(self):
        #
        # ------------------------------------------------------------------------------
        def compute_timespam():
            return str(min(self._records.year)) + ":" + str(max(self._records.year))

        self.insert_stats(
            "GENERAL",
            "Timespan",
            compute_timespam(),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "GENERAL",
            "Documents",
            len(self._records),
        )

        # ------------------------------------------------------------------------------
        def compute_annual_growth_rate():
            n_records = len(self._records)
            n_years = max(self._records.year) - min(self._records.year) + 1
            po_ = len(self._records.year[self._records.year == min(self._records.year)])
            return round(100 * (np.power(n_records / po_, 1 / n_years) - 1), 2)

        self.insert_stats(
            "GENERAL",
            "Annual growth rate %",
            compute_annual_growth_rate(),
        )

        # ------------------------------------------------------------------------------
        def compute_document_average_age():
            """Computes the average age of the documents"""
            mean_years = self._records.year.copy()
            mean_years = mean_years.dropna()
            mean_years = mean_years.mean()
            current_year = datetime.datetime.now().year
            return round(int(current_year) - mean_years, 2)

        self.insert_stats(
            "GENERAL",
            "Document average age",
            compute_document_average_age(),
        )

        # ------------------------------------------------------------------------------
        def compute_num_references():
            if "global_references" in self._records.columns:
                records = self._records.global_references.copy()
                records = records.dropna()
                records = records.str.split(";")
                records = records.explode()
                records = records.str.strip()
                return len(records)
            return pd.NA

        self.insert_stats(
            "GENERAL",
            "Num References",
            compute_num_references(),
        )

        # ------------------------------------------------------------------------------
        def compute_average_references_per_document():
            """Computes the average number of references per document"""

            if "global_references" in self._records.columns:
                num_references = self._records.global_references.copy()
                num_references = num_references.dropna()
                num_references = num_references.str.split(";")
                num_references = num_references.map(len)
                return round(num_references.mean(), 2)
            return pd.NA

        self.insert_stats(
            "GENERAL",
            "Average references per document",
            compute_average_references_per_document(),
        )

        # ------------------------------------------------------------------------------
        def compute_average_citations_per_document():
            if "global_citations" in self._records.columns:
                return round(self._records.global_citations.mean(), 2)
            return pd.NA

        self.insert_stats(
            "GENERAL",
            "Average citations per document",
            compute_average_citations_per_document(),
        )

        # ------------------------------------------------------------------------------
        def compute_average_citations_per_document_per_year():
            if "global_citations" in self._records.columns:
                return round(
                    self._records.global_citations.mean()
                    / (self._records.year.max() - self._records.year.min() + 1),
                    2,
                )
            return pd.NA

        self.insert_stats(
            "GENERAL",
            "Average citations per document per year",
            compute_average_citations_per_document_per_year(),
        )

        # ------------------------------------------------------------------------------
        def compute_num_sources():
            if "source_title" in self._records.columns:
                records = self._records.source_title.copy()
                records = records.dropna()
                records = records.drop_duplicates()
                return len(records)
            return pd.NA

        self.insert_stats(
            "GENERAL",
            "Sources",
            compute_num_sources(),
        )

        # ------------------------------------------------------------------------------
        def compute_average_documents_per_source():
            if "source_title" in self._records.columns:
                sources = self._records.source_title.copy()
                sources = sources.dropna()
                n_records = len(sources)
                sources = sources.drop_duplicates()
                n_sources = len(sources)
                return round(n_records / n_sources, 2)
            return pd.NA

        self.insert_stats(
            "GENERAL",
            "Average documents per source",
            compute_average_documents_per_source(),
        )

    #
    #
    # COMPUTE DOCUMENT TYPE STATS
    #
    #
    def _compute_document_types_stats(self):
        # Computes the document types statistics

        records = self._records[["document_type"]].dropna()

        document_types_count = (
            records[["document_type"]].groupby("document_type").size()
        )

        for document_type, count in zip(
            document_types_count.index, document_types_count
        ):
            self.insert_stats(
                "DOCUMENT TYPES",
                document_type,
                count,
            )

    #
    #
    # COMPUTE AUTHOR STATS
    #
    #
    def _compute_authors_stats(self):
        #
        # ------------------------------------------------------------------------------
        self.insert_stats(
            "AUTHORS",
            "Authors",
            self.count_unique_items("authors"),
        )

        # ------------------------------------------------------------------------------
        def num_authors_of_single_authored_documents():
            records = self._records[self._records["num_authors"] == 1]
            authors = records.authors.dropna()
            authors = authors.drop_duplicates()
            return len(authors)

        self.insert_stats(
            "AUTHORS",
            "Authors of single-authored documents",
            num_authors_of_single_authored_documents(),
        )

        # ------------------------------------------------------------------------------
        def count_single_authored_documents():
            return len(self._records[self._records["num_authors"] == 1])

        self.insert_stats(
            "AUTHORS",
            "Single-authored documents",
            count_single_authored_documents(),
        )

        # ------------------------------------------------------------------------------
        def count_multi_authored_documents():
            return len(self._records[self._records["num_authors"] > 1])

        self.insert_stats(
            "AUTHORS",
            "Multi-authored documents",
            count_multi_authored_documents(),
        )

        # ------------------------------------------------------------------------------
        def average_authors_per_document():
            num_authors = self._records["num_authors"].dropna()
            return round(num_authors.mean(), 2)

        self.insert_stats(
            "AUTHORS",
            "Authors per document",
            average_authors_per_document(),
        )

        # ------------------------------------------------------------------------------
        def co_authors_per_document():
            records = self._records.copy()
            num_authors = records[records.num_authors > 1].num_authors
            return round(num_authors.mean(), 2)

        self.insert_stats(
            "AUTHORS",
            "Co-authors per document",
            co_authors_per_document(),
        )

        # ------------------------------------------------------------------------------
        def international_co_authorship():
            countries = self._records.countries.copy()
            countries = countries.dropna()
            countries = countries.str.split(";")
            countries = countries.map(len)
            return round(len(countries[countries > 1]) / len(countries) * 100, 2)

        self.insert_stats(
            "AUTHORS",
            "International co-authorship %",
            international_co_authorship(),
        )

        # ------------------------------------------------------------------------------
        def author_appearances():
            """Computes the number of author appearances"""
            records = self._records.authors.copy()
            records = records.dropna()
            records = records.str.split(";")
            records = records.explode()
            records = records.str.strip()
            return len(records)

        self.insert_stats(
            "AUTHORS",
            "Author appearances",
            author_appearances(),
        )

        # ------------------------------------------------------------------------------
        def average_documents_per_author():
            records = self._records.authors.copy()
            records = records.dropna()
            n_records = len(records)
            records = records.str.split(";")
            records = records.explode()
            n_authors = len(records)
            return round(n_records / n_authors, 2)

        self.insert_stats(
            "AUTHORS",
            "Documents per author",
            average_documents_per_author(),
        )

        # ------------------------------------------------------------------------------
        def collaboration_index():
            records = self._records[["authors", "num_authors"]].copy()
            records = records.dropna()
            records = records[records.num_authors > 1]
            n_records = len(records)

            n_authors = records.authors.copy()
            n_authors = n_authors.str.split(";")
            n_authors = n_authors.explode()
            n_authors = len(records)
            return round(n_authors / n_records, 2)

        self.insert_stats(
            "AUTHORS",
            "Collaboration index",
            collaboration_index(),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "AUTHORS",
            "Organizations",
            self.count_unique_items("organizations"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "AUTHORS",
            "Organizations (1st author)",
            self.count_unique_items("organization_1st_author"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "AUTHORS",
            "Countries",
            self.count_unique_items("countries"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "AUTHORS",
            "Countries (1st author)",
            self.count_unique_items("country_1st_author"),
        )

    #
    #
    # COMPUTE KEYWORDS STATS
    #
    #
    def _compute_keywords_stats(self):
        """Computes the keywords stats"""

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "KEYWORDS",
            "Raw author keywords",
            self.count_unique_items("raw_author_keywords"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "KEYWORDS",
            "Cleaned author keywords",
            self.count_unique_items("author_keywords"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "KEYWORDS",
            "Raw index keywords",
            self.count_unique_items("raw_index_keywords"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "KEYWORDS",
            "Cleaned index keywords",
            self.count_unique_items("index_keywords"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "KEYWORDS",
            "Raw keywords",
            self.count_unique_items("raw_keywords"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "KEYWORDS",
            "Cleaned keywords",
            self.count_unique_items("keywords"),
        )

    #
    #
    # COMPUTE NLP PHRASES STATS
    #
    #
    def _compute_nlp_phrases_stats(self):
        # ------------------------------------------------------------------------------
        self.insert_stats(
            "NLP PHRASES",
            "Raw title NLP phrases",
            self.count_unique_items("raw_title_nlp_phrases"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "NLP PHRASES",
            "Cleaned title NLP phrases",
            self.count_unique_items("title_nlp_phrases"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "NLP PHRASES",
            "Raw abstract NLP phrases",
            self.count_unique_items("raw_abstract_nlp_phrases"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "NLP PHRASES",
            "Cleaned abstract NLP phrases",
            self.count_unique_items("abstract_nlp_phrases"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "NLP PHRASES",
            "Raw NLP phrases",
            self.count_unique_items("raw_nlp_phrases"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "NLP PHRASES",
            "Cleaned NLP phrases",
            self.count_unique_items("nlp_phrases"),
        )

    #
    #
    # COMPUTE DESCRIPTOR STATS
    #
    #
    def _compute_descriptors_stats(self):
        # ------------------------------------------------------------------------------
        self.insert_stats(
            "DESCRIPTORS",
            "Raw descriptors",
            self.count_unique_items("raw_descriptors"),
        )

        # ------------------------------------------------------------------------------
        self.insert_stats(
            "DESCRIPTORS",
            "Cleaned descriptors",
            self.count_unique_items("descriptors"),
        )
