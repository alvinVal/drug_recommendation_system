from dash import html, dcc

def create_layout():
    return html.Div(style={
        'font-family': 'Arial, sans-serif',
        'backgroundColor': '#f4f4f9',
        'padding': '20px'
    }, children=[
        html.Div(style={
            'maxWidth': '800px',
            'margin': 'auto',
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'borderRadius': '8px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        }, children=[
            html.H1("Drug Recommendation System", style={
                'color': '#2c3e50',
                'font-family': 'Georgia, serif',
                'fontSize': '36px',
                'textAlign': 'center',
                'marginBottom': '10px'
            }),
            html.P("Enter a drug name below to receive alternative recommendations based on therapeutic effects or side effects.", style={
                'textAlign': 'center',
                'fontSize': '16px',
                'color': '#7f8c8d',
                'marginBottom': '30px'
            }),
            html.Div([
                dcc.Input(
                    id="drug-input",
                    type="text",
                    placeholder="Enter drug name...",
                    style={
                        'width': '100%',
                        'padding': '10px',
                        'fontSize': '16px',
                        'border': '1px solid #bdc3c7',
                        'borderRadius': '4px'
                    }
                ),
                dcc.Dropdown(
                    id="suggestions-dropdown",
                    placeholder="Suggested drugs will appear here...",
                    style={
                        'width': '100%',
                        'marginTop': '10px',
                        'fontSize': '16px'
                    }
                ),
            ], style={'marginBottom': '20px'}),
            html.Div(id="output-container", style={
                'backgroundColor': '#ecf0f1',
                'padding': '15px',
                'borderRadius': '4px',
                'marginBottom': '20px'
            }),
            html.Div([
                html.Div([
                    html.H3("Therapeutic Effects", style={
                        'color': '#2980b9',
                        'borderBottom': '2px solid #2980b9',
                        'paddingBottom': '5px',
                        'marginBottom': '10px'
                    }),
                    html.Div(id="therapeutic-effects", style={
                        'backgroundColor': '#d6eaf8',
                        'padding': '10px',
                        'borderRadius': '4px',
                        'minHeight': '100px'
                    })
                ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top'}),
                html.Div([
                    html.H3("Side Effects", style={
                        'color': '#c0392b',
                        'borderBottom': '2px solid #c0392b',
                        'paddingBottom': '5px',
                        'marginBottom': '10px'
                    }),
                    html.Div(id="side-effects", style={
                        'backgroundColor': '#fadbd8',
                        'padding': '10px',
                        'borderRadius': '4px',
                        'minHeight': '100px'
                    })
                ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%', 'verticalAlign': 'top'})
            ])
        ])
    ])
