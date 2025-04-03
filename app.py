import dash
from dash import html, dcc, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import layout
from recommender import get_alternative_drugs, get_drug_side_effects
import pandas as pd
import math

# Load the dataset
df = pd.read_csv("data/drugs.csv")
df["Drug Name"] = df["Drug Name"].str.lower()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = layout.create_layout()

@app.callback(
    [Output("output-container", "children"),
     Output("recommended-drugs", "children"),
     Output("therapeutic-effects", "children"),
     Output("side-effects", "children"),
     Output("side-effects-checklist", "options"),
     Output("side-effects-checklist", "value"),
     Output("price-range-slider", "min"),
     Output("price-range-slider", "max"),
     Output("price-range-slider", "marks"),
     Output("price-range-slider", "value")],
    [Input("drug-input", "value"),
     Input("price-range-slider", "value")]
)
def update_recommendations(drug_name, price_range):
    ctx = callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    
    # Default slider values
    min_price = 0
    max_price = 2000
    marks = {0: '0', 500: '500', 1000: '1000', 1500: '1500', 2000: '2000'}
    slider_value = [0, 2000]

    if not drug_name:
        return ["Please enter a drug name.", [], "No details available.", "No details available.", [], [], min_price, max_price, marks, slider_value]

    drug_lower = drug_name.lower()
    
    # Get side effects for the current drug
    side_effects = get_drug_side_effects(drug_lower)
    side_effect_options = [{'label': effect, 'value': effect} for effect in side_effects]
    
    # Get recommendations
    recommendations = get_alternative_drugs(
        drug_lower, 
        criteria="therapeutic effects",
        price_range=price_range
    )
    
    # Update price slider based on recommendations
    if recommendations and recommendations[0] != "Drug not found in database.":
        recommended_drugs = df[df["Drug Name"].isin([drug.lower() for drug in recommendations])]
        if not recommended_drugs.empty:
            min_price = math.floor(recommended_drugs['Price'].min())
            max_price = math.ceil(recommended_drugs['Price'].max())
            if min_price == max_price:  # Handle single-price case
                max_price += 100
            step = (max_price - min_price) / 4
            marks = {
                int(min_price + i*step): str(int(min_price + i*step))
                for i in range(5)
            }
            slider_value = [min_price, max_price]

    if not recommendations or recommendations[0] == "Drug not found in database.":
        return ["Drug not found in database.", [], "No details available.", "No details available.", side_effect_options, side_effects, min_price, max_price, marks, slider_value]
    
    # Create buttons for recommendations
    buttons = [
        dbc.Button(
            drug.capitalize(),
            id={'type': 'recommendation-button', 'index': drug},
            className="m-1",
            color="primary",
            n_clicks=0
        ) for drug in recommendations
    ]
    
    # Get drug details
    drug_row = df[df["Drug Name"] == drug_lower]
    if drug_row.empty:
        return ["Drug not found in database.", [], "No details available.", "No details available.", side_effect_options, side_effects, min_price, max_price, marks, slider_value]
    
    drug_data = drug_row.iloc[0]
    therapeutic = f"Therapeutic Class: {drug_data.get('Therapeutic Class', 'N/A')}"
    side_effects_text = "Side Effects: " + ", ".join([str(effect) for effect in side_effects if effect])
    
    return ["", buttons, therapeutic, side_effects_text, side_effect_options, side_effects, min_price, max_price, marks, slider_value]

@app.callback(
    Output("drug-input", "value"),
    [Input({'type': 'recommendation-button', 'index': ALL}, 'n_clicks')],
    [State({'type': 'recommendation-button', 'index': ALL}, 'id')],
    prevent_initial_call=True
)
def update_input(n_clicks, button_ids):
    ctx = callback_context
    if not ctx.triggered:
        return no_update
    
    # Get the index of the clicked button
    clicked_index = next(
        (i for i, n in enumerate(n_clicks) if n is not None and n > 0),
        None
    )
    
    if clicked_index is not None:
        return button_ids[clicked_index]['index']
    
    return no_update

@app.callback(
    Output("current-drug-price", "children"),
    Input("drug-input", "value"),
    prevent_initial_call=True
)
def update_current_drug_price(drug_name):
    if not drug_name:
        return ""
    
    drug_lower = drug_name.lower()
    drug_row = df[df["Drug Name"] == drug_lower]
    
    if drug_row.empty:
        return html.Span("Drug Price: Not available", style={'color': 'red'})
    
    price = drug_row.iloc[0]['Price']
    return html.Span([
        "Drug Price: ",
        html.Span(
            f"₱{price:,.2f}",  # Philippine Peso symbol with comma formatting
            style={
                'color': 'darkred',
                'fontWeight': 'bolder',
                'fontSize': '1.2rem'
            }
        )
    ])

@app.callback(
    Output("recommended-drugs", "children", allow_duplicate=True),
    [Input("side-effects-checklist", "value"),
     Input("price-range-slider", "value")],
    [State("drug-input", "value")],
    prevent_initial_call=True
)
def filter_recommendations(selected_side_effects, price_range, drug_name):
    if not drug_name:
        return []
    
    recommendations = get_alternative_drugs(
        drug_name.lower(),
        criteria="therapeutic effects",
        selected_side_effects=selected_side_effects,
        price_range=price_range
    )
    
    if not recommendations or recommendations[0] == "Drug not found in database.":
        return [html.Div("No alternatives found with these filters.", className="text-center")]
    
    buttons = [
        dbc.Button(
            drug.capitalize(),
            id={'type': 'recommendation-button', 'index': drug},
            className="m-1",
            color="primary",
            n_clicks=0
        ) for drug in recommendations
    ]
    
    return buttons

if __name__ == "__main__":
    app.run(debug=True)