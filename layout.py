from dash import html, dcc

def create_layout():
    return html.Div(style={
            'font-family': 'Arial, sans-serif', 
            'backgroundColor': '#f5f5f5', 
            'padding': '20px'
        }, children=[
        # Title and instructions
        html.H1("Drug Recommendation System", style={
            'color': '#2c3e50', 
            'font-family': 'Georgia, serif', 
            'fontSize': '40px', 
            'textAlign': 'center'
        }),
        html.P("Enter a drug name below to get alternative recommendations based on therapeutic effects, side effects, or patient preferences.",
               style={'textAlign': 'center', 'fontSize': '18px'}),
        
        # Search area with input and suggestions dropdown
        html.Div([
            dcc.Input(
                id="drug-input", 
                type="text", 
                placeholder="Enter drug name...", 
                style={'width': '60%', 'padding': '10px', 'fontSize': '16px'}
            ),
            dcc.Dropdown(
                id="suggestions-dropdown", 
                placeholder="Suggested drugs", 
                multi=False,
                style={'width': '35%', 'display': 'inline-block', 'marginLeft': '20px', 'fontSize': '16px'}
            ),
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        # Section for suggested alternative drugs
        html.Div(id="output-container", style={
            'backgroundColor': '#ecf0f1', 
            'padding': '10px', 
            'margin': '20px auto', 
            'width': '80%', 
            'borderRadius': '5px'
        }),
        
        # Side-by-side display of drug details: therapeutic effects and side effects
        html.Div([
            html.Div([
                html.H3("Therapeutic Effects", style={'color': '#2980b9'}),
                html.Div(id="therapeutic-effects", style={
                    'backgroundColor': '#d6eaf8', 
                    'padding': '10px', 
                    'minHeight': '150px'
                })
            ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '5%'}),
            
            html.Div([
                html.H3("Side Effects", style={'color': '#c0392b'}),
                html.Div(id="side-effects", style={
                    'backgroundColor': '#fadbd8', 
                    'padding': '10px', 
                    'minHeight': '150px'
                })
            ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top'})
        ], style={'width': '80%', 'margin': 'auto'})
    ])
