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