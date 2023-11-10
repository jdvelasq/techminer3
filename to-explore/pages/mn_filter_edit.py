"""Filter/Edit menu page"""

import json
import os

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output

from .constants import DATABASE_PARAMS_FILE

dash.register_page(__name__)


def load_database_params():
    """Load filter parameters from DATABASE_PARAMS_FILE"""

    # if file not exists, create it and populate with default values
    if not os.path.exists(DATABASE_PARAMS_FILE):
        default_params = {
            "root_dir": "./",
            "database": "main",
            "year_filter": (None, None),
            "cited_by_filter": (None, None),
        }
        save_database_params(default_params)

    with open(DATABASE_PARAMS_FILE, "r", encoding="utf-8") as in_file:
        params = json.load(in_file)

    return params


def save_database_params(params):
    """Save filter parameters to DATABASE_PARAMS_FILE"""

    with open(DATABASE_PARAMS_FILE, "w", encoding="utf-8") as out_file:
        json.dump(params, out_file, indent=4)


def layout():
    """Return layout for this page"""

    params = load_database_params()
    print(params)

    return html.Div(
        [
            html.H2("Database filters"),
            html.Hr(),
            dbc.Label("Root directory:"),
            html.Br(),
            dbc.Input(placeholder="./", type="text", disabled=True),
            html.Hr(),
            dbc.Label("Database:"),
            dbc.RadioItems(
                options=[
                    {"label": "Main", "value": "main"},
                    {"label": "Cited by", "value": "cited_by"},
                    {"label": "References", "value": "references"},
                ],
                value=params["database"],
                id="radioitems-input",
            ),
            html.Hr(),
            dbc.Label("Year Filter:"),
            html.Hr(),
            dbc.Label("Cited by Filter:"),
            html.Hr(),
        ],
        style={
            # "color": "white",
            "padding": "20px 20px 20px 20px",
            # "padding-top": "10px",
            # "padding-left": "10px",
            # "padding-right": "10px",
            # "width": "100px",
        },
    )
