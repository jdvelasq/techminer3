"""Trend metrics"""

metrics = {
    #
    # TABLE PARAMS:
    "selected_columns": [
        "OCC",
        "global_citations",
        "mean_global_citations",
        "mean_global_citations_per_year",
    ],
    #
    # CHART PARAMS:
    "metric_to_plot": "OCC",
    "auxiliary_metric_to_plot": None,
    "title": "Annual Scientific Production",
    "year_label": None,
    "metric_label": None,
    "textfont_size": 10,
    "marker_size": 7,
    "line_width": 1.5,
    "yshift": 4,
    #
    # DATABASE PARAMS:
    "root_dir": "example/",
    "database": "main",
    "year_filter": (None, None),
    "cited_by_filter": (None, None),
}
