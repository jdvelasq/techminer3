# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    use_pages=True,
)


TOGGLE_STYLE = {
    "background": "rgb(226,108,33)",
    "border-color": "rgb(226,108,33)",
}

STYLE = {
    "color": "white",
    "padding-top": "10px",
    "padding-left": "20px",
    "width": "100px",
}


# ------------------------------------------------------------------------------
#
# DATA MENU
#
#
def mn_data():
    """Data menu"""

    return dbc.NavItem(
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Option 1", href="#"),
                dbc.DropdownMenuItem("Option 2", href="#"),
                dbc.DropdownMenuItem("Option 3", href="#"),
            ],
            label="Data",
            toggle_style=TOGGLE_STYLE,
            style=STYLE,
        ),
    )


# ------------------------------------------------------------------------------
#
# REFINE MENU
#
#
def mn_refine():
    """Refine menu"""

    return dbc.NavItem(
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Option 1", href="#"),
                dbc.DropdownMenuItem("Option 2", href="#"),
                dbc.DropdownMenuItem("Option 3", href="#"),
            ],
            label="Refine",
            toggle_style=TOGGLE_STYLE,
            style=STYLE,
        ),
    )


# ------------------------------------------------------------------------------
#
# FILTER MENU
#
#
def mn_filter():
    """Filter menu"""

    return dbc.NavItem(
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(
                    "Edit", href=dash.page_registry["pages.mn_filter_edit"]["path"]
                ),
            ],
            label="Filter",
            toggle_style=TOGGLE_STYLE,
            style=STYLE,
        )
    )


# ------------------------------------------------------------------------------
#
# SEARCH MENU
#
#
def mn_search():
    """Search menu"""

    return dbc.NavItem(
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Option 1", href="#"),
                dbc.DropdownMenuItem("Option 2", href="#"),
                dbc.DropdownMenuItem("Option 3", href="#"),
            ],
            label="Search",
            toggle_style=TOGGLE_STYLE,
            style=STYLE,
        )
    )


# ------------------------------------------------------------------------------
#
# ANALYZE MENU
#
#
def mn_analyze():
    """Analyze menu"""

    return dbc.NavItem(
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Option 1", href="#"),
                dbc.DropdownMenuItem("Option 2", href="#"),
                dbc.DropdownMenuItem("Option 3", href="#"),
            ],
            label="Analyze",
            toggle_style=TOGGLE_STYLE,
            style=STYLE,
        )
    )


# ------------------------------------------------------------------------------
#
# TOOLS MENU
#
#
def mn_tools():
    """Tools menu"""

    return dbc.NavItem(
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem("Option 1", href="#"),
                dbc.DropdownMenuItem("Option 2", href="#"),
                dbc.DropdownMenuItem("Option 3", href="#"),
            ],
            label="Tools",
            toggle_style=TOGGLE_STYLE,
            style=STYLE,
        )
    )


# ------------------------------------------------------------------------------
#
# APP LAYOUT
#
#
app.layout = html.Div(
    [
        html.Div(
            [
                dbc.Nav(
                    [
                        html.H1("TechMiner3", style={"color": "white"}),
                        #
                        mn_data(),
                        mn_refine(),
                        mn_filter(),
                        mn_search(),
                        mn_analyze(),
                        mn_tools(),
                    ],
                    navbar=True,
                    style={
                        "justify-content": "flex-row align-middle",
                        "padding": "10px",
                        "box-shadow": "4px 4px 0px lightgrey",
                    },
                ),
            ],
            style={"background-color": "rgb(226,108,33)"},
        ),
        dash.page_container,
    ],
)


if __name__ == "__main__":
    for page in dash.page_registry.keys():
        print(page)
    app.run_server(debug=True)
