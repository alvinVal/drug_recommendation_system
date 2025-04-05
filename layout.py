from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container(
        fluid=True,
        children=[
            dbc.Container(
                fluid=False,
                style={'maxWidth': '900px', 'padding': '20px'},
                children=[
                    # Title and instructions
                    html.H1(
                        "Drug Recommendation System",
                        className="text-center mb-4",
                        style={'color': '#2c3e50', 'fontFamily': 'Georgia, serif', 'fontWeight': 'bold'}
                    ),
                    html.P(
                        "Enter a drug name below to receive alternative recommendations based on therapeutic effects.",
                        className="text-center mb-4",
                        style={'color': '#7f8c8d'}
                    ),
                    # Search bar and output message
                    dbc.Input(
                        id="drug-input",
                        type="text",
                        placeholder="Enter exact drug name...",
                        className="mb-3",
                        style={
                            'width': '100%',
                            'margin': '0 auto',
                            'fontSize': '16px',
                            'border': '1px solid #bdc3c7',
                            'borderRadius': '4px',
                            'padding': '10px'
                        },
                        persistence=True,
                        persistence_type='session'
                    ),
                    html.Div(
                        id="output-container",
                        className="mb-2 text-center",
                        style={'color': '#e74c3c'}
                    ),
                    # All results (suggestions, filters, and drug details) grouped in one container,
                    # hidden unless a valid drug is typed in.
                    html.Div(
                        id="results-section",
                        style={"display": "none"},
                        children=[
                            # Suggested Drugs (displayed just below the search bar)
                            html.Div(
                                id="recommendations-section",
                                children=[
                                    html.H3(
                                        "Suggested Alternative Drugs",
                                        className="text-center mb-3",
                                        style={'color': '#2c3e50'}
                                    ),
                                    html.Div(
                                        id="recommended-drugs",
                                        className="mb-4 d-flex justify-content-center flex-wrap",
                                        style={'gap': '10px'}
                                    )
                                ]
                            ),
                            # Price filters and side effects row
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        dbc.Row([
                                            dbc.Col(
                                                html.H5("Price Range", className="d-flex align-items-center justify-content-center"),
                                                width=8
                                            ),
                                            dbc.Col(
                                                dbc.Switch(
                                                    id="price-filter-toggle",
                                                    label="Enable Price Filter",
                                                    value=False,  # Set to False so that the filter is off initially
                                                    className="mb-2"
                                                ),
                                                width=4,
                                                className="d-flex align-items-center justify-content-end"
                                            )
                                        ]),
                                        dcc.RangeSlider(
                                            id="price-range-slider",
                                            min=0,
                                            max=2000,
                                            step=10,
                                            value=[0, 2000],
                                            marks={i: str(i) for i in range(0, 2001, 500)},
                                            tooltip={"placement": "bottom", "always_visible": True},
                                            disabled=False
                                        ),
                                        # Price display under the slider in a light blue semi-transparent box
                                        html.Div(
                                            id="current-drug-price",
                                            className="mt-2 text-center",
                                            style={
                                                'backgroundColor': 'rgba(173,216,230,0.3)',
                                                'padding': '10px',
                                                'borderRadius': '5px',
                                                'color': 'red',
                                                'fontSize': '1.2rem'
                                            }
                                        )
                                    ], id="price-filter-col")
                                ], width=6),
                                dbc.Col([
                                    html.H5("Exclude Side Effects", className="text-center"),
                                    dcc.Checklist(
                                        id="side-effects-checklist",
                                        options=[],
                                        value=[],
                                        style={'overflowY': 'auto', 'maxHeight': '150px'},
                                        labelStyle={'display': 'block'}
                                    )
                                ], width=6)
                            ]),
                            # Drug Information Section
                            html.Div(
                                id="drug-info-section",
                                children=[
                                    dbc.Row(
                                        className="mt-4",
                                        children=[
                                            dbc.Col(
                                                width=6,
                                                children=[
                                                    html.H3(
                                                        "Therapeutic Class",
                                                        className="text-center mb-3",
                                                        style={'color': '#2980b9'}
                                                    ),
                                                    html.Div(
                                                        id="therapeutic-class",
                                                        className="p-3",
                                                        style={
                                                            'backgroundColor': '#d6eaf8',
                                                            'borderRadius': '4px',
                                                            'minHeight': '100px',
                                                            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
                                                        }
                                                    )
                                                ]
                                            ),
                                            dbc.Col(
                                                width=6,
                                                children=[
                                                    html.H3(
                                                        "Chemical & Action Class",
                                                        className="text-center mb-3",
                                                        style={'color': '#8e44ad'}
                                                    ),
                                                    html.Div(
                                                        id="chemical-action-class",
                                                        className="p-3",
                                                        style={
                                                            'backgroundColor': '#fcf3cf',
                                                            'borderRadius': '4px',
                                                            'minHeight': '100px',
                                                            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
                                                        }
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    dbc.Row(
                                        className="mt-4",
                                        children=[
                                            dbc.Col(
                                                width=6,
                                                children=[
                                                    html.H3(
                                                        "Therapeutic Uses",
                                                        className="text-center mb-3",
                                                        style={'color': '#1d8348'}
                                                    ),
                                                    html.Div(
                                                        id="therapeutic-uses",
                                                        className="p-3",
                                                        style={
                                                            'backgroundColor': '#d5f5e3',
                                                            'borderRadius': '4px',
                                                            'minHeight': '100px',
                                                            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
                                                        }
                                                    )
                                                ]
                                            ),
                                            dbc.Col(
                                                width=6,
                                                children=[
                                                    html.H3(
                                                        "Side Effects",
                                                        className="text-center mb-3",
                                                        style={'color': '#c0392b'}
                                                    ),
                                                    html.Div(
                                                        id="side-effects",
                                                        className="p-3",
                                                        style={
                                                            'backgroundColor': '#fadbd8',
                                                            'borderRadius': '4px',
                                                            'minHeight': '100px',
                                                            'boxShadow': '0 4px 8px rgba(0,0,0,0.1)'
                                                        }
                                                    )
                                                ]
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )
