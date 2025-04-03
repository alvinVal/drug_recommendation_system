from dash import html, dcc
import dash_bootstrap_components as dbc

def create_layout():
    return dbc.Container(
        fluid=True,
        className="d-flex align-items-center justify-content-center vh-100",
        children=[
            dbc.Container(
                fluid=False,
                style={'maxWidth': '900px', 'padding': '20px'},
                children=[
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
                    dbc.Input(
                        id="drug-input",
                        type="text",
                        placeholder="Enter drug name...",
                        className="mb-3",
                        style={
                            'width': '100%',
                            'margin': '0 auto',
                            'fontSize': '16px',
                            'border': '1px solid #bdc3c7',
                            'borderRadius': '4px',
                            'padding': '10px'
                        }
                    ),
                    html.Div(
                        id="output-container",
                        className="mb-2 text-center",
                        style={'color': '#e74c3c'}
                    ),
                    html.H3(
                        "Suggested Alternative Drugs",
                        className="text-center mb-3",
                        style={'color': '#2c3e50'}
                    ),
                    html.Div(
                        id="recommended-drugs",
                        className="mb-4 d-flex justify-content-center flex-wrap",
                        style={'gap': '10px'}
                    ),
                    html.H4("Filter Options", className="text-center mt-4 mb-3"),
                    
                    # Price Range Filter with Explanation
                    dbc.Row([
                        dbc.Col([
                            html.H5("Price Range", className="text-center"),
                            html.P(
                                "Adjust the slider to show only drugs within your preferred price range. "
                                "The range automatically adapts to available options.",
                                className="small text-muted text-center mb-2"
                            ),
                            dcc.RangeSlider(
                                id="price-range-slider",
                                min=0,
                                max=2000,
                                step=10,
                                value=[0, 2000],
                                marks={i: str(i) for i in range(0, 2001, 500)},
                                tooltip={"placement": "bottom", "always_visible": True}
                            )
                        ], width=6),
                        
                        # Side Effects Filter with Explanation
                        dbc.Col([
                            html.H5("Filter by Side Effects", className="text-center"),
                            html.P(
                                "All side effects are pre-checked. Uncheck any you want to AVOID in recommendations. "
                                "Drugs with unchecked effects will be hidden.",
                                className="small text-muted text-center mb-2"
                            ),
                            dcc.Checklist(
                                id="side-effects-checklist",
                                options=[],
                                value=[],
                                style={'overflowY': 'auto', 'maxHeight': '150px'},
                                labelStyle={'display': 'block'}
                            )
                        ], width=6)
                    ]),
                    dbc.Row(
                        className="mt-4",
                        style={'flexWrap': 'nowrap'},
                        children=[
                            dbc.Col(
                                width=6,
                                children=[
                                    html.H3(
                                        "Therapeutic Effects",
                                        className="text-center mb-3",
                                        style={'color': '#2980b9'}
                                    ),
                                    html.Div(
                                        id="therapeutic-effects",
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