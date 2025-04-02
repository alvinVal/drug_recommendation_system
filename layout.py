# layout.py
from dash import html, dcc

def create_layout():
    return html.Div([
        html.H1("Drug Recommendation System"),
        dcc.Input(id="drug-input", type="text", placeholder="Enter drug name..."),
        dcc.Dropdown(
            id="criteria-dropdown",
            options=[
                {"label": "Therapeutic Effects", "value": "therapeutic effects"},
                {"label": "Side Effects", "value": "side effects"}
            ],
            value="therapeutic effects"
        ),
        html.Div(id="output-container")
    ])
