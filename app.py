import dash
from dash import html, dcc, callback_context, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
import layout
from recommender import get_alternative_drugs, get_drug_side_effects
import pandas as pd
import math
import json

# Load the dataset
df = pd.read_csv("data/drugs.csv")
df["Drug Name"] = df["Drug Name"].str.lower()

# Initialize the app with additional CSS for smoother transitions
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Add CSS for smoother transitions
app.css.append_css({
    'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css'
})

# Enable loading states
app.config.suppress_callback_exceptions = True

app.layout = layout.create_layout()

# Callback to update drug info and initialize filters
@app.callback(
    [Output("output-container", "children"),
     Output("therapeutic-effects", "children"),
     Output("side-effects", "children"),
     Output("side-effects-checklist", "options"),
     Output("price-range-slider", "min"),
     Output("price-range-slider", "max"),
     Output("price-range-slider", "marks"),
     Output("current-drug-price", "children")],
    Input("drug-input", "value"),
    prevent_initial_call=True
)
def update_drug_info(drug_name):
    if not drug_name:
        return ["Please enter a drug name.", "No details available.", "No details available.", [], 
                0, 2000, {0: '0', 500: '500', 1000: '1000', 1500: '1500', 2000: '2000'}, ""]

    drug_lower = drug_name.lower()
    side_effects = get_drug_side_effects(drug_lower)
    side_effect_options = [{'label': effect, 'value': effect} for effect in side_effects]
    
    # Get price range for recommendations
    recommendations = get_alternative_drugs(drug_lower, criteria="therapeutic effects")
    min_price, max_price = 0, 2000
    marks = {0: '0', 500: '500', 1000: '1000', 1500: '1500', 2000: '2000'}
    
    if recommendations and recommendations[0] != "Drug not found in database.":
        recommended_drugs = df[df["Drug Name"].isin([drug.lower() for drug in recommendations])]
        if not recommended_drugs.empty:
            min_price = math.floor(recommended_drugs['Price'].min())
            max_price = math.ceil(recommended_drugs['Price'].max())
            if min_price == max_price:
                max_price += 100
            step = (max_price - min_price) / 4
            marks = {
                int(min_price + i*step): str(int(min_price + i*step))
                for i in range(5)
            }

    # Get drug details and price
    drug_row = df[df["Drug Name"] == drug_lower]
    if drug_row.empty:
        return ["Drug not found in database.", "No details available.", "No details available.", 
                side_effect_options, min_price, max_price, marks, "Drug Price: Not available"]
    
    drug_data = drug_row.iloc[0]
    therapeutic = f"Therapeutic Class: {drug_data.get('Therapeutic Class', 'N/A')}"
    side_effects_text = "Side Effects: " + ", ".join([str(effect) for effect in side_effects if effect])
    price_display = html.Span([
        "Drug Price: ",
        html.Span(
            f"₱{drug_data['Price']:,.2f}",
            style={'color': 'darkred', 'fontWeight': 'bolder', 'fontSize': '1.2rem'}
        )
    ])
    
    return ["", therapeutic, side_effects_text, side_effect_options, 
            min_price, max_price, marks, price_display]

# Callback to update recommendations based on filters
@app.callback(
    Output("recommended-drugs", "children"),
    [Input("drug-input", "value"),
     Input("side-effects-checklist", "value"),
     Input("price-range-slider", "value")],
    prevent_initial_call=True
)
def update_recommendations(drug_name, selected_side_effects, price_range):
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
    
    return [
        dbc.Button(
            drug.capitalize(),
            id={'type': 'recommendation-button', 'index': drug},
            className="m-1",
            color="primary",
            n_clicks=0
        ) for drug in recommendations
    ]

# Callback to maintain checkbox state
@app.callback(
    Output("side-effects-checklist", "value"),
    Input("side-effects-checklist", "options"),
    prevent_initial_call=True
)
def maintain_checkbox_state(options):
    return [option['value'] for option in options] if options else []

# Callback to handle recommendation button clicks
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
    
    clicked_index = next((i for i, n in enumerate(n_clicks) if n is not None and n > 0), None)
    return button_ids[clicked_index]['index'] if clicked_index is not None else no_update

if __name__ == "__main__":
    app.run(debug=True)